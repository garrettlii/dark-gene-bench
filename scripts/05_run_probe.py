#!/usr/bin/env python3
"""Ask each enabled model every question in a batch (no data, no tools). Resumable.

Responses go to runs_root/<batch>/responses/<model>.jsonl. Never reads truth_root.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from dgbench.backends import call_with_retries, make_backend, parse_probs  # noqa: E402
from dgbench.batch import batch_dirs, read_jsonl, write_json  # noqa: E402
from dgbench.config import load_config  # noqa: E402
from dgbench.questions import LABELS  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", default=None)
    ap.add_argument("--batch", required=True)
    ap.add_argument("--models", nargs="*", help="model names (default: all enabled)")
    ap.add_argument("--limit", type=int, default=None, help="only the first N questions (smoke test)")
    ap.add_argument("--workers", type=int, default=None)
    args = ap.parse_args()
    cfg = load_config(args.config)
    run_dir, _ = batch_dirs(cfg, args.batch)
    probe2 = (run_dir / "prompts.jsonl").exists()
    if probe2:  # probe v2: named/hidden prompts, per-model call order, k samples per prompt
        prompts = {(p["qid"], p["version"]): p for p in read_jsonl(run_dir / "prompts.jsonl")}
    else:
        questions = read_jsonl(run_dir / "questions.jsonl")
        if not questions:
            sys.exit(f"no questions in {run_dir}")
        if args.limit:
            questions = questions[: args.limit]
    models = [m for m in cfg["models"] if (m["name"] in args.models if args.models else m.get("enabled"))]
    if not models:
        sys.exit("no models selected")
    out_dir = run_dir / "responses"
    out_dir.mkdir(exist_ok=True)

    for mcfg in models:
        workers = args.workers or mcfg.get("workers") or cfg["run"]["workers"]
        backend = make_backend(mcfg, cfg["backends"])
        path = out_dir / f"{mcfg['name']}.jsonl"
        # Records with an infrastructure error (quota, auth, timeout) are retried on the next run.
        if probe2:
            calls = read_jsonl(run_dir / f"calls_{mcfg['name']}.jsonl")
            if args.limit:
                calls = calls[: args.limit]
            done = {(r["qid"], r["version"], r["sample"]) for r in read_jsonl(path) if not r.get("error")}
            todo = [{**prompts[(c["qid"], c["version"])], "sample": c["sample"]} for c in calls
                    if (c["qid"], c["version"], c["sample"]) not in done]
        else:
            done = {r["qid"] for r in read_jsonl(path) if not r.get("error")}
            todo = [q for q in questions if q["qid"] not in done]
        write_json(out_dir / f"{mcfg['name']}.backend.json", backend.describe())
        print(f"{mcfg['name']}: {len(done)} done, {len(todo)} to run")
        lock = threading.Lock()

        def run_one(q: dict) -> dict:
            text, error, secs = call_with_retries(backend, q["prompt"], retries=cfg["run"]["retries"])
            probs = parse_probs(text or "", q.get("labels", LABELS))
            rec = {"qid": q["qid"], "model": mcfg["name"], "probs": probs, "parse_ok": probs is not None,
                   "error": error, "seconds": round(secs, 2), "raw": text,
                   "at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
            if probe2:
                rec.update(version=q["version"], sample=q["sample"])
            return rec

        n_ok = n_fail = 0
        with ThreadPoolExecutor(max_workers=workers) as pool, open(path, "a") as fh:
            futures = [pool.submit(run_one, q) for q in todo]
            for i, fut in enumerate(as_completed(futures), 1):
                rec = fut.result()
                n_ok += rec["parse_ok"]
                n_fail += not rec["parse_ok"]
                with lock:
                    fh.write(json.dumps(rec) + "\n")
                    fh.flush()
                if i % 25 == 0 or i == len(futures):
                    print(f"  {mcfg['name']}: {i}/{len(futures)} (parse failures so far: {n_fail})")


if __name__ == "__main__":
    main()
