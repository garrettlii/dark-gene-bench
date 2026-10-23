#!/usr/bin/env python3
"""Generate a Phase 0 (prior-only probe) batch.

Refuses to run unless the pre-registration file is filled in, committed and pushed.
Questions go to runs_root/<batch>/questions.jsonl, answers to truth_root/<batch>/truth.jsonl.
Prints aggregate counts only. --dry-run builds the question set in memory, prints the
same counts, and writes nothing.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from dgbench.batch import batch_dirs, new_batch_id, read_jsonl, sha256_file, write_json  # noqa: E402
from dgbench.config import config_hash, derived_path, load_config  # noqa: E402
from dgbench.perturb import read_obs_var, readout_long  # noqa: E402
from dgbench.prereg import PreregError, check_prereg  # noqa: E402
from dgbench.questions import LABELS, build_prompt, label_effects, sample_questions  # noqa: E402


def build_candidates(cfg: dict) -> tuple[pd.DataFrame, list[str]]:
    pcfg, cols = cfg["probe"], cfg["columns"]
    ptab = pd.read_parquet(derived_path(cfg, "perturbations.parquet"))
    genes = pd.read_parquet(derived_path(cfg, "genes.parquet"))
    _, var = read_obs_var(cols["de_results"]["path"])
    long, missing = readout_long(cols["de_results"]["path"], var, cols, pcfg["readout_panel"])

    keep = ptab["qc_pass"] & ptab["GeneID"].notna() & ptab["condition"].isin(pcfg["condition_text"].keys())
    ptab = ptab[keep].copy()
    ptab["GeneID"] = ptab["GeneID"].astype("int64")
    cand = long.merge(ptab[["obs_index", "GeneID", "target", "condition"]], on="obs_index", how="inner")
    cand = cand.merge(genes[["GeneID", "symbol", "density_bin", "log_density", "n_papers", "flagged_paper"]],
                      on="GeneID", how="inner")
    cand = cand[cand["density_bin"].notna()]
    if pcfg.get("exclude_flagged_genes", True):
        cand = cand[~cand["flagged_paper"]]
    cand = cand[(cand["readout"] != cand["target"]) & (cand["readout"] != cand["symbol"])]
    t = pcfg["truth"]
    cand["label"] = label_effects(cand["lfc"].to_numpy(), cand["padj"].to_numpy(), t["alpha"], t["lfc_min"],
                                  t["none_padj_min"], t["none_lfc_max"])
    cand = cand[cand["label"].notna()].copy()
    cand["density_bin"] = cand["density_bin"].astype("int64")
    return cand.reset_index(drop=True), missing


def counts_table(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    tab = df.pivot_table(index="density_bin", columns="label", values="GeneID", aggfunc="count", fill_value=0)
    tab["genes"] = df.groupby("density_bin")["GeneID"].nunique()
    return tab


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", default=None)
    ap.add_argument("--prereg", default="prereg/phase0_prior_probe.md")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--additional-batch-reason", default=None,
                    help="required to generate a second batch under the same pre-registration commit")
    args = ap.parse_args()
    cfg = load_config(args.config)
    pcfg = cfg["probe"]

    prereg = None
    if not args.dry_run:
        try:
            prereg = check_prereg(args.prereg)
        except PreregError as exc:
            sys.exit(f"Pre-registration check failed: {exc}")
        print(f"pre-registration OK: {prereg['path']} @ {prereg['commit'][:10]} ({prereg['committed_at']})")
        ledger = Path(cfg["paths"]["truth_root"]) / "ledger.jsonl"
        earlier = [e for e in read_jsonl(ledger)
                   if e["prereg_path"] == prereg["path"] and e["prereg_commit"] == prereg["commit"]]
        if earlier and not args.additional_batch_reason:
            sys.exit(f"{len(earlier)} batch(es) already generated under this pre-registration "
                     f"({', '.join(e['batch_id'] for e in earlier)}). Pass --additional-batch-reason "
                     "to record why another is needed, or write a new pre-registration.")

    cand, missing = build_candidates(cfg)
    print(f"candidate questions: {len(cand)}; readouts missing from data: {missing or 'none'}")
    print("candidates by bin and label:\n" + counts_table(cand).to_string())

    rng = np.random.default_rng(pcfg["seed"])
    picked = sample_questions(cand, pcfg["questions_per_bin"], pcfg["max_questions_per_gene"], rng,
                              balance=pcfg.get("label_balance", True))
    per_bin = picked.groupby("density_bin").size()
    short = {int(b): int(n) for b, n in per_bin.items() if n < (pcfg["questions_per_bin"] // len(LABELS)) * len(LABELS)}
    print("selected by bin and label:\n" + counts_table(picked).to_string())
    if short:
        print(f"warning: bins below quota: {short}")
    if args.dry_run:
        print("dry run: nothing written")
        return

    batch_id = new_batch_id("p0")
    run_dir, truth_dir = batch_dirs(cfg, batch_id, create=True)
    balanced = pcfg.get("label_balance", True)
    with open(run_dir / "questions.jsonl", "w") as fq, open(truth_dir / "truth.jsonl", "w") as ft:
        for row in picked.itertuples(index=False):
            prompt = build_prompt(row.symbol, row.readout, pcfg["condition_text"][row.condition], balanced)
            fq.write(json.dumps({"qid": row.qid, "family": "F1", "prompt": prompt}) + "\n")
            ft.write(json.dumps({"qid": row.qid, "GeneID": int(row.GeneID), "symbol": row.symbol,
                                 "readout": row.readout, "condition": row.condition, "label": row.label,
                                 "density_bin": int(row.density_bin), "log_density": float(row.log_density),
                                 "n_papers": int(row.n_papers)}) + "\n")
    manifest = {
        "batch_id": batch_id, "created_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "phase": 0, "family": "F1", "prereg": {k: v for k, v in prereg.items() if k != "predictions"},
        "predictions": prereg["predictions"], "config_hash": config_hash(cfg), "config": cfg,
        "de_results_sha256": sha256_file(cfg["columns"]["de_results"]["path"]),
        "n_questions": len(picked), "per_bin": {int(k): int(v) for k, v in per_bin.items()},
        "bins_below_quota": short, "readouts_missing": missing,
    }
    write_json(run_dir / "manifest.json", manifest)
    ledger = Path(cfg["paths"]["truth_root"]) / "ledger.jsonl"
    with open(ledger, "a") as fh:
        fh.write(json.dumps({"batch_id": batch_id, "created_at": manifest["created_at"],
                             "prereg_path": prereg["path"], "prereg_commit": prereg["commit"],
                             "additional_batch_reason": args.additional_batch_reason}) + "\n")
    write_json(truth_dir / "manifest.json", manifest)
    print(f"batch {batch_id}: {len(picked)} questions\n  questions: {run_dir}\n  truth: {truth_dir}")


if __name__ == "__main__":
    main()
