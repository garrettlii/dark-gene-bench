import datetime as dt
import gzip

import numpy as np
import pandas as pd
import pytest

from dgbench.density import compute_density, query_pmids, read_gene2pubmed
from dgbench.donors import LAB_DOWN, LAB_NONE, LAB_UNCHANGED, LAB_UP, label_codes, paired_row_corr, row_corr
from dgbench.go import descendants, filter_annotations, gene_terms, pairwise, read_gaf, read_obo_parents
from dgbench.probe2 import (HIDDEN, NeighbourSpec, agrees, build_prompts, effect_terciles, gene_pairs, neighbour_items,
                            readout_candidates, run_order, stratified_sample)
from dgbench.scoring2 import (argmax_forecast, auc, brier, cluster_boot, combine_samples, completeness, fit_conditional_logit,
                              fit_softmax, murphy, predict_conditional_logit, predict_softmax, slope)


# ---------------------------------------------------------------- density per cutoff

def test_keep_pmids_restricts_counts_but_not_weights(gene2pubmed_path):
    links = read_gene2pubmed(gene2pubmed_path)
    full, _ = compute_density(links, max_genes_per_paper=3, pmid_cutoff=1000)
    sub, summary = compute_density(links, max_genes_per_paper=3, pmid_cutoff=1000, keep_pmids={100})
    assert set(sub["GeneID"]) == {1, 2}  # paper 100 links genes 1 and 2
    assert sub.set_index("GeneID").loc[1, "frac_papers"] == pytest.approx(0.5)  # weight still 1/2
    assert summary["papers_counted"] == 1 and full["n_papers"].sum() > sub["n_papers"].sum()


def test_query_pmids_bisects_ranges_over_the_cap():
    day_ids = {dt.date(2020, 1, d): list(range(d * 10, d * 10 + 4)) for d in range(1, 9)}  # 4 records per day

    def fake(term, a, b):
        a, b = dt.datetime.strptime(a, "%Y/%m/%d").date(), dt.datetime.strptime(b, "%Y/%m/%d").date()
        ids = [i for d, v in day_ids.items() if a <= d <= b for i in v]
        return len(ids), ids[:5]  # server caps the returned list

    got = query_pmids("x", dt.date(2020, 1, 1), dt.date(2020, 1, 8), search=fake, cap=5)
    assert got == {i for v in day_ids.values() for i in v}


# ---------------------------------------------------------------- donors

def test_label_codes_and_correlations():
    lfc = np.array([[-1.0, 0.0, 1.0, 0.3]])
    padj = np.array([[0.01, 0.9, 0.01, 0.2]])
    codes = label_codes(lfc, padj, alpha=0.05, lfc_min=0.25, none_padj_min=0.5, none_lfc_max=0.1)
    assert codes.tolist() == [[LAB_DOWN, LAB_UNCHANGED, LAB_UP, LAB_NONE]]
    a = np.array([[1, 2, 3, 4.0], [4, 3, 2, 1.0]])
    assert row_corr(a)[0, 1] == pytest.approx(-1)
    assert paired_row_corr(a, a * 2 + 1) == pytest.approx([1, 1])


# ---------------------------------------------------------------- GO

def test_go_filters_dates_refs_and_complex(tmp_path):
    gaf = tmp_path / "g.gaf.gz"
    lines = ["!gaf-version: 2.2",
             "\t".join(["UniProtKB", "P1", "AAA1", "enables", "GO:1", "PMID:1", "IDA", "", "F", "", "", "protein", "taxon:9606", "20250101", "X"]),
             "\t".join(["UniProtKB", "P1", "AAA1", "part_of", "GO:3", "PMID:2", "IDA", "", "C", "", "", "protein", "taxon:9606", "20250101", "X"]),
             "\t".join(["UniProtKB", "P2", "BBB2", "enables", "GO:1", "PMID:42664972", "IDA", "", "F", "", "", "protein", "taxon:9606", "20250101", "X"]),
             "\t".join(["UniProtKB", "P2", "BBB2", "part_of", "GO:3", "PMID:3", "IEA", "", "C", "", "", "protein", "taxon:9606", "20261009", "X"]),
             "\t".join(["UniProtKB", "P2", "BBB2", "NOT|enables", "GO:2", "PMID:4", "IDA", "", "F", "", "", "protein", "taxon:9606", "20250101", "X"])]
    with gzip.open(gaf, "wt") as fh:
        fh.write("\n".join(lines) + "\n")
    df = read_gaf(gaf)
    assert len(df) == 4  # NOT annotation dropped
    kept = filter_annotations(df, ["PMID:42664972"])
    terms = gene_terms(kept, {"AAA1": 1, "BBB2": 2})
    assert terms == {1: frozenset({"GO:1", "GO:3"}), 2: frozenset({"GO:3"})}  # BBB2's GO:1 cites the dataset paper
    assert gene_terms(filter_annotations(df, ["PMID:42664972"], exclude_evidence=("IEA",)), {"AAA1": 1, "BBB2": 2}) == {1: frozenset({"GO:1", "GO:3"})}
    assert 2 not in gene_terms(filter_annotations(df, ["PMID:42664972"], cutoff_date="2026-05-01"), {"AAA1": 1, "BBB2": 2})
    obo = tmp_path / "go.obo"
    obo.write_text("[Term]\nid: GO:0032991\n\n[Term]\nid: GO:3\nis_a: GO:0032991 ! complex\n\n[Term]\nid: GO:4\nrelationship: part_of GO:3 ! x\n")
    assert descendants("GO:0032991", read_obo_parents(obo)) == {"GO:3", "GO:4"}
    jac, share = pairwise([1, 2, 3], {1: frozenset({"a", "b"}), 2: frozenset({"b", "c"}), 3: frozenset()})
    assert jac[0, 1] == pytest.approx(1 / 3) and share[0, 1] and not share[0, 2]
    _, share_small = pairwise([1, 2], {1: frozenset({"a", "b"}), 2: frozenset({"b", "c"})}, restrict={"a"})
    assert not share_small[0, 1]


# ---------------------------------------------------------------- F-readout

def _rows(n, conditions=("Rest",), bins=None):
    return pd.DataFrame({"condition": [conditions[i % len(conditions)] for i in range(n)],
                         "density_bin": bins if bins is not None else [i % 2 for i in range(n)],
                         "GeneID": np.arange(n) + 100, "target_baseMean": np.full(n, 50.0),
                         "n_downstream": np.arange(n) * 10 + 30, "eff_class": np.zeros(n, dtype=np.int8)})


def test_readout_candidates_rules():
    rows = _rows(2)
    labels = np.array([[LAB_DOWN, LAB_UNCHANGED, LAB_UNCHANGED, LAB_UP],
                       [LAB_UP, LAB_UNCHANGED, LAB_NONE, LAB_DOWN]], dtype=np.int8)
    resp = np.array([[10, 30, 2, 5]])
    c = readout_candidates(rows, labels, resp, ["Rest"], target_cols=np.array([3, -1]), R=20)
    got = set(zip(c["row"], c["readout_col"], c["label"]))
    assert (0, 3, "increased") not in got  # the target's own readout is never used
    assert (0, 2, "unchanged") not in got  # unchanged readout responds to fewer than R perturbations
    assert {(0, 0, "decreased"), (0, 1, "unchanged"), (1, 0, "increased"), (1, 1, "unchanged"), (1, 3, "decreased")} == got
    agree = np.ones_like(labels, dtype=bool)
    agree[1, 0] = False
    c2 = readout_candidates(rows, labels, resp, ["Rest"], np.array([3, -1]), 20, agree=agree)
    assert (1, 0) not in set(zip(c2["row"], c2["readout_col"]))
    assert set(c["eff_class"]) == {0}


def test_effect_terciles_within_condition():
    rows = pd.DataFrame({"condition": ["Rest"] * 6 + ["Stim8hr"] * 3, "n_downstream": [10, 20, 30, 40, 50, 60, 5, 500, 50]})
    assert effect_terciles(rows).tolist() == [0, 0, 1, 1, 2, 2, 0, 2, 1]


def test_agrees_needs_every_half():
    comb = np.array([[LAB_UP, LAB_DOWN]], dtype=np.int8)
    assert agrees(comb, [np.array([[LAB_UP, LAB_DOWN]]), np.array([[LAB_UP, LAB_NONE]])]).tolist() == [[True, False]]


# ---------------------------------------------------------------- F-gene

def test_gene_pairs_ratio_match_and_order():
    rows = _rows(4, bins=[0, 0, 0, 1])
    rows["target_baseMean"] = [50, 60, 400, 55]
    nde = np.array([100, 30, 10, 300])
    half_ok, half_flip = np.array([90, 40, 5, 200]), np.array([20, 40, 5, 200])
    p = gene_pairs(rows, nde, [half_ok], ratio=2, log2_tol=1.0, eligible=np.ones(4, bool))
    assert set(zip(p["row_a"], p["row_b"])) == {(0, 1)}  # row 2: expression too far; row 3: other bin
    assert p["larger"].tolist() == [0]
    assert gene_pairs(rows, nde, [half_flip], 2, 1.0, np.ones(4, bool)).empty  # order disagrees in a half
    rows3 = _rows(3, bins=[0, 0, 0])
    one = gene_pairs(rows3, np.array([100, 30, 10]), [np.array([100, 30, 10])], 2, 1.0, np.ones(3, bool), one_of=np.array([True, False, False]))
    assert set(zip(one["row_a"], one["row_b"])) == {(0, 1), (0, 2)}  # exactly one flagged gene per pair


# ---------------------------------------------------------------- F-neighbour

def test_neighbour_items_tiers_margin_and_halves():
    n = 12
    rows = _rows(n, bins=[0] * n)
    rng = np.random.default_rng(0)
    corr = np.full((n, n), 0.0)
    corr[0, 1] = corr[1, 0] = 0.9  # row 1 is row 0's neighbour
    corr[0, 2:] = corr[2:, 0] = np.linspace(-0.5, 0.1, n - 2)
    np.fill_diagonal(corr, 1)
    jac = np.zeros((n, n))
    no = np.zeros((n, n), bool)
    spec = NeighbourSpec(min_de=10, min_self_corr=0.2, margin=0.3, go_max_genes=50, match_log2_tol=1.0)
    targets = np.zeros(n, bool)
    targets[0] = True
    args = (rows, np.arange(n), corr, [corr], np.full(n, 50), np.full(n, 0.5), targets, np.ones(n, bool), jac, no, no, spec)
    items = neighbour_items(*args, rng)
    assert set(items["tier"]) == {"easy", "hard", "discovery"}
    for opts, lab in zip(items["options"], items["label"]):
        assert opts["ABCD".index(lab)] == 1
        assert all(corr[0, o] < np.median(np.delete(corr[0], 0)) for o in opts if o != 1)
    shared = no.copy()
    shared[0, 1] = True
    assert "discovery" not in set(neighbour_items(*args[:9], shared, no, spec, rng)["tier"])
    flipped = corr.copy()
    flipped[0, 1] = -1
    assert neighbour_items(*args[:3], [flipped], *args[4:], rng).empty  # correct option not first in a half
    assert neighbour_items(rows, np.arange(n), corr, [corr], np.full(n, 50), np.full(n, 0.1), targets, np.ones(n, bool),
                           jac, no, no, spec, rng).empty  # unreliable signatures


# ---------------------------------------------------------------- sampling, prompts, order

def test_stratified_sample_equal_per_bin_and_drops_cells():
    cand = pd.DataFrame({"GeneID": [1, 2, 3, 4, 5, 6, 7], "density_bin": [0, 0, 1, 1, 0, 1, 0],
                         "condition": ["Rest"] * 4 + ["Stim8hr"] * 3, "label": ["up"] * 7})
    sel, dropped = stratified_sample(cand, ["condition", "label"], per_cell=2, max_per_gene=1, rng=np.random.default_rng(0))
    assert dropped == [("Stim8hr", "up")]  # only one bin-1 candidate
    assert sel.groupby("density_bin").size().tolist() == [2, 2]
    pairs = pd.DataFrame({"GeneID": [(1, 2), (1, 3), (4, 5), (6, 7)], "density_bin": [0, 0, 1, 1], "condition": ["R"] * 4, "label": ["A"] * 4})
    sel, _ = stratified_sample(pairs, ["condition", "label"], per_cell=1, max_per_gene=1, rng=np.random.default_rng(1))
    assert len(sel) == 2


def test_prompts_differ_only_in_gene_lines():
    for fam, genes in [("readout", {"target": "GENEX", "readout": "IL2"}), ("gene", {"gene_a": "GENEX", "gene_b": "GENEY"}),
                       ("neighbour", {"target": "GENEX", "opt_a": "A1", "opt_b": "B1", "opt_c": "C1", "opt_d": "D1"})]:
        p = build_prompts(fam, "resting cells", **genes)
        assert "GENEX" in p["named"] and "GENEX" not in p["hidden"] and HIDDEN in p["hidden"]
        diff = [(a, b) for a, b in zip(p["named"].splitlines(), p["hidden"].splitlines()) if a != b]
        assert all("GENEX" in a or "GENEY" in a for a, _ in diff) and len(p["named"].splitlines()) == len(p["hidden"].splitlines())


def test_run_order_separates_a_questions_calls():
    items = [(f"q{i}", v, s) for i in range(20) for v in ("named", "hidden") for s in range(3)]
    order = run_order(items, np.random.default_rng(0))
    assert sorted(order) == sorted(items)
    assert all(a[0] != b[0] for a, b in zip(order, order[1:]))
    with pytest.raises(ValueError):
        run_order([("q1", "named", 0), ("q1", "hidden", 0), ("q2", "named", 0)], np.random.default_rng(0))


# ---------------------------------------------------------------- scoring

def test_combine_samples_both_ways():
    probs = [np.array([1.0, 0.0]), np.array([0.0, 1.0])]
    c = combine_samples(probs, y=0)
    assert c["mean_brier"] == pytest.approx(1.0)  # (0 + 2) / 2
    assert c["brier_of_mean"] == pytest.approx(0.5)  # mean forecast (0.5, 0.5)


def test_auc_murphy_and_baselines():
    assert auc(np.array([0.9, 0.8, 0.1, 0.2]), np.array([True, True, False, False])) == 1.0
    assert auc(np.array([0.5, 0.5]), np.array([True, False])) == 0.5
    rng = np.random.default_rng(0)
    y = rng.integers(0, 3, 500)
    p = np.full((500, 3), 0.1)
    p[np.arange(500), y] = 0.8
    m = murphy(p, y)
    assert m["reliability"] - m["resolution"] + m["uncertainty"] == pytest.approx(m["brier"], abs=1e-9)
    X = rng.normal(size=(400, 1))
    yy = (X[:, 0] + rng.normal(scale=0.3, size=400) > 0).astype(int)
    P = predict_softmax(fit_softmax(X, yy, 2), X)
    assert (P.argmax(1) == yy).mean() > 0.85
    F = rng.normal(size=(300, 4, 1))
    choice = F[:, :, 0].argmax(1)
    b = fit_conditional_logit(F, choice)
    assert (predict_conditional_logit(b, F).argmax(1) == choice).mean() > 0.9
    assert argmax_forecast(np.array([[0.1, 0.5, 0.5]])).tolist() == [[0, 0.5, 0.5]]
    assert brier(np.array([[1.0, 0.0]]), np.array([1]))[0] == pytest.approx(2)


def test_cluster_boot_slope_and_completeness():
    df = pd.DataFrame({"cluster": np.repeat(np.arange(30), 2), "x": np.repeat(np.arange(30.0), 2)})
    df["y"] = 2 * df["x"] + 1
    point, lo, hi = cluster_boot(df, lambda d: slope(d, "y", "x"), n_boot=50)
    assert point == pytest.approx(2) and lo == pytest.approx(2) and hi == pytest.approx(2)
    expected = pd.DataFrame({"qid": ["a", "a", "b"], "version": ["named", "hidden", "named"], "sample": [0, 0, 0]})
    resp = pd.DataFrame({"qid": ["a", "a"], "version": ["named", "hidden"], "sample": [0, 0], "error": [None, "quota"]})
    assert completeness(resp, expected) == {"unanswered": 1, "infra_errors": 1}


def test_baseline_rungs_are_calibrated_and_use_signal():
    from dgbench.baselines import Context, crossfit, label_index

    rng = np.random.default_rng(0)
    n = 600
    gids = np.arange(n)
    terms = {int(g): frozenset({f"t{g % 7}", "shared"}) for g in gids}  # options sharing t{g%7} with the target
    ld = pd.Series(rng.normal(size=n), index=gids)
    ctx = Context(ld, {}, terms, {}, -2.0)
    # neighbour: the correct option shares the target's specific term; distractors do not
    rows = []
    for t in range(150):
        correct = int((t + 7) % n)
        dis = [int(x) for x in rng.choice([g for g in gids if g % 7 != t % 7], 3, replace=False)]
        order = rng.permutation(4)
        opts = np.array([correct] + dis)[order]
        rows.append({"GeneID": t, "condition": "Rest", "option_GeneIDs": opts.tolist(), "label": "ABCD"[int(np.flatnonzero(order == 0)[0])]})
    df = pd.DataFrame(rows)
    out = crossfit("neighbour", ctx, df, "GeneID", seed=0)
    y = label_index("neighbour", df)
    b_ann = ((out["annotation_only"] - np.eye(4)[y]) ** 2).sum(1).mean()
    b_fame = ((out["fame_only"] - np.eye(4)[y]) ** 2).sum(1).mean()
    assert b_ann < 0.5  # Jaccard softmax learns a sharp temperature when the signal is real
    assert abs(b_fame - 0.75) < 0.05  # no signal: stays near uniform, not confidently wrong


def test_balanced_pool_equal_cells():
    from dgbench.baselines import balanced_pool

    df = pd.DataFrame({"label": ["u"] * 50 + ["d"] * 5 + ["i"] * 8, "condition": "Rest"})
    out = balanced_pool(df, ["condition", "label"], max_total=1000, seed=0)
    assert out["label"].value_counts().to_dict() == {"u": 5, "d": 5, "i": 5}


def test_skill_point_gain_and_family_balance():
    from dgbench.scoring2 import family_balanced_mean, normalized_gain

    g = normalized_gain([2 / 3, 0.5, 0.75], [0.0, 0.0, 0.0], ["readout", "gene", "neighbour"])
    assert g == pytest.approx([1.0, 1.0, 1.0])  # each family's uniform Brier maps to one skill point
    df = pd.DataFrame({"family": ["readout"] * 9 + ["gene"], "gain": [0.0] * 9 + [1.0]})
    assert family_balanced_mean(df, "gain") == pytest.approx(0.5)  # equal family weight, not 0.1


def test_top_k_effects_and_wrong_names():
    rows = _rows(1)
    labels = np.array([[LAB_DOWN, LAB_UP, LAB_UNCHANGED]], dtype=np.int8)
    zrank = np.array([[1, 0, 2]], dtype=np.int16)
    c = readout_candidates(rows, labels, np.array([[0, 0, 99]]), ["Rest"], np.array([-1]), R=5, zrank=zrank, top_k=1)
    assert set(zip(c["readout_col"], c["label"])) == {(1, "increased"), (2, "unchanged")}  # rank-1 decrease excluded
    from dgbench.probe2 import wrong_names

    r = _rows(6, bins=[0, 0, 0, 1, 0, 0])
    r["symbol"] = ["G0", "G1", "G2", "G3", "G4", "G5"]
    r["target_baseMean"] = [50, 60, 55, 50, 500, 52]
    pool = np.array([True, True, True, True, True, False])
    out = wrong_names(r, [[0], [0, 1]], [{"G2"}, set()], log2_tol=0.5, pool=pool, rng=np.random.default_rng(0))
    assert out[0] == [1]  # G2 excluded by symbol, G3 other bin, G4 expression, G5 not in pool
    assert out[1] is None or (len(set(out[1])) == 2 and not set(out[1]) & {0, 1})


def test_agreement_filter_per_family():
    import importlib.util
    from pathlib import Path

    path = Path(__file__).resolve().parents[1] / "scripts" / "08_make_probe2_batch.py"
    spec = importlib.util.spec_from_file_location("gen08", path)
    gen = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gen)
    cands = {"all_three": ["a", "b", "c"], "d12_d34": ["a"]}
    per_family = {"probe2": {"agreement": {"candidates": cands, "chosen": {"readout": "d12_d34", "gene": "all_three"}}}}
    assert gen.family_splits(per_family, "readout") == ("d12_d34", ["a"])
    assert gen.family_splits(per_family, "gene") == ("all_three", ["a", "b", "c"])
    single = {"probe2": {"agreement": {"candidates": cands, "chosen": "all_three"}}}
    assert gen.family_splits(single, "readout") == ("all_three", ["a", "b", "c"])


def test_decision_branch():
    from dgbench.scoring2 import decision_branch
    ok = {"A_pooled_gain_ci_low_above": True, "B_slope_with_covariates_ci_low_above": True,
          "top_bin_gain_ci_low_at_least": True, "positive_control_gain_ci_low_at_least": True}
    assert decision_branch(ok) == 4
    assert decision_branch({**ok, "top_bin_gain_ci_low_at_least": False}) == 3
    assert decision_branch({**ok, "B_slope_with_covariates_ci_low_above": False}) == 3
    assert decision_branch({**ok, "A_pooled_gain_ci_low_above": False, "B_slope_with_covariates_ci_low_above": None}) == 2
    assert decision_branch({**ok, "positive_control_gain_ci_low_at_least": False, "A_pooled_gain_ci_low_above": False}) == 1
