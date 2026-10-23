#!/usr/bin/env python3
"""Build the per-gene literature density table.

Default: density.cutoff_date -> data_root/derived/density.parquet (Phase 0).
--cutoff-date D: resolve the PMID cutoff for D and write density_<D>.parquet (one per model cutoff).
--tcell: also write density_tcell_<D>.parquet, counting only papers indexed with the
"T-Lymphocytes" MeSH heading (exploded) entered before D.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from dgbench.batch import sha256_file  # noqa: E402
from dgbench.config import derived_path, load_config  # noqa: E402
from dgbench.density import compute_density, esearch, query_pmids, read_gene2pubmed, resolve_pmid_cutoff  # noqa: E402

TCELL_TERM = '"T-Lymphocytes"[MeSH Terms]'


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", default=None)
    ap.add_argument("--resolve-pmid-cutoff", action="store_true",
                    help="look up the PMID cutoff for density.cutoff_date via NCBI E-utilities")
    ap.add_argument("--no-cutoff", action="store_true", help="count all papers regardless of date")
    ap.add_argument("--cutoff-date", default=None, help="YYYY-MM-DD; writes density_<date>.parquet")
    ap.add_argument("--tcell", action="store_true", help="with --cutoff-date, also build the T-cell MeSH density")
    args = ap.parse_args()
    cfg = load_config(args.config)
    dcfg = cfg["density"]
    api_key = os.environ.get("NCBI_API_KEY")

    cutoff_date = args.cutoff_date or dcfg["cutoff_date"]
    suffix = f"_{cutoff_date}" if args.cutoff_date else ""
    cutoff_info = None
    pmid_cutoff = None if args.cutoff_date else dcfg.get("pmid_cutoff")
    if args.resolve_pmid_cutoff or args.cutoff_date:
        cutoff_info = resolve_pmid_cutoff(cutoff_date, api_key=api_key, stray_gap=dcfg.get("stray_pmid_gap"))
        pmid_cutoff = cutoff_info["pmid_cutoff"]
        print(f"PMID cutoff for {cutoff_date}: {pmid_cutoff} ({cutoff_info})")
        if cutoff_info["truncated"]:
            print("warning: more records that day than returned; cutoff is approximate")
    if pmid_cutoff is None and not args.no_cutoff:
        sys.exit("No PMID cutoff: pass --resolve-pmid-cutoff or --cutoff-date, set density.pmid_cutoff, or pass --no-cutoff")

    g2p = cfg["ncbi"]["gene2pubmed"]
    links = read_gene2pubmed(g2p, tax_id=cfg["ncbi"]["tax_id"])
    table, summary = compute_density(links, max_genes_per_paper=dcfg["max_genes_per_paper"],
                                     pmid_cutoff=pmid_cutoff, epsilon=dcfg["epsilon"])
    out = derived_path(cfg, f"density{suffix}.parquet")
    table.to_parquet(out, index=False)
    meta = {"summary": summary, "cutoff_lookup": cutoff_info, "cutoff_date": cutoff_date,
            "gene2pubmed_sha256": sha256_file(g2p)}

    if args.tcell:
        if not args.cutoff_date:
            sys.exit("--tcell needs --cutoff-date")
        end = dt.date.fromisoformat(cutoff_date) - dt.timedelta(days=1)
        tcell = query_pmids(TCELL_TERM, dt.date(1800, 1, 1), end,
                            search=lambda t, a, b: esearch(t, a, b, api_key))
        # gene-to-paper weights use all of a paper's genes, so the screen filter and fractions match the main density
        tc_table, tc_summary = compute_density(links, max_genes_per_paper=dcfg["max_genes_per_paper"],
                                               pmid_cutoff=pmid_cutoff, epsilon=dcfg["epsilon"], keep_pmids=tcell)
        tc_out = derived_path(cfg, f"density_tcell{suffix}.parquet")
        tc_table.to_parquet(tc_out, index=False)
        meta["tcell"] = {"term": TCELL_TERM, "pmids_before_cutoff": len(tcell), "summary": tc_summary}
        print(f"T-cell MeSH PMIDs before {cutoff_date}: {len(tcell)}; wrote {tc_out}")

    derived_path(cfg, f"density{suffix}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
