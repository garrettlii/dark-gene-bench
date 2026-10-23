"""Batch bookkeeping. Questions and model outputs go under runs_root/<batch>;
truth goes under truth_root/<batch>. Existing batches are never overwritten."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import secrets
from pathlib import Path


def new_batch_id(prefix: str) -> str:
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"{prefix}-{stamp}-{secrets.token_hex(2)}"


def batch_dirs(cfg: dict, batch_id: str, create: bool = False) -> tuple[Path, Path]:
    run_dir = Path(cfg["paths"]["runs_root"]) / batch_id
    truth_dir = Path(cfg["paths"]["truth_root"]) / batch_id
    if create:
        for d in (run_dir, truth_dir):
            if d.exists():
                raise FileExistsError(f"{d} already exists; batches are never regenerated in place")
            d.mkdir(parents=True)
    return run_dir, truth_dir


def sha256_file(path: str | Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while block := fh.read(chunk):
            h.update(block)
    return h.hexdigest()


def write_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, default=str) + "\n")


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path) as fh:
        return [json.loads(line) for line in fh if line.strip()]
