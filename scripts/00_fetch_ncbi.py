#!/usr/bin/env python3
"""Download NCBI gene2pubmed and Homo_sapiens.gene_info into data_root/raw/ncbi, with a checksum manifest."""
from __future__ import annotations

import argparse
import datetime as dt
import shutil
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from dgbench.batch import sha256_file  # noqa: E402
from dgbench.config import load_config  # noqa: E402

BASE = "https://ftp.ncbi.nlm.nih.gov/gene/DATA"
FILES = {
    "gene2pubmed.gz": f"{BASE}/gene2pubmed.gz",
    "Homo_sapiens.gene_info.gz": f"{BASE}/GENE_INFO/Mammalia/Homo_sapiens.gene_info.gz",
}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", default=None)
    ap.add_argument("--force", action="store_true", help="re-download files that already exist")
    args = ap.parse_args()
    cfg = load_config(args.config)
    out = Path(cfg["paths"]["data_root"]) / "raw" / "ncbi"
    out.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    lines = []
    for name, url in FILES.items():
        dest = out / name
        if dest.exists() and not args.force:
            print(f"exists, skipping: {dest}")
        else:
            print(f"downloading {url}")
            tmp = dest.with_suffix(dest.suffix + ".part")
            with urllib.request.urlopen(url, timeout=120) as resp, open(tmp, "wb") as fh:
                shutil.copyfileobj(resp, fh, length=1 << 20)
            tmp.replace(dest)
        lines.append(f"{stamp}\t{name}\t{sha256_file(dest)}\t{url}")
    with open(out / "MANIFEST.tsv", "a") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"checksums appended to {out / 'MANIFEST.tsv'}")


if __name__ == "__main__":
    main()
