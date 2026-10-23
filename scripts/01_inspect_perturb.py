#!/usr/bin/env python3
"""Print the structure of the differential-expression .h5ad so config/columns.yaml can be filled in.

Output stays on screen; nothing is written to the repository.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from dgbench.config import load_config  # noqa: E402
from dgbench.perturb import describe  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", default=None)
    ap.add_argument("--path", default=None, help="defaults to columns.yaml de_results.path")
    args = ap.parse_args()
    cfg = load_config(args.config)
    path = Path(args.path or cfg["columns"]["de_results"]["path"]).expanduser()
    if not path.exists():
        sys.exit(f"not found: {path}\nDownload the file (docs/DATA.md) and set de_results.path in config/columns.yaml")
    print(describe(path))
    print("\nNext: fill config/columns.yaml (obs.target_gene, obs.condition, layers.lfc, layers.padj, flags),")
    print("and make probe.condition_text keys in config/default.yaml match the condition labels above.")


if __name__ == "__main__":
    main()
