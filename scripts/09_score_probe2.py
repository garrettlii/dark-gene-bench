#!/usr/bin/env python3
"""Score a probe v2 batch. Writes reports/probe2_<batch>.md (aggregates only).

The report is final only when every model has 0 unanswered calls and 0 infrastructure
errors; otherwise it carries an INTERIM banner. Decision checks read their thresholds from
the pre-registration's predictions YAML (copied into the batch manifest).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from dgbench.batch import batch_dirs, read_jsonl  # noqa: E402
from dgbench.config import REPO_ROOT, derived_path, load_config  # noqa: E402
from dgbench.baselines import Context, forecasts, label_index  # noqa: E402
from dgbench.genes import build_maps, read_gene_info  # noqa: E402
from dgbench.go import filter_annotations, gene_terms, read_gaf  # noqa: E402
from dgbench.probe2 import LABELS  # noqa: E402
from dgbench.scoring2 import (COMBINE, auc, brier, cluster_boot, combine_samples, completeness, decision_branch, ece,  # noqa: E402
                              family_balanced_mean, murphy, normalized_gain, slope)

COVARIATES = ["n_downstream", "log2_baseMean", "ontarget_effect_size", "donor_correlation_all_mean"]


def fmt(t):
    return f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"


def scores_for(model, resp, truth):
    """Per qid: Brier per version under both combine methods, and the mean forecast per version."""
    out = []
    lab_ix = {q: LABELS[f].index(l) for q, f, l in truth[["qid", "family", "label"]].itertuples(index=False)}
    ok = resp[resp["error"].isna()].copy()
    for (qid, version), g in ok.groupby(["qid", "version"]):
        fam = truth.loc[qid, "family"]
        K = len(LABELS[fam])
        probs = [np.array([p[l] for l in LABELS[fam]]) if p else np.full(K, 1 / K) for p in g["probs"]]  # parse failure = uniform
        c = combine_samples(probs, lab_ix[qid])
        out.append({"qid": qid, "version": version, **c, "mean_p": np.mean(probs, axis=0), "parse_failed": int(g["probs"].isna().sum())})
    return pd.DataFrame(out)


def train_frame(fam, tr, rows_cache, readouts):
    """Baseline training rows (indices into the probe2 cache) as plain GeneID frames."""
    gid = rows_cache["GeneID"].to_numpy()
    d = pd.DataFrame({"condition": tr["condition"].to_numpy(), "label": tr["label"].to_numpy()})
    if fam == "readout":
        d["GeneID"] = gid[tr["row"].astype(int).to_numpy()]
        d["readout_id"] = readouts["readout_id"].to_numpy()[tr["readout_col"].astype(int).to_numpy()]
    elif fam == "gene":
        d["GeneID_a"], d["GeneID_b"] = gid[tr["row_a"].astype(int).to_numpy()], gid[tr["row_b"].astype(int).to_numpy()]
    else:
        d["GeneID"] = gid[tr["target"].astype(int).to_numpy()]
        d["option_GeneIDs"] = [[int(gid[int(o)]) for o in os_] for os_ in tr["options"]]
    return d


def test_frame(fam, T):
    d = pd.DataFrame({"condition": T["condition"].to_numpy(), "label": T["label"].to_numpy()}, index=T.index)
    if fam == "readout":
        d["GeneID"], d["readout_id"] = [g[0] for g in T["GeneIDs"]], T["readout_id"].to_numpy()
    elif fam == "gene":
        d["GeneID_a"], d["GeneID_b"] = [g[0] for g in T["GeneIDs"]], [g[1] for g in T["GeneIDs"]]
    else:
        d["GeneID"], d["option_GeneIDs"] = [g[0] for g in T["GeneIDs"]], T["option_GeneIDs"].tolist()
    return d


def baselines(cfg, truth, train, cutoff, rows_cache, readouts, genes, maps):
    """Brier per qid for uniform, label-frequency, fame-only, annotation-only and annotation-only (no IEA) forecasts.

    Fame and annotation rungs are calibrated forecasts fitted on genes outside the batch
    (dgbench.baselines); GO terms come from the archived release for this model's cutoff (D-021)."""
    gaf = read_gaf(cfg["go"]["releases"][cutoff]["path"])
    sym = {**maps.synonym, **maps.symbol}
    terms = {False: gene_terms(filter_annotations(gaf, cfg["go"]["exclude_refs"]), sym),
             True: gene_terms(filter_annotations(gaf, cfg["go"]["exclude_refs"], exclude_evidence=("IEA",)), sym)}
    bm = rows_cache.set_index(["GeneID", "condition"])["target_baseMean"].to_dict()
    out = []
    for fam, T in truth.groupby("family"):
        K = len(LABELS[fam])
        te = test_frame(fam, T)
        y = label_index(fam, te)
        freq = np.bincount(y, minlength=K) / len(y)
        res = {"uniform": np.full((len(T), K), 1 / K), "label_freq": np.tile(freq, (len(T), 1))}
        tr = train_frame(fam, train[train["family"] == fam], rows_cache, readouts)
        for no_iea in (False, True):
            ctx = Context(genes.set_index("GeneID")[f"log_density_{cutoff}"], bm, terms[no_iea], maps.ensembl,
                          float(np.log10(cfg["density"]["epsilon"])))
            f = forecasts(fam, ctx, tr, te)
            if no_iea:
                res["annotation_only_noIEA"] = f["annotation_only"]
            else:
                res.update(f)
        for name, P in res.items():
            out.append(pd.DataFrame({"qid": T.index, "baseline": name, "brier": brier(P, y)}))
    return pd.concat(out, ignore_index=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", default=None)
    ap.add_argument("--batch", required=True)
    ap.add_argument("--n-boot", type=int, default=2000)
    args = ap.parse_args()
    cfg = load_config(args.config)
    run_dir, truth_dir = batch_dirs(cfg, args.batch)
    manifest = json.loads((truth_dir / "manifest.json").read_text())
    pred = manifest["predictions"]
    truth = pd.DataFrame(read_jsonl(truth_dir / "truth.jsonl")).set_index("qid", drop=False)
    truth.index.name = None
    truth["cluster"] = [g[0] for g in truth["GeneIDs"]]
    truth["log2_baseMean"] = np.log2(truth["target_baseMean"])
    train = pd.read_parquet(truth_dir / "baseline_train.parquet")
    cache = derived_path(cfg, "probe2")
    rows_cache, readouts = pd.read_parquet(cache / "rows.parquet"), pd.read_parquet(cache / "readouts.parquet")
    genes = pd.read_parquet(derived_path(cfg, "genes.parquet"))
    maps = build_maps(read_gene_info(cfg["ncbi"]["gene_info"]))
    chosen = cfg["probe2"].get("combine_samples")

    models = [m for m in cfg["models"] if (run_dir / f"calls_{m['name']}.jsonl").exists()]
    status, sections, gains, model_checks = {}, [], {}, {}
    for m in models:
        expected = pd.DataFrame(read_jsonl(run_dir / f"calls_{m['name']}.jsonl"))
        resp = pd.DataFrame(read_jsonl(run_dir / "responses" / f"{m['name']}.jsonl"))
        status[m["name"]] = completeness(resp, expected) if len(resp) else {"unanswered": len(expected), "infra_errors": 0}
        if not len(resp):
            continue
        resp = resp.drop_duplicates(["qid", "version", "sample"], keep="last")
        sc = scores_for(m["name"], resp, truth)
        wide = sc.pivot(index="qid", columns="version", values=list(COMBINE))
        wide = wide[wide[[(c, v) for c in COMBINE for v in ("named", "hidden")]].notna().all(axis=1)]
        q = truth.loc[wide.index].copy()
        q["is_gene"] = (q["family"] == "gene").astype(float)
        has_wrong = "wrong" in sc["version"].unique()
        for c in COMBINE:
            # skill points (D-024): Brier difference divided by the family's uniform Brier
            q[f"gain_{c}"] = normalized_gain(wide[(c, "hidden")], wide[(c, "named")], q["family"])
            q[f"named_{c}"], q[f"hidden_{c}"] = wide[(c, "named")], wide[(c, "hidden")]
            if has_wrong:
                q[f"kgain_{c}"] = normalized_gain(wide[(c, "wrong")], wide[(c, "named")], q["family"])
        x = f"log_density_{m['cutoff_date']}"
        lines = [f"## {m['name']} (density at its own cutoff {m['cutoff_date']})", ""]
        for c in COMBINE:
            lines += [f"### Gain in skill points = (Brier(hidden) - Brier(named)) / uniform Brier, samples combined as {c}"
                      + (" (pre-registered)" if c == chosen else "") + "; per family, descriptive", ""]
            for (fam, stratum), g in q.groupby(["family", "stratum"]):
                groups = [("all tiers", g)] if fam != "neighbour" else [(t, gg) for t, gg in g.groupby("tier")]
                for tier, gg in groups:
                    pooled = cluster_boot(gg, lambda d: d[f"gain_{c}"].mean(), n_boot=args.n_boot)
                    sl = cluster_boot(gg, lambda d: slope(d, f"gain_{c}", x), n_boot=args.n_boot)
                    lines += [f"- {fam} / {stratum} / {tier}: n={len(gg)}; pooled gain {fmt(pooled)}; slope on log density {fmt(sl)}"]
                    if has_wrong:
                        lines += [f"  - knowledge gain (Brier(wrong name) - Brier(named), skill points): "
                                  f"{fmt(cluster_boot(gg.dropna(subset=[f'kgain_{c}']), lambda d: d[f'kgain_{c}'].mean(), n_boot=args.n_boot))}"]
                    lines += ["  - by bin: " + "; ".join(
                        f"{b}: {fmt(cluster_boot(gb, lambda d: d[f'gain_{c}'].mean(), n_boot=args.n_boot // 4))}"
                        for b, gb in gg.groupby("density_bin"))]
            lines.append("")
        # F-gene ratio bands (descriptive)
        if "nde_ratio" in q and (q["family"] == "gene").any():
            g = q[(q["family"] == "gene") & (q["stratum"] == "main")]
            band = pd.cut(g["nde_ratio"], [0, 2, 4, 10, np.inf], right=False, labels=["<2", "2-4", "4-10", ">10"])
            lines += ["### F-gene gain by DE-count ratio band (descriptive)", ""] + [
                f"- ratio {b}: n={len(gb)}; " + "; ".join(f"{c}: {fmt(cluster_boot(gb, lambda d, c=c: d[f'gain_{c}'].mean(), n_boot=args.n_boot // 4))}"
                                                           for c in COMBINE) for b, gb in g.groupby(band, observed=True)] + [""]
        # pre-registered checks (D-024): main stratum, F-readout and F-gene with equal family weight
        # (mean of the two family means); F-neighbour main is descriptive (analysis C)
        main = q[(q["stratum"] == "main") & q["family"].isin(["readout", "gene"])]
        if chosen in COMBINE and len(main):
            gcol = f"gain_{chosen}"
            pooled = cluster_boot(main, lambda d: family_balanced_mean(d, gcol), n_boot=args.n_boot)
            cov_slope = cluster_boot(main, lambda d: slope(d, gcol, x, COVARIATES + ["is_gene"]), n_boot=args.n_boot)
            top = main[main["density_bin"] == main["density_bin"].max()]
            top_gain = cluster_boot(top, lambda d: family_balanced_mean(d, gcol), n_boot=args.n_boot)
            flagged = q[(q["stratum"] == "flagged") & q["family"].isin(["readout", "gene"])]
            pc = cluster_boot(flagged, lambda d: family_balanced_mean(d, gcol), n_boot=args.n_boot) if len(flagged) else (np.nan,) * 3
            checks = {
                "A_pooled_gain_ci_low_above": pooled[1] > float(pred["min_pooled_gain"]),
                "B_slope_with_covariates_ci_low_above": cov_slope[1] > float(pred["min_slope"]) if pooled[1] > float(pred["min_pooled_gain"]) else None,
                "top_bin_gain_ci_low_at_least": top_gain[1] >= float(pred["top_bin_min_gain"]),
                "positive_control_gain_ci_low_at_least": pc[1] >= float(pred["positive_control_min_gain"]) if len(flagged) else None,
            }
            lines += ["### Pre-registered checks (skill points; F-readout and F-gene weighted equally)", "",
                      f"- pooled gain {fmt(pooled)}; slope with covariates and family {fmt(cov_slope)}; "
                      f"top-bin gain {fmt(top_gain)}; positive-control gain {fmt(pc)}"]
            lines += [f"- {k}: {'pass' if v else ('not evaluated' if v is None else 'FAIL')}" for k, v in checks.items()] + [""]
            gains[m["name"]], model_checks[m["name"]] = main[[gcol, "family", "cluster"]].rename(columns={gcol: "gain"}), checks
        # secondary measures
        lines += ["### Secondary measures (mean forecast over samples)", ""]
        for (fam, version), g in sc.merge(truth[["qid", "family", "label", "stratum"]], on="qid").groupby(["family", "version"]):
            P = np.stack(g["mean_p"].to_numpy())
            y = g["label"].map({l: i for i, l in enumerate(LABELS[fam])}).to_numpy()
            K = len(LABELS[fam])
            skill = 1 - brier(P, y).mean() / brier(np.full_like(P, 1 / K), y).mean()
            row = f"- {fam} / {version}: Brier skill vs uniform {skill:.3f}; ECE {ece(P, y):.3f}; parse failures {int(g['parse_failed'].sum())}"
            if fam == "readout":
                changed = y != LABELS[fam].index("unchanged")
                d, u = LABELS[fam].index("decreased"), LABELS[fam].index("increased")
                right, wrong = np.where(y[changed] == u, P[changed, u], P[changed, d]), np.where(y[changed] == u, P[changed, d], P[changed, u])
                dir_ok = (right > wrong) + 0.5 * (right == wrong)  # ties count half, as in the AUC
                row += f"; AUC on P(changed) {auc(1 - P[:, LABELS[fam].index('unchanged')], changed):.3f}; direction accuracy among changed {dir_ok.mean():.3f}"
            mu = murphy(P, y)
            row += "; Murphy " + ", ".join(f"{k} {v:.3f}" for k, v in mu.items())
            lines.append(row)
        # baseline ladder
        base = baselines(cfg, truth, train, m["cutoff_date"], rows_cache, readouts, genes, maps)
        named = q[[f"named_{c}" for c in COMBINE] + ["family", "stratum", "cluster"]]
        lines += ["", "### Baseline ladder: mean Brier, and the model's named gain beyond each rung (skill points: (rung Brier - named Brier) / uniform Brier)", ""]
        for (fam, b), g in base.merge(named, left_on="qid", right_index=True).groupby(["family", "baseline"]):
            beyond = cluster_boot(g, lambda d: normalized_gain(d["brier"], d[f"named_{chosen or 'mean_brier'}"], d["family"]).mean(),
                                  n_boot=args.n_boot // 4)
            lines.append(f"- {fam} / {b}: Brier {g['brier'].mean():.3f}; named gain beyond {fmt(beyond)}")
        lines.append("")
        sections += lines

    primary = cfg["probe2"].get("primary_model")
    if primary in model_checks:
        branch = decision_branch(model_checks[primary])
        sections += ["## Decision rule (prereg/probe2.md), applied mechanically", "",
                     f"- primary model {primary}: branch {branch}"]
        for other in [n for n in gains if n != primary]:
            # paired on shared questions: per-question gain difference, family-balanced, gene-clustered bootstrap
            shared = gains[primary].join(gains[other]["gain"].rename("other"), how="inner")
            shared["diff"] = shared["gain"] - shared["other"]
            d = cluster_boot(shared, lambda x: family_balanced_mean(x, "diff"), n_boot=args.n_boot)
            exposure = branch in (3, 4) and d[1] > 0
            sections += [f"- exposure contrast {primary} - {other}, pooled gain on {len(shared)} shared main-stratum "
                         f"F-readout and F-gene questions: {fmt(d)}",
                         f"- exposure clause (branches 3 and 4; CI excludes 0 with {primary} higher): "
                         + ("applies" if exposure else "does not apply")]
        sections.append("")

    final = all(s["unanswered"] == 0 and s["infra_errors"] == 0 for s in status.values()) and len(status) > 0
    head = [f"# Probe v2 results: batch {args.batch}", "",
            f"Pre-registration {manifest['prereg']['path']} @ {manifest['prereg']['commit'][:10]}. Aggregates only. k = {manifest['samples']}.", ""]
    if not final:
        head += [f"> **INTERIM.** Not every model is complete: {json.dumps(status)}. Rerun scripts/05_run_probe.py until every model "
                 "has 0 unanswered calls and 0 infrastructure errors, then re-score. Only the final report counts for the checks.", ""]
    else:
        head += [f"Completeness: {json.dumps(status)}.", ""]
    out = REPO_ROOT / "reports" / f"probe2_{args.batch}.md"
    out.write_text("\n".join(head + sections))
    print("\n".join(head + sections))
    print(f"wrote {out} ({'final' if final else 'INTERIM'})")


if __name__ == "__main__":
    main()
