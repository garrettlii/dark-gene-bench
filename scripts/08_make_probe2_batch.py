#!/usr/bin/env python3
"""Generate a probe v2 batch (named vs hidden gene, prior-only).

--dry-run: builds candidates for every FILL candidate value in config (probe2.*_grid and
*_quantiles) and every donor-agreement option, prints a summary and writes the full aggregate
tables to reports/probe2_dryrun.md. Nothing goes to runs_root or truth_root.
Without --dry-run: refuses unless the probe v2 pre-registration passes check_prereg and every
FILL value in config is set; then writes prompts, per-model shuffled call orders, truth,
baseline training data and a manifest (CLI versions, command lines, GO releases).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from dgbench.baselines import Context, balanced_pool, crossfit, label_index  # noqa: E402
from dgbench.batch import batch_dirs, new_batch_id, read_jsonl, sha256_file, write_json  # noqa: E402
from dgbench.config import REPO_ROOT, config_hash, derived_path, load_config  # noqa: E402
from dgbench.genes import build_maps, read_gene_info, strip_version  # noqa: E402
from dgbench.go import COMPLEX_ROOT, descendants, filter_annotations, gene_terms, pairwise, read_gaf, read_obo_parents, term_sizes  # noqa: E402
from dgbench.prereg import PreregError, check_prereg  # noqa: E402
from dgbench.probe2 import (LABELS, NeighbourSpec, agrees, build_prompts, cell_capacity, effect_terciles, gene_pairs,  # noqa: E402
                            neighbour_items, readout_candidates, run_order, stratified_sample, wrong_names)

POOL = "_pool"  # constant bin column: the flagged stratum is pooled across density bins (D-022)


# ---------------------------------------------------------------- inputs

def load_inputs(cfg):
    d = derived_path(cfg, "probe2")
    rows = pd.read_parquet(d / "rows.parquet")
    readouts = pd.read_parquet(d / "readouts.parquet")
    M = dict(np.load(d / "matrices.npz"))
    genes = pd.read_parquet(derived_path(cfg, "genes.parquet"))
    cutoffs = sorted({m["cutoff_date"] for m in cfg["models"] if m.get("enabled") and m.get("cutoff_date")})
    keep = ["GeneID", "symbol", "flagged_paper", "density_bin_strata"] + [c for c in genes if c.startswith(("log_density_", "density_bin_2"))]
    rows = rows.drop(columns=[c for c in keep if c != "GeneID" and c in rows]).merge(genes[keep], on="GeneID", how="left")
    rows = rows.rename(columns={"density_bin_strata": "density_bin"})
    p0_path = Path(cfg["probe2"]["phase0_truth"]).expanduser()
    if not p0_path.exists():  # read_jsonl returns [] for a missing file, which would silently drop the exclusion
        raise FileNotFoundError(f"probe2.phase0_truth not found: {p0_path}")
    phase0 = {r["GeneID"] for r in read_jsonl(p0_path)}
    rows["phase0"] = rows["GeneID"].isin(phase0)
    rows["density_bin"] = rows["density_bin"].astype(int)
    rows["eff_class"] = effect_terciles(rows)
    rows[POOL] = 0
    return rows, readouts, M, cutoffs, phase0


def go_terms(cfg, cutoff, no_iea=False):
    """Terms per GeneID from the archived release for this cutoff (D-021)."""
    rel = cfg["go"]["releases"][cutoff]
    maps = build_maps(read_gene_info(cfg["ncbi"]["gene_info"]))
    gaf = read_gaf(rel["path"])
    kept = filter_annotations(gaf, cfg["go"]["exclude_refs"], exclude_evidence=("IEA",) if no_iea else ())
    terms = gene_terms(kept, {**maps.synonym, **maps.symbol})
    complexes = (descendants(COMPLEX_ROOT, read_obo_parents(cfg["go"]["obo"])) | {COMPLEX_ROOT}) & set(kept.loc[kept["aspect"] == "C", "go_id"])
    stats = {"release": rel["release"], "date_generated": rel["date_generated"], "annotations": len(gaf), "kept": len(kept),
             "IEA": int((gaf["evidence"] == "IEA").sum()),
             "citing_dataset_paper": int(len(gaf) - len(filter_annotations(gaf, cfg["go"]["exclude_refs"]))),
             "genes_with_terms": len(terms)}
    return terms, term_sizes(terms), complexes, stats


def target_columns(rows, readouts):
    pos = {g: i for i, g in enumerate(readouts["readout_id"])}
    return np.array([pos.get(strip_version(str(e)), -1) for e in rows["target_ensembl"]])


def go_matrices(rows, conditions, terms, sizes, complex_terms, go_max_genes):
    small = {t for t, n in sizes.items() if n <= go_max_genes}
    out = {}
    for c in conditions:
        g = rows["GeneID"].to_numpy()[rows["condition"].to_numpy() == c]
        out[c] = (pairwise(g, terms)[0], pairwise(g, terms, small)[1], pairwise(g, terms, complex_terms)[1])
    return out


def neighbour_build(cfg, rows, M, n_inf, splits, targets, option_ok, go_mats, spec, seed, self_thr=None):
    """F-neighbour items per condition. With ``self_thr`` ({condition: threshold}) the spec comes from
    config with that condition's self-reliability threshold and no margin filter (the caller applies it)."""
    p2 = cfg["probe2"]
    ng = p2["neighbour"]
    mods = [m for s in splits for m in p2["agreement"]["splits"][s]]
    selfc = np.min(np.stack([M[f"selfcorrinf_{n_inf}_{s}"] for s in splits]), axis=0)
    items = []
    for c in cfg["probe"]["condition_text"]:
        cr = np.flatnonzero(rows["condition"].to_numpy() == c)
        halves = [M[f"corrinf_{n_inf}_{m}_{c}"] for m in mods]
        sp = spec if self_thr is None else NeighbourSpec(ng["min_de"], self_thr[c], -np.inf, ng["go_max_genes"], ng["match_log2_tol"])
        items.append(neighbour_items(rows, cr, M[f"corrinf_{n_inf}_comb_{c}"], halves, M["nde_comb"][cr], selfc[cr], targets[cr],
                                     option_ok[cr], *go_mats[c], sp, np.random.default_rng(seed)).assign(condition=c))
    items = pd.concat(items, ignore_index=True)
    if len(items):
        items["density_bin"] = rows["density_bin"].to_numpy()[items["target"].astype(int)]
        items["GeneID"] = rows["GeneID"].to_numpy()[items["target"].astype(int)]
    return items


# ---------------------------------------------------------------- reporting helpers

def effect_summary(df, by, col="n_downstream"):
    g = df.groupby(by)[col]
    return pd.DataFrame({"n": g.size(), "p25": g.quantile(.25), "median": g.median(), "p75": g.quantile(.75)}).round(2)


def md_table(df):
    df = df.reset_index() if not isinstance(df.index, pd.RangeIndex) else df
    head = "| " + " | ".join(map(str, df.columns)) + " |"
    sep = "|" + "---|" * len(df.columns)
    return "\n".join([head, sep] + ["| " + " | ".join(map(str, r)) + " |" for r in df.itertuples(index=False)])


def max_fill(cap, cell_cols, bins, value="genes"):
    """Largest per-cell count every cell reaches in every bin (at one item per gene per cell)."""
    if cap.empty:
        return 0, []
    piv = cap.pivot_table(index=cell_cols, columns="density_bin", values=value, fill_value=0).reindex(columns=bins, fill_value=0)
    return int(piv.min(axis=1).min()), [tuple(np.atleast_1d(i)) for i in piv.index[piv.min(axis=1) == 0]]


def pooled_capacity(cand, cells):
    """Flagged stratum: distinct genes per cell, pooled over bins (D-022)."""
    if cand.empty:
        return pd.DataFrame(columns=cells + ["genes"])
    return cand.groupby(cells)["GeneID"].nunique().rename("genes").reset_index()


def pairs_frame(rows, pairs):
    p = pairs.copy()
    p["condition"] = rows["condition"].to_numpy()[p["row_a"]]
    p["density_bin"] = rows["density_bin"].to_numpy()[p["row_a"]]
    p["GeneID"] = list(zip(rows["GeneID"].to_numpy()[p["row_a"]], rows["GeneID"].to_numpy()[p["row_b"]]))
    return p


# ---------------------------------------------------------------- generation

def cli_versions(cfg):
    out = {}
    for m in cfg["models"]:
        if m.get("enabled") and m.get("version_command"):
            proc = subprocess.run(m["version_command"], capture_output=True, text=True, stdin=subprocess.DEVNULL)
            out[m["name"]] = (proc.stdout or proc.stderr).strip()
    return out


def orient_pairs(pairs, rng):
    """Randomize which gene is shown as A; label is the position of the larger DE count."""
    flip = rng.random(len(pairs)) < 0.5
    a = np.where(flip, pairs["row_b"], pairs["row_a"])
    b = np.where(flip, pairs["row_a"], pairs["row_b"])
    larger_is_a = np.where(flip, pairs["larger"] == 1, pairs["larger"] == 0)
    return pd.DataFrame({"row_a": a, "row_b": b, "label": np.where(larger_is_a, "A", "B")})


def option_mask(cfg, rows):
    """Options and distractors: never flagged; Phase 0 genes excluded if configured."""
    ok = ~rows["flagged_paper"].to_numpy()
    if cfg["probe2"]["neighbour"]["options_exclude_phase0"]:
        ok &= ~rows["phase0"].to_numpy()
    return ok


def family_splits(cfg, family):
    """Donor splits of the agreement filter chosen for this family (probe2.agreement.chosen is per family, D-024)."""
    a = cfg["probe2"]["agreement"]
    chosen = a["chosen"][family] if isinstance(a["chosen"], dict) else a["chosen"]
    return chosen, a["candidates"][chosen]


def neighbour_thresholds(cfg, rows, M, splits, targets, option_ok, go_mats):
    """Per-condition absolute thresholds from the pre-registered quantiles (D-024): self-reliability
    at its quantile over covered perturbations in the condition, margin at its quantile over the
    condition's main-stratum candidate items."""
    ng, conditions = cfg["probe2"]["neighbour"], list(cfg["probe"]["condition_text"])
    selfc = np.min(np.stack([M[f"selfcorrinf_{ng['n_inf']}_{s}"] for s in splits]), axis=0)
    cond = rows["condition"].to_numpy()
    self_thr = {c: float(np.nanquantile(selfc[cond == c], ng["min_self_corr_quantile"])) for c in conditions}
    items = neighbour_build(cfg, rows, M, ng["n_inf"], splits, targets, option_ok, go_mats, None, cfg["probe2"]["seed"],
                            self_thr=self_thr)
    margin_thr = {c: float(np.quantile(items.loc[items["condition"] == c, "margin"], ng["margin_quantile"]))
                  if (items["condition"] == c).any() else float("inf") for c in conditions}
    return self_thr, margin_thr


def build_family(cfg, family, stratum, rows, M, tcols, go_mats, rng, used_main=frozenset(), nthr=None):
    """Candidates for one family and stratum at the configured (FILL) values and that family's agreement filter."""
    p2 = cfg["probe2"]
    _, splits = family_splits(cfg, family)
    mods = [m for s in splits for m in p2["agreement"]["splits"][s]]
    conditions = list(cfg["probe"]["condition_text"])
    gid, bins = rows["GeneID"].to_numpy(), rows["density_bin"].to_numpy()
    not0 = ~rows["phase0"].to_numpy()
    flagged = rows["flagged_paper"].to_numpy()
    targets = not0 & (flagged if stratum == "flagged" else ~flagged)
    if family == "readout":
        c = readout_candidates(rows, M["labels_comb"], M["resp"], conditions, tcols, p2["readout"]["R"],
                               agree=agrees(M["labels_comb"], [M[f"labels_{m}"] for m in mods]),
                               zrank=M["zrank_comb"], top_k=p2["readout"].get("top_k_effects"))
        c = c[targets[c["row"].to_numpy()]].copy()
        c["GeneID"], c["density_bin"], c[POOL] = gid[c["row"]], bins[c["row"]], 0
        use_cls = p2["readout"]["use_class"] and stratum == "main"
        return c, ["condition", "label"] + (["eff_class"] if use_cls else [])
    if family == "gene":
        nh = [M[f"nde_{m}"] for m in mods]
        if stratum == "main":
            pairs = gene_pairs(rows, M["nde_comb"], nh, p2["gene"]["ratio"], p2["gene"]["match_log2_tol"], not0 & ~flagged)
        else:  # one flagged gene plus an unflagged partner not used in the main stratum (D-022)
            partner_ok = not0 & ~flagged & ~np.isin(gid, list(used_main))
            pairs = gene_pairs(rows, M["nde_comb"], nh, p2["gene"]["ratio"], p2["gene"]["match_log2_tol"],
                               (not0 & flagged) | partner_ok, one_of=flagged)
        c = pairs_frame(rows, orient_pairs(pairs, rng))
        c[POOL] = 0
        return c, ["condition", "label"]
    ng = p2["neighbour"]
    self_thr, margin_thr = nthr
    c = neighbour_build(cfg, rows, M, ng["n_inf"], splits, targets, option_mask(cfg, rows), go_mats, None, p2["seed"], self_thr=self_thr)
    if len(c):
        c = c[c["margin"].to_numpy() >= c["condition"].map(margin_thr).to_numpy()].copy()
    if stratum == "flagged":
        c = c[c["tier"].isin(ng.get("flagged_tiers", ["easy"]))].copy()
    c[POOL] = 0
    return c, (["tier", "condition"] if stratum == "main" else ["condition"])


def sample_family(cand, cells, per_cell, max_per_gene, rng, **kw):
    """stratified_sample, with per_cell either one count or a count per F-neighbour tier."""
    if not isinstance(per_cell, dict):
        return stratified_sample(cand, cells, per_cell, max_per_gene, rng, **kw)
    parts, dropped = [], []
    for tier, n in per_cell.items():
        sel, drop = stratified_sample(cand[cand["tier"] == tier], cells, n, max_per_gene, rng, **kw)
        parts.append(sel)
        dropped += drop if len(cand[cand["tier"] == tier]) else [(tier, "no candidates")]
    return pd.concat(parts), dropped


def select_questions(cfg):
    """Pre-registered selection without writing anything: questions, dropped cells, baseline pool, context."""
    p2, cond_text = cfg["probe2"], cfg["probe"]["condition_text"]
    rows, readouts, M, cutoffs, phase0 = load_inputs(cfg)
    rng = np.random.default_rng(p2["seed"])
    tcols = target_columns(rows, readouts)
    terms, sizes, complex_terms, gostats = go_terms(cfg, cutoffs[0])
    go_mats = go_matrices(rows, list(cond_text), terms, sizes, complex_terms, p2["neighbour"]["go_max_genes"])
    not0, flagged = ~rows["phase0"].to_numpy(), rows["flagged_paper"].to_numpy()
    nthr = None
    if "neighbour" in p2["families"]:
        nthr = neighbour_thresholds(cfg, rows, M, family_splits(cfg, "neighbour")[1], not0 & ~flagged, option_mask(cfg, rows), go_mats)
    bins = sorted(rows["density_bin"].unique())
    selected, dropped, outside = [], {}, []
    for family in p2["families"]:
        used_main: set = set()
        for stratum in ("main", "flagged"):
            cand, cells = build_family(cfg, family, stratum, rows, M, tcols, go_mats, rng, frozenset(used_main), nthr)
            if stratum == "main":
                sel, drop = sample_family(cand, cells, p2[family]["per_cell"], p2["max_per_gene"], rng, bins=bins)
                used_main = {x for g in sel["GeneID"] for x in (g if isinstance(g, tuple) else (g,))}
            else:
                sel, drop = sample_family(cand, cells, p2["flagged_per_cell"][family], p2["max_per_gene"], rng, bin_col=POOL, bins=[0])
            dropped[f"{family}/{stratum}"] = [list(map(str, d)) for d in drop]
            cell_key = ["|".join(map(str, v)) for v in sel[cells].itertuples(index=False)]
            selected.append(sel.assign(family=family, stratum=stratum, cell=cell_key))
            if stratum == "main":  # baseline training pool: strata-balanced candidates whose genes are not in the batch
                rest = cand[[not any(x in used_main for x in (g if isinstance(g, tuple) else (g,))) for g in cand["GeneID"]]]
                outside.append(balanced_pool(rest, cells, p2["baseline_train_max"], p2["seed"]).assign(family=family))
    q = pd.concat(selected, ignore_index=True)
    q["qid"] = [f"q{x:06d}" for x in rng.permutation(len(q))]
    q["sol"] = False  # sol subset: the same fraction of every family x stratum x cell x bin, half rounding up
    for _, idx in q.groupby(["family", "stratum", "cell", "density_bin"]).groups.items():
        idx = list(idx)
        take = rng.choice(idx, size=int(np.floor(len(idx) * p2["sol_fraction"] + 0.5)), replace=False) if idx else []
        q.loc[take, "sol"] = True

    sym = rows["symbol"].to_numpy()
    versions = ("named", "hidden") + (("wrong",) if p2.get("wrong_name") else ())
    if p2.get("wrong_name"):  # third version naming a different real gene (same bin, expression-matched)
        qrows, excl = [], []
        for r in q.itertuples(index=False):
            if r.family == "readout":
                qrows.append([int(r.row)]); excl.append({readouts["readout"].iat[int(r.readout_col)]})
            elif r.family == "gene":
                qrows.append([int(r.row_a), int(r.row_b)]); excl.append(set())
            else:
                qrows.append([int(r.target)]); excl.append({sym[int(o)] for o in r.options})
        q["wrong_rows"] = wrong_names(rows, qrows, excl, p2["wrong_name_match_log2_tol"], ~flagged & not0, rng)
        n_missing = int(q["wrong_rows"].isna().sum())
        if n_missing:
            print(f"note: {n_missing} questions have no wrong-name substitute and are dropped")
            q = q[q["wrong_rows"].notna()].reset_index(drop=True)
    thresholds = {"neighbour": {"min_self_corr": nthr[0], "margin": nthr[1]}} if nthr else {}
    return dict(q=q, dropped=dropped, outside=outside, rows=rows, readouts=readouts, M=M, cutoffs=cutoffs, gostats=gostats,
                versions=versions, thresholds=thresholds, rng=rng)


def generate(cfg, prereg, additional_reason):
    p2, cond_text = cfg["probe2"], cfg["probe"]["condition_text"]
    ledger = Path(cfg["paths"]["truth_root"]) / "ledger.jsonl"
    earlier = [e for e in read_jsonl(ledger) if e["prereg_path"] == prereg["path"] and e["prereg_commit"] == prereg["commit"]]
    if earlier and not additional_reason:
        sys.exit(f"{len(earlier)} batch(es) already generated under this pre-registration; pass --additional-batch-reason")
    S = select_questions(cfg)
    q, dropped, outside, rows, readouts, M = S["q"], S["dropped"], S["outside"], S["rows"], S["readouts"], S["M"]
    cutoffs, gostats, versions, rng = S["cutoffs"], S["gostats"], S["versions"], S["rng"]
    sym = rows["symbol"].to_numpy()

    batch_id = new_batch_id("p2")
    run_dir, truth_dir = batch_dirs(cfg, batch_id, create=True)
    prompts, truth = [], []
    covars = ["n_downstream", "target_baseMean", "ontarget_effect_size", "donor_correlation_all_mean"]
    for r in q.itertuples(index=False):
        if r.family == "readout":
            row, col = int(r.row), int(r.readout_col)
            genes = {"target": sym[row], "readout": readouts["readout"].iat[col]}
            gene_rows, extra = [row], {"readout_id": readouts["readout_id"].iat[col], "eff_class": int(r.eff_class)}
        elif r.family == "gene":
            ra, rb = int(r.row_a), int(r.row_b)
            genes = {"gene_a": sym[ra], "gene_b": sym[rb]}
            na, nb = float(M["nde_comb"][ra]), float(M["nde_comb"][rb])
            gene_rows, extra = [ra, rb], {"nde_ratio": max(na, nb) / max(min(na, nb), 1.0)}
        else:
            opts = [int(o) for o in r.options]
            genes = {"target": sym[int(r.target)], **{f"opt_{k}": sym[o] for k, o in zip("abcd", opts)}}
            gene_rows, extra = [int(r.target)], {"tier": r.tier, "option_GeneIDs": [int(rows["GeneID"].iat[o]) for o in opts],
                                                 "margin": float(r.margin)}
        texts = build_prompts(r.family, cond_text[r.condition], **genes)
        if p2.get("wrong_name"):
            wr = list(r.wrong_rows)
            keys = {"readout": ["target"], "gene": ["gene_a", "gene_b"], "neighbour": ["target"]}[r.family]
            texts["wrong"] = build_prompts(r.family, cond_text[r.condition], **{**genes, **{k: sym[w] for k, w in zip(keys, wr)}})["named"]
            extra["wrong_GeneIDs"] = [int(rows["GeneID"].iat[w]) for w in wr]
        for version, text in texts.items():
            prompts.append({"qid": r.qid, "version": version, "family": r.family, "labels": list(LABELS[r.family]), "prompt": text})
        gr = rows.iloc[gene_rows]
        truth.append({"qid": r.qid, "family": r.family, "stratum": r.stratum, "cell": r.cell, "condition": r.condition,
                      "label": r.label, "density_bin": int(r.density_bin), "sol": bool(r.sol),
                      "GeneIDs": gr["GeneID"].astype(int).tolist(), "symbols": gr["symbol"].tolist(),
                      **{f"log_density_{d}": float(gr[f"log_density_{d}"].mean()) for d in cutoffs},
                      **{f"log_density_tcell_{d}": float(gr[f"log_density_tcell_{d}"].mean()) for d in cutoffs if f"log_density_tcell_{d}" in gr},
                      **{c: float(gr[c].astype(float).mean()) for c in covars}, **extra})
    k = cfg["run"]["samples"]
    with open(run_dir / "prompts.jsonl", "w") as fh:
        for p in prompts:
            fh.write(json.dumps(p) + "\n")
    for m in cfg["models"]:
        if not m.get("enabled"):
            continue
        qids = set(q["qid"]) if m["name"] != "sol-6.1-cli" else set(q.loc[q["sol"], "qid"])
        calls = run_order([(qid, v, s) for qid in sorted(qids) for v in versions for s in range(k)], rng)
        with open(run_dir / f"calls_{m['name']}.jsonl", "w") as fh:
            for qid, v, s in calls:
                fh.write(json.dumps({"qid": qid, "version": v, "sample": s}) + "\n")
    with open(truth_dir / "truth.jsonl", "w") as fh:
        for t in truth:
            fh.write(json.dumps(t, default=int) + "\n")
    pd.concat(outside, ignore_index=True).assign(GeneID=lambda d: d["GeneID"].astype(str)).to_parquet(truth_dir / "baseline_train.parquet")
    releases = {d: {**cfg["go"]["releases"][d], "sha256": sha256_file(cfg["go"]["releases"][d]["path"])} for d in cutoffs}
    manifest = {
        "batch_id": batch_id, "created_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "phase": "probe2",
        "prereg": {k_: v for k_, v in prereg.items() if k_ != "predictions"}, "predictions": prereg["predictions"],
        "config_hash": config_hash(cfg), "config": cfg, "samples": k,
        "cli": {"versions": cli_versions(cfg), "commands": {m["name"]: m.get("command") for m in cfg["models"] if m.get("enabled")}},
        "sha256": {"de_results": sha256_file(cfg["columns"]["de_results"]["path"]), "donor_pairs": sha256_file(p2["donor_pairs_path"])},
        "go_releases": releases, "go_stats_items": gostats, "n_questions": len(q), "dropped_cells": dropped,
        "agreement_per_family": {f: family_splits(cfg, f)[0] for f in p2["families"]}, "thresholds": S["thresholds"],
        "per_family": {"/".join(k_): int(v) for k_, v in q.groupby(["family", "stratum"]).size().items()},
    }
    write_json(run_dir / "manifest.json", {k_: v for k_, v in manifest.items() if k_ != "predictions"})
    write_json(truth_dir / "manifest.json", manifest)
    with open(ledger, "a") as fh:
        fh.write(json.dumps({"batch_id": batch_id, "created_at": manifest["created_at"], "prereg_path": prereg["path"],
                             "prereg_commit": prereg["commit"], "additional_batch_reason": additional_reason}) + "\n")
    print(f"batch {batch_id}: {len(q)} questions; dropped cells: {dropped}\n  run dir: {run_dir}\n  truth: {truth_dir}")


# ---------------------------------------------------------------- dry run

def dry_run(cfg):
    p2, conditions = cfg["probe2"], list(cfg["probe"]["condition_text"])
    rows, readouts, M, cutoffs, phase0 = load_inputs(cfg)
    bins = sorted(rows["density_bin"].unique())
    tcols = target_columns(rows, readouts)
    flagged, not0 = rows["flagged_paper"].to_numpy(), ~rows["phase0"].to_numpy()
    main_t, flag_t = not0 & ~flagged, not0 & flagged
    rep = ["# Probe v2 dry run", "", f"Generated {dt.date.today().isoformat()}. Aggregate counts only; nothing written to runs_root or truth_root.",
           "Capacities: main stratum = the largest per-cell count every cell reaches in every bin at one item per gene per cell; "
           "flagged stratum = distinct genes in the smallest cell, pooled over bins (D-022).", ""]
    summary = []

    genes = pd.read_parquet(derived_path(cfg, "genes.parquet"))
    qcg = genes[genes["qc_pass_any"] & genes["density_bin_strata"].notna()]
    cov = qcg["GeneID"].isin(set(rows["GeneID"]))
    p0 = qcg["GeneID"].isin(phase0)
    att = pd.DataFrame({"qc_genes": qcg.groupby("density_bin_strata").size(),
                        "covered": qcg[cov].groupby("density_bin_strata").size(),
                        "minus_phase0": qcg[cov & ~p0].groupby("density_bin_strata").size(),
                        "main_targets": qcg[cov & ~p0 & ~qcg["flagged_paper"]].groupby("density_bin_strata").size(),
                        "flagged_targets": qcg[cov & ~p0 & qcg["flagged_paper"]].groupby("density_bin_strata").size()}).fillna(0).astype(int)
    att.index.name = "bin"
    print(f"Phase 0 genes excluded: {len(phase0)} (covered: {len(set(rows['GeneID']) & phase0)})")
    rep += ["## Scope and Phase 0 exclusion (genes per strata bin)", "", f"Phase 0 genes excluded from sampling: {len(phase0)}.", "", md_table(att), ""]

    rep += ["## GO annotations (archived release closest before each cutoff; D-021)", ""]
    for d in cutoffs:
        for no_iea in (False, True):
            st = go_terms(cfg, d, no_iea)[3]
            rep.append(f"- cutoff {d}{' (no-IEA variant)' if no_iea else ''}: " + ", ".join(f"{k} {v}" for k, v in st.items()))
    rep.append("")
    terms, sizes, complex_terms, _ = go_terms(cfg, cutoffs[0])

    splits_of = p2["agreement"]["candidates"]
    label_halves = {a: [M[f"labels_{m}"] for s in sp for m in p2["agreement"]["splits"][s]] for a, sp in splits_of.items()}
    nde_halves = {a: [M[f"nde_{m}"] for s in sp for m in p2["agreement"]["splits"][s]] for a, sp in splits_of.items()}

    # ---- F-readout
    rep += ["## F-readout (strata: condition x label x target effect-size tercile, D-019)", ""]
    for R, tk in [(R, tk) for R in p2["readout"]["R_grid"] for tk in p2["readout"]["top_k_effects_grid"]]:
        base = readout_candidates(rows, M["labels_comb"], M["resp"], conditions, tcols, R, zrank=M["zrank_comb"], top_k=tk)
        for ag, halves in label_halves.items():
            cand = readout_candidates(rows, M["labels_comb"], M["resp"], conditions, tcols, R, agree=agrees(M["labels_comb"], halves),
                                      zrank=M["zrank_comb"], top_k=tk)
            cand["GeneID"], cand["density_bin"] = rows["GeneID"].to_numpy()[cand["row"]], rows["density_bin"].to_numpy()[cand["row"]]
            c = cand[main_t[cand["row"].to_numpy()]]
            for use_cls in (True, False):
                cells = ["condition", "label"] + (["eff_class"] if use_cls else [])
                cap = cell_capacity(c, cells)
                mf, empty = max_fill(cap, cells, bins)
                summary.append(("readout", "main", f"R={R}, top_k={tk or 'all'}", ag, "effect tercile" if use_cls else "no tercile", mf, len(empty)))
                if use_cls and R == p2["readout"]["R_grid"][1]:
                    piv = cap.pivot_table(index=cells, columns="density_bin", values="genes", fill_value=0)
                    rep += [f"### R={R}, top_k={tk or 'all'}, agreement {ag}, main, with effect tercile: distinct genes per cell and bin", "", md_table(piv), ""]
            fc = pooled_capacity(cand[flag_t[cand["row"].to_numpy()]], ["condition", "label"])
            summary.append(("readout", "flagged (pooled)", f"R={R}, top_k={tk or 'all'}", ag, "condition x label",
                            int(fc["genes"].min()) if len(fc) == 3 * len(conditions) else 0, 3 * len(conditions) - len(fc)))
            if ag == "all_three":
                b = base[main_t[base["row"].to_numpy()]]
                bb = pd.DataFrame({"bin": rows["density_bin"].to_numpy()[b["row"]], "label": b["label"]}).value_counts().rename("before")
                aa = pd.DataFrame({"bin": c["density_bin"], "label": c["label"]}).value_counts().rename("after_all_three")
                rep += [f"### R={R}, top_k={tk or 'all'}: agreement attrition (main, candidates)", "", md_table(pd.concat([bb, aa], axis=1).fillna(0).astype(int).sort_index()), ""]
        del base

    rep += ["## Donor-agreement filter: target effect size (n_downstream) of changed readout questions, by bin and condition", "",
            "Each changed (decreased or increased) candidate question counts once.", ""]
    R0 = p2["readout"]["R_grid"][1]

    def changed_effects(cc):
        cc = cc[(cc["label"] != "unchanged") & main_t[cc["row"].to_numpy()]]
        return pd.DataFrame({"density_bin": rows["density_bin"].to_numpy()[cc["row"]], "condition": cc["condition"].to_numpy(),
                             "n_downstream": rows["n_downstream"].to_numpy()[cc["row"]]})

    base = readout_candidates(rows, M["labels_comb"], M["resp"], conditions, tcols, R0)
    rep += [f"Before agreement (R={R0}):", "", md_table(effect_summary(changed_effects(base), ["density_bin", "condition"])), ""]
    for ag, halves in label_halves.items():
        cand = readout_candidates(rows, M["labels_comb"], M["resp"], conditions, tcols, R0, agree=agrees(M["labels_comb"], halves))
        rep += [f"After agreement {ag}:", "", md_table(effect_summary(changed_effects(cand), ["density_bin", "condition"])), ""]
    del base

    # ---- F-gene
    rep += ["## F-gene", ""]
    nde = M["nde_comb"].astype(float)
    for ratio in p2["gene"]["ratio_grid"]:
        for tol in p2["gene"]["match_log2_tol_grid"]:
            for ag, nh in nde_halves.items():
                pairs = gene_pairs(rows, M["nde_comb"], nh, ratio, tol, main_t)
                if pairs.empty:
                    summary.append(("gene", "main", f"ratio={ratio}, tol={tol}", ag, "condition x label", 0, 2 * len(conditions)))
                else:
                    p = pairs_frame(rows, pairs)
                    piv = (p.pivot_table(index="condition", columns="density_bin", values="row_a", aggfunc="count", fill_value=0)
                           .reindex(index=conditions, columns=bins, fill_value=0))
                    summary.append(("gene", "main", f"ratio={ratio}, tol={tol}", ag, "condition x label", int(piv.min(axis=1).min()) // 2,
                                    int((piv.min(axis=1) == 0).sum())))
                    if ag == "all_three":
                        rep += [f"### ratio={ratio}, tol={tol}, agreement {ag}, main: candidate pairs per condition and bin "
                                "(each pair can fill either label cell)", "", md_table(piv), ""]
                    if ratio == p2["gene"]["ratio_grid"][1] and tol == p2["gene"]["match_log2_tol_grid"][-1]:
                        hi = np.maximum(nde[p["row_a"]], nde[p["row_b"]])
                        lo = np.minimum(nde[p["row_a"]], nde[p["row_b"]])
                        d = pd.DataFrame({"density_bin": p["density_bin"], "larger_nDE": hi, "smaller_nDE": lo, "ratio": hi / np.maximum(lo, 1)})
                        tab = d.groupby("density_bin").agg(pairs=("ratio", "size"),
                                                           larger_nDE_median=("larger_nDE", "median"), smaller_nDE_median=("smaller_nDE", "median"),
                                                           ratio_p25=("ratio", lambda x: x.quantile(.25)), ratio_median=("ratio", "median"),
                                                           ratio_p75=("ratio", lambda x: x.quantile(.75))).round(2)
                        rep += [f"### ratio={ratio}, tol={tol}, agreement {ag}: pairs' effect levels and ratios per bin", "", md_table(tab), ""]
                        d["band"] = pd.cut(d["ratio"], [0, 2, 4, 10, np.inf], right=False, labels=["<2", "2-4", "4-10", ">10"])
                        bands = d.pivot_table(index="density_bin", columns="band", values="ratio", aggfunc="count", fill_value=0, observed=False)
                        rep += [f"### ratio={ratio}, tol={tol}, agreement {ag}: candidate pairs per DE-count ratio band (descriptive)", "", md_table(bands), ""]
                fp = gene_pairs(rows, M["nde_comb"], nh, ratio, tol, flag_t | main_t, one_of=flagged)
                if fp.empty:
                    summary.append(("gene", "flagged (pooled)", f"ratio={ratio}, tol={tol}", ag, "condition x label", 0, 2 * len(conditions)))
                else:
                    fp = pairs_frame(rows, fp)
                    fgene = np.where(flagged[fp["row_a"]], rows["GeneID"].to_numpy()[fp["row_a"]], rows["GeneID"].to_numpy()[fp["row_b"]])
                    per = pd.Series(fgene).groupby(fp["condition"].to_numpy()).nunique().reindex(conditions, fill_value=0)
                    summary.append(("gene", "flagged (pooled)", f"ratio={ratio}, tol={tol}", ag, "condition x label",
                                    int(per.min()) // 2, int((per == 0).sum())))

    # ---- F-neighbour on informative readouts (D-020)
    ng = p2["neighbour"]
    rep += ["## F-neighbour (similarity over the n_inf most responsive readouts per condition; D-020)", "",
            f"Held at reference values: min_de {ng['min_de_grid'][1]}, go_max_genes {ng['go_max_genes_grid'][-1]}, "
            f"match_log2_tol {ng['match_log2_tol_grid'][-1]}. Self-reliability thresholds are quantiles over covered perturbations "
            "(minimum over the filter option's splits); margin thresholds are quantiles of the candidate items' gaps at that setting. "
            "Options and distractors never include flagged genes; capacity is shown with and without the Phase 0 exclusion for them.", ""]
    go_mats = go_matrices(rows, conditions, terms, sizes, complex_terms, ng["go_max_genes_grid"][-1])
    diag = []
    for n_inf in ng["n_inf_grid"]:
        for ag, splits in splits_of.items():
            selfc = np.min(np.stack([M[f"selfcorrinf_{n_inf}_{s}"] for s in splits]), axis=0)
            for c in conditions:
                cr = rows["condition"].to_numpy() == c
                corr = M[f"corrinf_{n_inf}_comb_{c}"].copy()
                np.fill_diagonal(corr, np.nan)
                q = lambda v: "/".join(f"{x:.2f}" for x in np.nanquantile(v, [.1, .5, .9]))
                diag.append((n_inf, ag, c, q(selfc[cr]), q(np.nanmax(corr[:, main_t[cr]], axis=1)), q(np.nanmedian(corr, axis=1))))
            for sq in ng["min_self_corr_quantiles"]:
                thr = float(np.nanquantile(selfc, sq))
                for excl0 in (True, False):
                    opt_ok = ~flagged & (not0 if excl0 else np.ones_like(not0))
                    opts = "options excl. Phase 0" if excl0 else "options incl. Phase 0"
                    spec = NeighbourSpec(ng["min_de_grid"][1], thr, -np.inf, ng["go_max_genes_grid"][-1], ng["match_log2_tol_grid"][-1])
                    for stratum, tmask in (("main", main_t), ("flagged (pooled)", flag_t)):
                        items = neighbour_build(cfg, rows, M, n_inf, splits, tmask, opt_ok, go_mats, spec, p2["seed"])
                        par = f"n_inf={n_inf}, self>=q{sq:.2f} ({thr:.2f})"
                        if items.empty:
                            summary += [(f"neighbour/{t}", stratum, par + ", margin any", ag, opts, 0, len(conditions)) for t in ("easy", "hard", "discovery")]
                            continue
                        for mq, mthr in zip(ng["margin_quantiles"], np.quantile(items["margin"], ng["margin_quantiles"])):
                            kept = items[items["margin"] >= mthr]
                            for tier in ("easy", "hard", "discovery"):
                                t = kept[kept["tier"] == tier]
                                if stratum == "main":
                                    piv = (t.pivot_table(index="condition", columns="density_bin", values="target", aggfunc="count", fill_value=0)
                                           .reindex(index=conditions, columns=bins, fill_value=0) if len(t) else pd.DataFrame(0, index=conditions, columns=bins))
                                    cap, emp = int(piv.min(axis=1).min()), int((piv.min(axis=1) == 0).sum())
                                    if excl0 and sq == ng["min_self_corr_quantiles"][0] and mq == ng["margin_quantiles"][1]:
                                        rep += [f"### n_inf={n_inf}, agreement {ag}, self>=q{sq:.2f} ({thr:.2f}), margin>=q{mq:.2f} ({mthr:.2f}), "
                                                f"tier {tier}: main items per condition and bin", "", md_table(piv), ""]
                                else:
                                    per = t.groupby("condition").size().reindex(conditions, fill_value=0)
                                    cap, emp = int(per.min()), int((per == 0).sum())
                                summary.append((f"neighbour/{tier}", stratum, f"{par}, margin>=q{mq:.2f} ({mthr:.2f})", ag, opts, cap, emp))
    rep += ["### F-neighbour diagnostics (10th/50th/90th percentiles over covered rows)", "",
            md_table(pd.DataFrame(diag, columns=["n_inf", "agreement", "condition", "self_reliability", "top_similarity", "median_similarity"])), ""]

    s = pd.DataFrame(summary, columns=["family", "stratum", "parameters", "agreement", "strata", "max_per_cell", "cells_empty"])
    rep += ["## Summary", "", "max_per_cell: main = largest count every cell reaches in every bin; flagged = smallest pooled cell. "
            "cells_empty: cells with no candidate in some bin (main) or at all (flagged).", "", md_table(s), ""]
    # D-023: effect-tercile sampling under the strictest filter that fills it, ahead of any filter without terciles
    order = [(ag, "effect tercile") for ag in splits_of] + [(ag, "no tercile") for ag in splits_of]
    rd = s[(s["family"] == "readout") & (s["stratum"] == "main")]
    rule = []
    for par, grp in rd.groupby("parameters"):
        cap = {(r.agreement, r.strata): int(r.max_per_cell) for r in grp.itertuples()}
        for per_cell in (1, 2, 3, 4, 5, 8, 10, 15, 19, 20):
            pick = next((f"{ag} + {st}" for ag, st in order if cap.get((ag, st), 0) >= per_cell), "none fills")
            rule.append((par, per_cell, pick))
    rep += ["## F-readout filter and strata picked by the D-023 order, by per-cell count", "",
            "Order: " + ", then ".join(f"{ag} with {st}" for ag, st in order) + ".", "",
            md_table(pd.DataFrame(rule, columns=["parameters", "per_cell", "picked"])), ""]

    # ---- baseline rungs: cross-fitted (5 folds by gene) on strata-balanced candidate pools at reference settings
    ref_ag = "d12_d34"
    ref = {"readout": f"R={p2['readout']['R_grid'][1]}, cells condition x label x effect tercile",
           "gene": f"ratio={p2['gene']['ratio_grid'][1]}, tol={p2['gene']['match_log2_tol_grid'][-1]}, cells condition x label",
           "neighbour": f"n_inf={ng['n_inf_grid'][1]}, self>=q{ng['min_self_corr_quantiles'][0]}, margin any, options excl. Phase 0, cells tier x condition"}
    rep += ["## Baseline rungs: cross-fitted Brier skill vs uniform (descriptive)", "",
            f"Candidate pools at reference settings (agreement {ref_ag}; {'; '.join(f'{k}: {v}' for k, v in ref.items())}), "
            "with an equal count in every cell (as in the batch; total up to probe2.baseline_train_max), forecasts out-of-fold with folds split by gene. "
            "Skill = 1 - Brier / Brier(uniform).", ""]
    gid = rows["GeneID"].to_numpy()
    splits = splits_of[ref_ag]
    mods = [m for sp in splits for m in p2["agreement"]["splits"][sp]]
    cr = readout_candidates(rows, M["labels_comb"], M["resp"], conditions, tcols, p2["readout"]["R_grid"][1],
                            agree=agrees(M["labels_comb"], [M[f"labels_{m}"] for m in mods]))
    cr = cr[main_t[cr["row"].to_numpy()]]
    pool = {"readout": (pd.DataFrame({"GeneID": gid[cr["row"]], "condition": cr["condition"].to_numpy(), "label": cr["label"].to_numpy(),
                                      "readout_id": readouts["readout_id"].to_numpy()[cr["readout_col"]], "cell": cr["eff_class"].to_numpy()}),
                        "GeneID")}
    gp = gene_pairs(rows, M["nde_comb"], [M[f"nde_{m}"] for m in mods], p2["gene"]["ratio_grid"][1], p2["gene"]["match_log2_tol_grid"][-1], main_t)
    go_ = orient_pairs(gp, np.random.default_rng(p2["seed"]))
    pool["gene"] = (pd.DataFrame({"GeneID_a": gid[go_["row_a"]], "GeneID_b": gid[go_["row_b"]], "condition": rows["condition"].to_numpy()[go_["row_a"]],
                                  "label": go_["label"].to_numpy(), "cell": 0}), "GeneID_a")
    spec = NeighbourSpec(ng["min_de_grid"][1], float(np.nanquantile(np.min(np.stack([M[f"selfcorrinf_{ng['n_inf_grid'][1]}_{sp}"] for sp in splits]), axis=0),
                                                                    ng["min_self_corr_quantiles"][0])), -np.inf, ng["go_max_genes_grid"][-1], ng["match_log2_tol_grid"][-1])
    it = neighbour_build(cfg, rows, M, ng["n_inf_grid"][1], splits, main_t, ~flagged & not0, go_mats, spec, p2["seed"])
    pool["neighbour"] = (pd.DataFrame({"GeneID": it["GeneID"].to_numpy(), "condition": it["condition"].to_numpy(), "label": it["label"].to_numpy(),
                                       "option_GeneIDs": [[int(gid[o]) for o in os_] for os_ in it["options"]], "cell": it["tier"].to_numpy()}), "GeneID")
    maps = build_maps(read_gene_info(cfg["ncbi"]["gene_info"]))
    sym = {**maps.synonym, **maps.symbol}
    bm = rows.set_index(["GeneID", "condition"])["target_baseMean"].to_dict()
    lines = []
    for d in cutoffs:
        gaf = read_gaf(cfg["go"]["releases"][d]["path"])
        for no_iea in (False, True):
            ctx = Context(genes.set_index("GeneID")[f"log_density_{d}"], bm,
                          gene_terms(filter_annotations(gaf, cfg["go"]["exclude_refs"], exclude_evidence=("IEA",) if no_iea else ()), sym),
                          maps.ensembl, float(np.log10(cfg["density"]["epsilon"])))
            for fam, (df, cluster) in pool.items():
                bal = balanced_pool(df, ["condition", "label", "cell"], p2["baseline_train_max"], p2["seed"])
                y = label_index(fam, bal)
                K = len(LABELS[fam])
                uni = ((np.full((len(bal), K), 1 / K) - np.eye(K)[y]) ** 2).sum(1).mean()
                for name, P in crossfit(fam, ctx, bal, cluster, seed=p2["seed"]).items():
                    if no_iea and name == "fame_only":
                        continue
                    b = ((P - np.eye(K)[y]) ** 2).sum(1).mean()
                    lines.append((d, fam, name + ("_noIEA" if no_iea else ""), len(bal), round(float(b), 4), round(float(uni), 4), round(float(1 - b / uni), 4)))
    rep += [md_table(pd.DataFrame(lines, columns=["cutoff", "family", "rung", "questions", "brier", "brier_uniform", "skill_vs_uniform"])), ""]

    # ---- calls and wall time (per-model workers)
    med = {}
    for path in (Path(cfg["paths"]["runs_root"]) / "p0-20261023-165705-9eb7" / "responses").glob("*.jsonl"):
        secs = [r["seconds"] for r in read_jsonl(path) if not r.get("error")]
        med[path.stem] = float(np.median(secs)) if secs else float("nan")
    workers = {m["name"]: m.get("workers") or cfg["run"]["workers"] for m in cfg["models"] if m.get("enabled")}
    rep += ["## Model calls and wall time", "", f"Median seconds per call in Phase 0: {json.dumps({k: round(v, 1) for k, v in med.items()})}; "
            f"workers per model: {json.dumps(workers)}. Calls = questions x versions x k (opus-5.5-cli) plus sol_fraction of the questions "
            "(sol-6.1-cli); versions = 2 (named, hidden) or 3 with the optional wrong-name control; the two models run concurrently.", ""]
    calls = []
    for n_q in (600, 1290):
        for k in (1, 2, 3):
            for frac in (0.5, 1.0):
                for nv in (2, 3):
                    o, sol = n_q * nv * k, int(n_q * frac) * nv * k
                    h_o = o * med.get("opus-5.5-cli", np.nan) / workers["opus-5.5-cli"] / 3600
                    h_s = sol * med.get("sol-6.1-cli", np.nan) / workers["sol-6.1-cli"] / 3600
                    calls.append((n_q, k, frac, nv, o, sol, o + sol, round(h_o, 1), round(h_s, 1), round(max(h_o, h_s), 1)))
    rep += [md_table(pd.DataFrame(calls, columns=["questions", "k", "sol_fraction", "versions", "opus_calls", "sol_calls", "total_calls",
                                                  "opus_hours", "sol_hours", "wall_hours"])), ""]
    # ---- the pre-registered configuration: the exact selection generation would make (nothing written)
    nulls = [k for k, v in fill_values(cfg).items() if v is None]
    rep += ["## Pre-registered configuration: selection as generation would make it", ""]
    if nulls:
        rep += [f"Not run: config values still null: {nulls}.", ""]
    else:
        S = select_questions(cfg)
        q = S["q"]
        per = q.groupby(["family", "stratum"]).agg(opus=("qid", "size"), sol=("sol", "sum")).reset_index()
        rep += ["Questions per family and stratum (opus-5.5-cli runs all; sol-6.1-cli the sol subset):", "", md_table(per), "",
                f"Agreement filter per family: {json.dumps({f: family_splits(cfg, f)[0] for f in p2['families']})}.",
                f"F-neighbour thresholds per condition: {json.dumps(S['thresholds'], default=lambda x: round(float(x), 3))}.",
                f"Dropped cells: {json.dumps(S['dropped'])}.", ""]
        k, nv = cfg["run"]["samples"], len(S["versions"])
        rows_t = []
        for m in (m for m in cfg["models"] if m.get("enabled")):
            n_q = len(q) if m["name"] != "sol-6.1-cli" else int(q["sol"].sum())
            n_calls = n_q * nv * k
            hours = n_calls * med.get(m["name"], np.nan) / workers[m["name"]] / 3600
            rows_t.append((m["name"], n_q, nv, k, n_calls, round(hours, 1)))
        rep += [md_table(pd.DataFrame(rows_t, columns=["model", "questions", "versions", "k", "calls", "hours"])), ""]
    out = REPO_ROOT / "reports" / "probe2_dryrun.md"
    out.write_text("\n".join(rep))
    return s, out


def fill_values(cfg):
    """Every value generation needs; None means not yet set."""
    p2 = cfg["probe2"]
    return {"run.samples": cfg["run"].get("samples"), "probe2.max_per_gene": p2.get("max_per_gene"),
            "probe2.sol_fraction": p2.get("sol_fraction"), "probe2.combine_samples": p2.get("combine_samples"),
            "probe2.flagged_per_cell": p2.get("flagged_per_cell"), "probe2.agreement.chosen": p2["agreement"].get("chosen"),
            **{f"probe2.{f}.{k}": v for f in ("readout", "gene", "neighbour") for k, v in p2[f].items()
               if not k.endswith(("_grid", "_quantiles")) and k != "top_k_effects"}}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", default=None)
    ap.add_argument("--prereg", default="prereg/probe2.md")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--additional-batch-reason", default=None)
    args = ap.parse_args()
    cfg = load_config(args.config)
    if args.dry_run:
        s, out = dry_run(cfg)
        print(s.to_string(index=False))
        print(f"\nfull tables: {out}\ndry run: nothing written to runs_root or truth_root")
        return
    try:
        prereg = check_prereg(args.prereg)
    except PreregError as exc:
        sys.exit(f"Pre-registration check failed: {exc}")
    missing = [k for k, v in fill_values(cfg).items() if v is None]
    if missing:
        sys.exit(f"FILL values not set in config: {missing}")
    generate(cfg, prereg, args.additional_batch_reason)


if __name__ == "__main__":
    main()
