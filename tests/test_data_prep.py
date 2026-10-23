import numpy as np
import pandas as pd
import pytest

from dgbench.config import resolve_paths
from dgbench.density import assign_bins, attach_density, compute_density, read_gene2pubmed
from dgbench.genes import build_maps, map_targets, read_gene_info
from dgbench.perturb import describe, perturbation_table, read_columns, read_obs_var, readout_long


def test_density_fractional_counts_cutoff_and_screen_filter(gene2pubmed_path):
    links = read_gene2pubmed(gene2pubmed_path, chunksize=3)
    assert set(links["GeneID"]) == {1, 2, 3, 4, 5}  # mouse row dropped
    table, summary = compute_density(links, max_genes_per_paper=3, pmid_cutoff=1000, epsilon=0.01)
    t = table.set_index("GeneID")
    assert t.loc[1, "n_papers"] == 2 and t.loc[1, "frac_papers"] == pytest.approx(1.5)
    assert t.loc[2, "frac_papers"] == pytest.approx(0.5)
    assert t.loc[3, "frac_papers"] == pytest.approx(1.0)
    assert 4 not in t.index  # only linked by the 4-gene screen
    assert 5 not in t.index  # only paper is after the cutoff
    assert summary["papers_dropped_high_throughput"] == 1


def test_attach_density_and_bins():
    genes = pd.DataFrame({"GeneID": [1, 2, 3, 4, 5, 6]})
    dens = pd.DataFrame({"GeneID": [1, 2, 3], "n_papers": [10, 5, 1], "frac_papers": [8.0, 3.0, 0.5],
                         "log_density": np.log10(np.array([8.0, 3.0, 0.5]) + 0.01)})
    out = attach_density(genes, dens, epsilon=0.01)
    assert (out.loc[out["GeneID"] > 3, "n_papers"] == 0).all()
    bins = assign_bins(out["log_density"], n_bins=2)
    assert bins[out["GeneID"] == 1].item() == 1
    assert bins[out["GeneID"].isin([4, 5, 6])].nunique() == 1  # tied zeros share a bin


def test_gene_mapping(gene_info_path):
    maps = build_maps(read_gene_info(gene_info_path))
    m = map_targets(["AAA1", "ccc3", "OLDA", "SHARED", "ZZZ9", "XYZ"], maps,
                    [None, None, None, None, None, "ENSG00000000002.7"]).set_index("target")
    assert m.loc["AAA1", "GeneID"] == 1 and m.loc["AAA1", "map_method"] == "symbol"
    assert m.loc["ccc3", "map_method"] == "symbol_case"
    assert m.loc["OLDA", "GeneID"] == 1 and m.loc["OLDA", "map_method"] == "synonym"
    assert m.loc["SHARED", "map_method"] == "unmapped"  # ambiguous synonym
    assert m.loc["ZZZ9", "map_method"] == "unmapped"
    assert m.loc["XYZ", "GeneID"] == 2 and m.loc["XYZ", "map_method"] == "ensembl"


def test_perturbation_table_qc(de_h5ad, columns_cfg):
    obs, _ = read_obs_var(de_h5ad)
    pt = perturbation_table(obs, columns_cfg)
    by_target = pt.groupby("target")["qc_pass"].all()
    assert not by_target["DDD4"]  # neighbor knockdown flag
    assert not by_target["EEE5"]  # fails keep_test_genes
    assert by_target["AAA1"]
    assert "effect_size" in pt


def test_missing_column_raises(de_h5ad, columns_cfg):
    obs, _ = read_obs_var(de_h5ad)
    bad = {**columns_cfg, "obs": {**columns_cfg["obs"], "condition": "nope"}}
    with pytest.raises(KeyError):
        perturbation_table(obs, bad)


def test_read_columns_preserves_requested_order(de_h5ad):
    import anndata as ad
    adata = ad.read_h5ad(de_h5ad)
    got = read_columns(de_h5ad, "lfc", [3, 0, 2])
    np.testing.assert_allclose(got, adata.layers["lfc"][:, [3, 0, 2]])


def test_readout_long(de_h5ad, columns_cfg):
    import anndata as ad
    adata = ad.read_h5ad(de_h5ad)
    _, var = read_obs_var(de_h5ad)
    long, missing = readout_long(de_h5ad, var, columns_cfg, ["TNF", "IL2", "NOTAGENE"])
    assert missing == ["NOTAGENE"]
    row = long[(long["obs_index"] == 4) & (long["readout"] == "TNF")].iloc[0]
    assert row["lfc"] == pytest.approx(float(adata.layers["lfc"][4, 3]))
    assert row["padj"] == pytest.approx(float(adata.layers["padj"][4, 3]))


def test_describe_lists_layers(de_h5ad):
    text = describe(de_h5ad)
    assert "layers/lfc" in text and "culture_condition" in text


def test_paths_inside_repo_rejected(tmp_path):
    from dgbench.config import REPO_ROOT
    cfg = {"paths": {"data_root": str(REPO_ROOT / "data"), "runs_root": str(tmp_path / "r"),
                     "truth_root": str(tmp_path / "t")}}
    with pytest.raises(ValueError):
        resolve_paths(cfg)
    ok = {"paths": {"data_root": str(tmp_path / "d"), "runs_root": str(tmp_path / "r"),
                    "truth_root": str(tmp_path / "t")}, "x": "{runs_root}/a {prompt}"}
    out = resolve_paths(ok)
    assert out["x"].endswith("/a {prompt}")
