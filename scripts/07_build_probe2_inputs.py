#!/usr/bin/env python3
"""Build the matrices probe v2 needs from the combined and donor-pair DE fits (run once).

Eligible rows: QC-passing perturbation x condition rows with a mapped GeneID that have a
fit in every donor pair (D-015). Readouts: the measured genes present in the donor-pair
fits. Writes data_root/derived/probe2/: rows.parquet, readouts.parquet, matrices.npz.
Prints aggregate counts only.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from dgbench.config import derived_path, load_config  # noqa: E402
from dgbench.donors import changed_mask, label_codes, obs_keys, paired_row_corr, read_rows, row_corr, var_index  # noqa: E402
from dgbench.perturb import read_obs_var  # noqa: E402

OBS_COLS = ["target_baseMean", "ontarget_effect_size", "ontarget_significant", "donor_correlation_all_mean",
            "n_downstream", "n_cells_target", "n_guides"]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", default=None)
    ap.add_argument("--chunk", type=int, default=2000, help="rows per chunk when scanning all QC rows")
    args = ap.parse_args()
    cfg = load_config(args.config)
    cols, t, p2 = cfg["columns"], cfg["probe"]["truth"], cfg["probe2"]
    comb, pairs = cols["de_results"]["path"], p2["donor_pairs_path"]
    lfc_key, padj_key = f"layers/{cols['layers']['lfc']}", f"layers/{cols['layers']['padj']}"
    conditions = list(cfg["probe"]["condition_text"])
    mods = sorted({m for split in p2["agreement"]["splits"].values() for m in split})

    ptab = pd.read_parquet(derived_path(cfg, "perturbations.parquet"))
    obs, _ = read_obs_var(comb)
    for c in OBS_COLS:
        ptab[c] = obs[c].to_numpy()
    mod_keys = {m: obs_keys(pairs, f"mod/{m}") for m in mods}
    in_all = set.intersection(*(set(k) for k in mod_keys.values()))
    ptab["covered"] = ptab["obs_name"].isin(in_all)
    rows = ptab[ptab["covered"] & ptab["qc_pass"] & ptab["GeneID"].notna()].copy()
    rows["GeneID"] = rows["GeneID"].astype("int64")
    rows = rows.sort_values("obs_index").reset_index(drop=True)
    print(f"rows with fits in all {len(mods)} donor pairs: {int(ptab['covered'].sum())}; eligible (QC, mapped): {len(rows)}")

    comb_var = var_index(comb, "")
    pair_var = var_index(pairs, f"mod/{mods[0]}")
    for m in mods[1:]:
        assert (var_index(pairs, f"mod/{m}") == pair_var).all(), m
    pos = {g: i for i, g in enumerate(comb_var)}
    comb_cols = np.array([pos[g] for g in pair_var])
    readouts = pd.DataFrame({"readout_id": pair_var})
    gene_symbol = cols["var"].get("gene_symbol")
    _, var = read_obs_var(comb)
    readouts["readout"] = (var[gene_symbol].to_numpy() if gene_symbol else var.index.to_numpy())[comb_cols].astype(str)
    print(f"readouts with donor-pair fits: {len(readouts)} of {len(comb_var)}")

    out: dict[str, np.ndarray] = {}
    cond_idx = {c: np.flatnonzero(rows["condition"].to_numpy() == c) for c in conditions}

    lfc = read_rows(comb, lfc_key, rows["obs_index"].to_numpy(), comb_cols)
    padj = read_rows(comb, padj_key, rows["obs_index"].to_numpy(), comb_cols)
    out["labels_comb"] = label_codes(lfc, padj, t["alpha"], t["lfc_min"], t["none_padj_min"], t["none_lfc_max"])
    # rank of each readout by |z| within its row (0 = strongest), for top-effect readouts
    z = np.abs(read_rows(comb, f"layers/{cols['layers']['z']}", rows["obs_index"].to_numpy(), comb_cols))
    order = np.argsort(-np.nan_to_num(z, nan=-1), axis=1, kind="stable")
    zrank = np.empty_like(order, dtype=np.int16)
    np.put_along_axis(zrank, order, np.arange(order.shape[1], dtype=np.int16)[None, :].repeat(len(order), 0), axis=1)
    out["zrank_comb"] = zrank
    del z, order
    # F-neighbour: informative readouts per condition = the N most often changed among covered perturbations (D-020)
    changed = changed_mask(lfc, padj, t["alpha"], t["lfc_min"])
    n_grid = p2["neighbour"]["n_inf_grid"]
    inf_cols = {}
    for c, ix in cond_idx.items():
        order = np.argsort(-changed[ix].sum(0), kind="stable")
        for n in n_grid:
            inf_cols[(n, c)] = np.sort(order[:n])
            out[f"infcols_{n}_{c}"] = inf_cols[(n, c)]
            out[f"corrinf_{n}_comb_{c}"] = row_corr(lfc[ix][:, inf_cols[(n, c)]])
    del changed
    out["nde_comb"] = ((padj < t["alpha"]) & np.isfinite(padj)).sum(1).astype(np.int32)
    for c, ix in cond_idx.items():
        out[f"corr_comb_{c}"] = row_corr(lfc[ix])
    del lfc, padj

    # responsiveness: per condition, how many QC-passing perturbations change each readout
    qc = ptab[ptab["qc_pass"] & ptab["condition"].isin(conditions)].sort_values("obs_index")
    resp = np.zeros((len(conditions), len(pair_var)), dtype=np.int32)
    for start in range(0, len(qc), args.chunk):
        part = qc.iloc[start:start + args.chunk]
        ch = changed_mask(read_rows(comb, lfc_key, part["obs_index"].to_numpy(), comb_cols),
                          read_rows(comb, padj_key, part["obs_index"].to_numpy(), comb_cols), t["alpha"], t["lfc_min"])
        for k, c in enumerate(conditions):
            resp[k] += ch[part["condition"].to_numpy() == c].sum(0)
    out["resp"] = resp
    print(f"responsiveness computed over {len(qc)} QC-passing rows")

    for name, (a, b) in p2["agreement"]["splits"].items():
        halves = {}
        for m in (a, b):
            mpos = {k: i for i, k in enumerate(mod_keys[m])}
            mrows = np.array([mpos[k] for k in rows["obs_name"]])
            mlfc = read_rows(pairs, f"mod/{m}/{lfc_key}", mrows)
            mpadj = read_rows(pairs, f"mod/{m}/{padj_key}", mrows)
            out[f"labels_{m}"] = label_codes(mlfc, mpadj, t["alpha"], t["lfc_min"], t["none_padj_min"], t["none_lfc_max"])
            out[f"nde_{m}"] = ((mpadj < t["alpha"]) & np.isfinite(mpadj)).sum(1).astype(np.int32)
            for c, ix in cond_idx.items():
                out[f"corr_{m}_{c}"] = row_corr(mlfc[ix])
                for n in n_grid:
                    out[f"corrinf_{n}_{m}_{c}"] = row_corr(mlfc[ix][:, inf_cols[(n, c)]])
            del mpadj
            halves[m] = mlfc
        out[f"selfcorr_{name}"] = paired_row_corr(halves[a], halves[b]).astype(np.float32)
        for n in n_grid:
            sc = np.full(len(rows), np.nan, dtype=np.float32)
            for c, ix in cond_idx.items():
                sc[ix] = paired_row_corr(halves[a][ix][:, inf_cols[(n, c)]], halves[b][ix][:, inf_cols[(n, c)]])
            out[f"selfcorrinf_{n}_{name}"] = sc
        del halves
        print(f"split {name}: done")

    d = derived_path(cfg, "probe2")
    d.mkdir(exist_ok=True)
    rows.to_parquet(d / "rows.parquet", index=False)
    readouts.to_parquet(d / "readouts.parquet", index=False)
    np.savez(d / "matrices.npz", **out)
    print(f"wrote {d}")


if __name__ == "__main__":
    main()
