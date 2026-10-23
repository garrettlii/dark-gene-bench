#!/usr/bin/env python3
"""Build the per-gene literature density table (data_root/derived/density.parquet)."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from dgbench.batch import sha256_file  # noqa: E402
from dgbench.config import derived_path, load_config  # noqa: E402
from dgbench.density import compute_density, read_gene2pubmed, resolve_pmid_cutoff  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", default=None)
    ap.add_argument("--resolve-pmid-cutoff", action="store_true",
                    help="look up the PMID cutoff for density.cutoff_date via NCBI E-utilities")
    ap.add_argument("--no-cutoff", action="store_true", help="count all papers regardless of date")
    args = ap.parse_args()
    cfg = load_config(args.config)
    dcfg = cfg["density"]

    cutoff_info = None
    pmid_cutoff = dcfg.get("pmid_cutoff")
    if args.resolve_pmid_cutoff:
        cutoff_info = resolve_pmid_cutoff(dcfg["cutoff_date"], api_key=os.environ.get("NCBI_API_KEY"))
        pmid_cutoff = cutoff_info["pmid_cutoff"]
        print(f"PMID cutoff for {dcfg['cutoff_date']}: {pmid_cutoff} ({cutoff_info})")
        if cutoff_info["truncated"]:
            print("warning: more records that day than returned; cutoff is approximate")
    if pmid_cutoff is None and not args.no_cutoff:
        sys.exit("No PMID cutoff: pass --resolve-pmid-cutoff, set density.pmid_cutoff, or pass --no-cutoff")

    g2p = cfg["ncbi"]["gene2pubmed"]
    links = read_gene2pubmed(g2p, tax_id=cfg["ncbi"]["tax_id"])
    table, summary = compute_density(links, max_genes_per_paper=dcfg["max_genes_per_paper"],
                                     pmid_cutoff=pmid_cutoff, epsilon=dcfg["epsilon"])
    out = derived_path(cfg, "density.parquet")
    table.to_parquet(out, index=False)
    meta = {"summary": summary, "cutoff_lookup": cutoff_info, "cutoff_date": dcfg["cutoff_date"],
            "gene2pubmed_sha256": sha256_file(g2p)}
    derived_path(cfg, "density_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
