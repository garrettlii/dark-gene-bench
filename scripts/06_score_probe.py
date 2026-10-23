#!/usr/bin/env python3
"""Score a Phase 0 batch against its truth file and the pre-registered decision rules.

Writes reports/phase0_<batch>.md (aggregates only, safe to commit) and a per-question
table to runs_root/<batch>/scored_<model>.parquet (private).

Handling, as pre-registered: responses that arrived but could not be parsed are scored
as the uniform forecast and counted; infrastructure errors (no response) are excluded
from scoring and counted separately.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from dgbench.batch import batch_dirs, read_jsonl  # noqa: E402
from dgbench.config import REPO_ROOT, load_config  # noqa: E402
from dgbench.questions import LABELS  # noqa: E402
from dgbench.scoring import by_bin, verdicts  # noqa: E402


def load_responses(path: Path) -> pd.DataFrame:
    latest = {r["qid"]: r for r in read_jsonl(path)}  # last record per question wins
    rows = []
    for r in latest.values():
        probs = r.get("probs") or {}
        rows.append({"qid": r["qid"], "infra_error": bool(r.get("error")) and r.get("raw") is None,
                     "parse_failed": r.get("probs") is None,
                     **{f"p_{lab}": probs.get(lab, 1 / len(LABELS)) for lab in LABELS}})
    return pd.DataFrame(rows)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", default=None)
    ap.add_argument("--batch", required=True)
    ap.add_argument("--n-boot", type=int, default=2000)
    args = ap.parse_args()
    cfg = load_config(args.config)
    run_dir, truth_dir = batch_dirs(cfg, args.batch)
    truth = pd.DataFrame(read_jsonl(truth_dir / "truth.jsonl"))
    manifest = json.loads((truth_dir / "manifest.json").read_text())
    predictions = manifest["predictions"]

    lines = [f"# Phase 0 results: batch {args.batch}", "",
             f"Scored {dt.date.today().isoformat()}. Pre-registration {manifest['prereg']['path']} "
             f"@ {manifest['prereg']['commit'][:10]}. Aggregates only.", "",
             f"Questions: {len(truth)}. Bins: {truth['density_bin'].nunique()} (0 = least studied).", ""]
    for resp_path in sorted((run_dir / "responses").glob("*.jsonl")):
        model = resp_path.stem
        resp = load_responses(resp_path)
        df = truth.merge(resp, on="qid", how="left")
        n_missing = int(df["p_unchanged"].isna().sum())
        infra = df["infra_error"].astype("boolean").fillna(False).astype(bool)
        n_infra = int(infra.sum())
        scored = df[df["p_unchanged"].notna() & ~infra].copy()
        table, slope = by_bin(scored, LABELS, n_boot=args.n_boot, seed=cfg["probe"]["seed"])
        verdict = verdicts(table, slope, predictions)
        scored.to_parquet(run_dir / f"scored_{model}.parquet", index=False)
        lines += [f"## {model}", "",
                  f"Scored {len(scored)}; not yet answered {n_missing}; infrastructure errors {n_infra}; "
                  f"parse failures scored as uniform {int(scored['parse_failed'].sum())}.", "",
                  "| bin | questions | genes | Brier skill | 95% CI | accuracy | ECE | parse fail |",
                  "|---|---|---|---|---|---|---|---|"]
        for r in table.itertuples(index=False):
            lines.append(f"| {r.density_bin} | {r.n_questions} | {r.n_genes} | {r.skill:.3f} | "
                         f"[{r.ci_low:.3f}, {r.ci_high:.3f}] | {r.accuracy:.3f} | {r.ece:.3f} | {r.parse_fail_rate:.3f} |")
        lines += ["", f"Slope of skill per bin: {slope['slope']:.4f} [{slope['ci_low']:.4f}, {slope['ci_high']:.4f}]", "",
                  "Pre-registered checks:"]
        lines += [f"- {k}: {'pass' if v else 'FAIL'}" for k, v in verdict.items()]
        lines.append("")
    out = REPO_ROOT / "reports" / f"phase0_{args.batch}.md"
    out.write_text("\n".join(lines))
    print("\n".join(lines))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
