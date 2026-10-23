"""Small synthetic stand-ins for the NCBI files and the DE results file."""
from __future__ import annotations

import gzip
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd
import pytest

GENE_INFO_HEADER = ("#tax_id\tGeneID\tSymbol\tLocusTag\tSynonyms\tdbXrefs\tchromosome\tmap_location\tdescription\t"
                    "type_of_gene\tSymbol_from_nomenclature_authority\tFull_name_from_nomenclature_authority\t"
                    "Nomenclature_status\tOther_designations\tModification_date\tFeature_type")


def _gi_row(gid, sym, syns="-", ens=None):
    xrefs = f"HGNC:HGNC:{gid}" + (f"|Ensembl:{ens}" if ens else "")
    return f"9606\t{gid}\t{sym}\t-\t{syns}\t{xrefs}\t1\t1p1\tdesc\tprotein-coding\t{sym}\tname\tO\t-\t20260101\t-"


@pytest.fixture
def gene_info_path(tmp_path: Path) -> Path:
    rows = [
        _gi_row(1, "AAA1", "OLDA|SHARED", "ENSG00000000001"),
        _gi_row(2, "BBB2", "OLDB|SHARED", "ENSG00000000002"),
        _gi_row(3, "CCC3", "-", "ENSG00000000003"),
        _gi_row(4, "DDD4", "-"),
        _gi_row(5, "EEE5", "-"),
        _gi_row(6, "FFF6", "-"),
    ]
    path = tmp_path / "Homo_sapiens.gene_info.gz"
    with gzip.open(path, "wt") as fh:
        fh.write(GENE_INFO_HEADER + "\n" + "\n".join(rows) + "\n")
    return path


@pytest.fixture
def gene2pubmed_path(tmp_path: Path) -> Path:
    links = [
        (9606, 1, 100), (9606, 2, 100),            # paper 100: two genes -> 0.5 each
        (9606, 1, 101),                             # paper 101: gene 1 only
        (9606, 3, 102),                             # paper 102: gene 3 only
        (10090, 3, 103),                            # mouse link, ignored
        (9606, 1, 900), (9606, 2, 900), (9606, 3, 900), (9606, 4, 900),  # 4-gene "screen"
        (9606, 5, 5000),                            # after the cutoff in tests
    ]
    path = tmp_path / "gene2pubmed.gz"
    with gzip.open(path, "wt") as fh:
        fh.write("#tax_id\tGeneID\tPubMed_ID\n")
        for t, g, p in links:
            fh.write(f"{t}\t{g}\t{p}\n")
    return path


@pytest.fixture
def de_h5ad(tmp_path: Path) -> Path:
    targets = ["AAA1", "BBB2", "CCC3", "OLDA", "DDD4", "EEE5"]
    conds = ["Rest", "Stim48hr"]
    obs = pd.DataFrame(
        [{"target_gene": t, "culture_condition": c,
          "neighboring_gene_KD": t == "DDD4", "distal_offtarget_flag": False,
          "low_target_gex": False, "keep_test_genes": t != "EEE5", "n_de": i,
          "ontarget_significant": c == "Rest"}
         for i, (t, c) in enumerate((t, c) for t in targets for c in conds)]
    )
    obs.index = [f"p{i}" for i in range(len(obs))]
    var = pd.DataFrame(index=["IL2", "IFNG", "AAA1", "TNF"])
    rng = np.random.default_rng(0)
    lfc = rng.normal(0, 0.5, size=(len(obs), len(var))).astype("float32")
    padj = rng.uniform(0, 1, size=(len(obs), len(var))).astype("float32")
    adata = ad.AnnData(X=np.zeros((len(obs), len(var)), dtype="float32"), obs=obs, var=var,
                       layers={"lfc": lfc, "padj": padj})
    path = tmp_path / "de.h5ad"
    adata.write_h5ad(path)
    return path


@pytest.fixture
def columns_cfg() -> dict:
    return {
        "obs": {"target_gene": "target_gene", "target_gene_id": None, "condition": "culture_condition",
                "n_cells": None, "effect_size": "n_de", "ontarget_significant": "ontarget_significant",
                "flags_exclude_true": ["neighboring_gene_KD", "distal_offtarget_flag", "low_target_gex"],
                "flags_require_true": ["keep_test_genes"]},
        "var": {"gene_symbol": None},
        "layers": {"lfc": "lfc", "padj": "padj", "se": None},
    }
