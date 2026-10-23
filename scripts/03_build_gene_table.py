#!/usr/bin/env python3
"""Join perturbation QC, gene identifiers and literature density; assign density bins.

Writes data_root/derived/perturbations.parquet and genes.parquet (outside the repo)
and reports/feasibility.md (aggregate counts only).
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from dgbench.config import REPO_ROOT, derived_path, load_config  # noqa: E402
from dgbench.density import assign_bins, attach_density  # noqa: E402
from dgbench.genes import build_maps, map_targets, read_gene_info  # noqa: E402
from dgbench.perturb import perturbation_table, read_obs_var  # noqa: E402


def read_flagged(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {ln.strip() for ln in path.read_text().splitlines() if ln.strip() and not ln.startswith("#")}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", default=None)
    args = ap.parse_args()
    cfg = load_config(args.config)
    cols = cfg["columns"]
    de_path = Path(cols["de_results"]["path"])
    obs, var = read_obs_var(de_path)
    ptab = perturbation_table(obs, cols, min_cells=cfg["perturb"].get("min_cells"))

    gene_info = read_gene_info(cfg["ncbi"]["gene_info"])
    maps = build_maps(gene_info)
    targets = ptab[["target", "target_ensembl"]].drop_duplicates()
    mapping = map_targets(targets["target"], maps, targets["target_ensembl"])
    ptab = ptab.merge(mapping, on=["target", "target_ensembl"], how="left")

    flagged_file = Path(cfg["perturb"]["flagged_genes_file"])
    flagged = read_flagged(flagged_file if flagged_file.is_absolute() else REPO_ROOT / flagged_file)
    ptab["flagged_paper"] = ptab["target"].isin(flagged)

    density = pd.read_parquet(derived_path(cfg, "density.parquet"))
    mapped = ptab[ptab["GeneID"].notna()].copy()
    mapped["GeneID"] = mapped["GeneID"].astype("int64")
    agg = {"target": ("target", "first"), "qc_pass_any": ("qc_pass", "any"),
           "n_conditions_qc": ("qc_pass", "sum"), "flagged_paper": ("flagged_paper", "any")}
    if "effect_size" in mapped:
        agg["effect_size_median"] = ("effect_size", "median")
    if "ontarget_significant" in mapped:
        # covariate only: share of the gene's QC-passing conditions with significant on-target knockdown
        mapped["ontarget_sig_qc"] = mapped["ontarget_significant"].where(mapped["qc_pass"]).astype(float)
        agg["ontarget_sig_rate"] = ("ontarget_sig_qc", "mean")
    genes = mapped.groupby("GeneID").agg(**agg).reset_index()
    genes = genes.merge(gene_info[["GeneID", "Symbol"]].rename(columns={"Symbol": "symbol"}), on="GeneID", how="left")
    genes = attach_density(genes, density, epsilon=cfg["density"]["epsilon"])
    eligible = genes["qc_pass_any"]
    genes["density_bin"] = pd.NA
    zero_bin = cfg["density"].get("zero_bin", False)
    genes.loc[eligible, "density_bin"] = assign_bins(
        genes.loc[eligible, "log_density"], cfg["density"]["n_bins"],
        n_papers=genes.loc[eligible, "n_papers"] if zero_bin else None).to_numpy()
    genes["density_bin"] = genes["density_bin"].astype("Int64")

    ptab.to_parquet(derived_path(cfg, "perturbations.parquet"), index=False)
    genes.to_parquet(derived_path(cfg, "genes.parquet"), index=False)

    readouts = cfg["probe"]["readout_panel"]
    symbols = var[cols["var"]["gene_symbol"]].astype(str) if cols["var"].get("gene_symbol") else var.index.astype(str)
    missing_readouts = [r for r in readouts if r not in set(symbols)]

    lines = [f"# Feasibility report", "", f"Generated {dt.date.today().isoformat()}. Aggregate counts only.", "",
             "## Perturbations", "",
             f"- rows (perturbation x condition): {len(ptab)}",
             f"- unique targets: {ptab['target'].nunique()}",
             f"- conditions: {', '.join(sorted(ptab['condition'].unique()))}", ""]
    lines.append("Target mapping to Entrez GeneID:")
    for method, n in mapping["map_method"].value_counts().items():
        lines.append(f"- {method}: {n}")
    lines += ["", "QC (rows):"]
    for c in [c for c in ptab.columns if c.startswith(("flag_", "require_"))]:
        lines.append(f"- {c}: {int(ptab[c].sum())} true")
    lines.append(f"- qc_pass: {int(ptab['qc_pass'].sum())} of {len(ptab)}")
    for cond, sub in ptab.groupby("condition"):
        lines.append(f"  - {cond}: {int(sub['qc_pass'].sum())} pass")
    lines += ["", f"Genes passing QC in at least one condition: {int(eligible.sum())}",
              f"Flagged (named in the dataset paper): {int(genes['flagged_paper'].sum())}", "",
              "## Literature density by bin (QC-passing genes; bin 0 = least studied)", ""]
    header = "| bin | genes | papers min | papers median | papers max | share with 0 papers | flagged |"
    sep = "|---|---|---|---|---|---|---|"
    if "effect_size_median" in genes:
        header += " effect size median |"
        sep += "---|"
    if "ontarget_sig_rate" in genes:
        header += " on-target KD significant (mean share of QC conditions) |"
        sep += "---|"
    lines += [header, sep]
    for b, sub in genes[eligible].groupby("density_bin"):
        row = (f"| {int(b)} | {len(sub)} | {int(sub['n_papers'].min())} | {sub['n_papers'].median():.0f} | "
               f"{int(sub['n_papers'].max())} | {(sub['n_papers'] == 0).mean():.2f} | {int(sub['flagged_paper'].sum())} |")
        if "effect_size_median" in genes:
            row += f" {sub['effect_size_median'].median():.1f} |"
        if "ontarget_sig_rate" in genes:
            row += f" {sub['ontarget_sig_rate'].mean():.2f} |"
        lines.append(row)
    n_got, n_req = genes.loc[eligible, "density_bin"].nunique(), cfg["density"]["n_bins"] + int(zero_bin)
    if n_got < n_req:
        lines += ["", f"Warning: {n_req} bins requested but ties in density produced {n_got}. "
                  "Many genes share the lowest counts; decide how to bin before pre-registering."]
    lines += ["", f"Readout panel: {len(readouts) - len(missing_readouts)} of {len(readouts)} present"
              + (f"; missing: {', '.join(missing_readouts)}" if missing_readouts else ""), ""]
    report = REPO_ROOT / "reports" / "feasibility.md"
    report.write_text("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
