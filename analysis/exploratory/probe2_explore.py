"""Probe v2 exploratory aggregates (batch p2-20261023-232739-c559).

Written on 2026-10-24 AFTER seeing the final probe v2 report. Not pre-registered: nothing here
feeds the pre-registered checks or the decision rule (D-025), and any use of these numbers must
be labelled exploratory. Writes aggregates to analysis/exploratory/probe2_explore.md; gene
identities (part a) go to data_root/derived/probe2_explore/ and are never committed.

  a. Gene composition of the bin-0 flagged cells, and the positive control with bin 0 excluded.
  b. Name-similarity rung for F-neighbour (shared symbol prefix, symbol root, HGNC gene group).
  c. Essentiality rung for F-gene (DepMap 24Q4 Chronos gene effect, Replogle 2022 K562
     genome-wide knockdown strength, -pct_expr), overall and by DE-count ratio band.
  d. Opus vs Sol discrimination (Murphy resolution, AUC) separately from calibration (Murphy
     reliability, ECE), per family, on the questions both models answered.

Extra inputs (data_root/raw): hgnc/hgnc_complete_set.txt, depmap/CRISPRGeneEffect_24Q4.csv,
replogle/K562_gwps_normalized_bulk_01.h5ad.

Usage: python analysis/exploratory/probe2_explore.py [--parts abcd] [--n-boot 2000]
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))
from dgbench.batch import batch_dirs, read_jsonl  # noqa: E402
from dgbench.config import derived_path, load_config  # noqa: E402
from dgbench.density import esearch  # noqa: E402
from dgbench.genes import build_maps, read_gene_info  # noqa: E402
from dgbench.probe2 import LABELS  # noqa: E402
from dgbench.scoring2 import (UNIFORM_BRIER, auc, brier, cluster_boot, ece, family_balanced_mean, fit_conditional_logit,  # noqa: E402
                              fit_softmax, murphy, normalized_gain, predict_conditional_logit, predict_softmax)

BATCH = "p2-20261023-232739-c559"
MODELS = {"opus-5.5-cli": "2026-07-01", "sol-6.1-cli": "2026-05-01"}
spec = importlib.util.spec_from_file_location("score", REPO / "scripts" / "09_score_probe2.py")
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)


def fmt(t):
    return f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"


def load(cfg):
    """truth, and per model a per-question frame: Briers and mean forecasts per version, gain in skill points."""
    run_dir, truth_dir = batch_dirs(cfg, BATCH)
    truth = pd.DataFrame(read_jsonl(truth_dir / "truth.jsonl")).set_index("qid", drop=False)
    truth.index.name = None
    truth["cluster"] = [g[0] for g in truth["GeneIDs"]]
    out = {}
    for m in MODELS:
        resp = pd.DataFrame(read_jsonl(run_dir / "responses" / f"{m}.jsonl")).drop_duplicates(["qid", "version", "sample"], keep="last")
        sc = S.scores_for(m, resp, truth).set_index(["qid", "version"])
        q = truth.loc[sorted({i for i, _ in sc.index})].copy()
        for v in ("named", "hidden"):
            q[f"b_{v}"] = sc.xs(v, level="version")["mean_brier"].reindex(q.index)
            q[f"p_{v}"] = sc.xs(v, level="version")["mean_p"].reindex(q.index)
        q["gain"] = normalized_gain(q["b_hidden"], q["b_named"], q["family"])
        out[m] = q
    return truth, truth_dir, out


def ylab(df):
    return np.array([LABELS[f].index(l) for f, l in zip(df["family"], df["label"])])


# ---------------------------------------------------------------- a. bin-0 flagged composition

def part_a(cfg, truth, q, n_boot, lines):
    genes = pd.read_parquet(derived_path(cfg, "genes.parquet")).set_index("GeneID")
    gi = read_gene_info(cfg["ncbi"]["gene_info"]).set_index("GeneID")
    hg = pd.read_csv(Path(cfg["paths"]["data_root"]).expanduser() / "raw/hgnc/hgnc_complete_set.txt", sep="\t", low_memory=False,
                     usecols=["symbol", "locus_type", "alias_symbol", "prev_symbol", "date_symbol_changed", "gene_group", "entrez_id"])
    hg = hg.dropna(subset=["entrez_id"]).astype({"entrez_id": int}).set_index("entrez_id")
    cell = truth[(truth["stratum"] == "flagged") & (truth["density_bin"] == 0)]
    ids = sorted({g for gs in cell["GeneIDs"] for g in gs})
    # reference: genes of main-stratum bin-0 questions, same families
    ref_pool = sorted({g for gs in truth[(truth["stratum"] == "main") & (truth["density_bin"] == 0)]["GeneIDs"] for g in gs} - set(ids))
    ref = list(np.random.default_rng(0).choice(ref_pool, min(40, len(ref_pool)), replace=False))
    rows = []
    for g in ids + ref:
        sym = gi.at[g, "Symbol"] if g in gi.index else str(g)
        h = hg.loc[g] if g in hg.index else None
        aliases = sorted({a for col in ("alias_symbol", "prev_symbol") if h is not None and isinstance(h[col], str) for a in h[col].split("|")})
        row = {"GeneID": g, "symbol": sym, "set": "bin0_flagged" if g in ids else "bin0_main_reference",
               "flagged_paper": bool(genes.at[g, "flagged_paper"]) if g in genes.index else None,
               "type_of_gene": gi.at[g, "type_of_gene"] if g in gi.index else None,
               "hgnc_locus_type": h["locus_type"] if h is not None else None,
               "aliases_prev": "|".join(aliases), "date_symbol_changed": h["date_symbol_changed"] if h is not None else None,
               "gene_group": h["gene_group"] if h is not None else None}
        for cut in sorted(set(MODELS.values())):
            maxdate = (pd.Timestamp(cut) - pd.Timedelta(days=1)).strftime("%Y/%m/%d")
            row[f"g2p_papers_{cut}"] = float(genes.at[g, f"n_papers_{cut}"]) if g in genes.index else np.nan
            row[f"pubmed_symbol_{cut}"] = esearch(f'"{sym}"[tiab]', "1800/01/01", maxdate)[0]
            terms = " OR ".join(f'"{a}"[tiab]' for a in [sym, *aliases])
            row[f"pubmed_symbol_or_alias_{cut}"] = esearch(f"({terms})", "1800/01/01", maxdate)[0]
        rows.append(row)
    tab = pd.DataFrame(rows)
    out = derived_path(cfg, "probe2_explore")
    out.mkdir(parents=True, exist_ok=True)
    tab.to_csv(out / "bin0_flagged_genes.tsv", sep="\t", index=False)
    cut = "2026-05-01"
    tab["ratio_sym"] = tab[f"pubmed_symbol_{cut}"] / tab[f"g2p_papers_{cut}"].clip(lower=1)
    tab["ratio_alias"] = tab[f"pubmed_symbol_or_alias_{cut}"] / tab[f"g2p_papers_{cut}"].clip(lower=1)
    lines += ["## a. Bin-0 flagged cells", "",
              f"Questions: {len(cell)} ({cell.groupby('family').size().to_dict()}); distinct genes: {len(ids)} "
              f"(flagged by the paper: {int(tab.loc[tab['set'] == 'bin0_flagged', 'flagged_paper'].sum())}). "
              f"Reference: {len(ref)} random genes from main-stratum bin-0 questions. Identities are in data_root only.", "",
              "| set | n | NCBI type protein-coding | symbol changed (HGNC) | has alias/prev symbol | median gene2pubmed papers | "
              "median PubMed [tiab] symbol hits | median hits/papers (symbol) | median hits/papers (symbol or alias) |", "|---|---|---|---|---|---|---|---|---|"]
    for s, g in tab.groupby("set"):
        lines.append(f"| {s} | {len(g)} | {(g['type_of_gene'] == 'protein-coding').sum()} | {g['date_symbol_changed'].notna().sum()} | "
                     f"{(g['aliases_prev'] != '').sum()} | {g[f'g2p_papers_{cut}'].median():.1f} | {g[f'pubmed_symbol_{cut}'].median():.0f} | "
                     f"{g['ratio_sym'].median():.1f} | {g['ratio_alias'].median():.1f} |")
    lines += ["", f"PubMed counts are title/abstract hits before {cut} (Sol's cutoff); symbol searches over-count short or "
              "word-like symbols, and alias searches over-count more, so compare the two sets rather than reading the ratios as rates.", ""]
    lines += ["Positive-control gain (flagged stratum, F-readout and F-gene, mean of the two family means, mean_brier), with and without bin 0:", ""]
    for m, d in q.items():
        f = d[(d["stratum"] == "flagged") & d["family"].isin(["readout", "gene"])]
        lines.append(f"- {m}: all bins {fmt(cluster_boot(f, lambda x: family_balanced_mean(x, 'gain'), n_boot=n_boot))} (n={len(f)}); "
                     f"bin 0 excluded {fmt(cluster_boot(f[f['density_bin'] != 0], lambda x: family_balanced_mean(x, 'gain'), n_boot=n_boot))} "
                     f"(n={int((f['density_bin'] != 0).sum())})")
    lines.append("")


# ---------------------------------------------------------------- b. name-similarity rung (F-neighbour)

def lcp(a, b):
    n = 0
    for x, y in zip(a, b):
        if x != y:
            break
        n += 1
    return n


def root(s):
    m = re.match(r"[A-Z]+", s)
    return m.group(0) if m else s


def name_features(targets, options, sym, groups):
    """(n, 4, 3): shared prefix length, same alphabetic root (2+ letters), shared HGNC gene group."""
    F = np.zeros((len(targets), 4, 3))
    for i, (t, os_) in enumerate(zip(targets, options)):
        st, gt = sym.get(t, ""), groups.get(t, set())
        for j, o in enumerate(os_):
            so = sym.get(o, "")
            F[i, j] = [lcp(st, so), float(len(root(st)) >= 2 and root(st) == root(so)), float(bool(gt & groups.get(o, set())))]
    return F


def part_b(cfg, truth, truth_dir, q, n_boot, lines):
    gi = read_gene_info(cfg["ncbi"]["gene_info"])
    sym = dict(zip(gi["GeneID"], gi["Symbol"]))
    hg = pd.read_csv(Path(cfg["paths"]["data_root"]).expanduser() / "raw/hgnc/hgnc_complete_set.txt", sep="\t", low_memory=False,
                     usecols=["entrez_id", "gene_group_id"]).dropna()
    groups = {int(e): set(str(g).split("|")) for e, g in zip(hg["entrez_id"], hg["gene_group_id"])}
    cache = derived_path(cfg, "probe2")
    rows_cache, readouts = pd.read_parquet(cache / "rows.parquet"), pd.read_parquet(cache / "readouts.parquet")
    train = pd.read_parquet(truth_dir / "baseline_train.parquet")
    tr = S.train_frame("neighbour", train[train["family"] == "neighbour"], rows_cache, readouts)
    T = truth[truth["family"] == "neighbour"]
    te = S.test_frame("neighbour", T)
    Ftr = name_features(tr["GeneID"], tr["option_GeneIDs"], sym, groups)
    Fte = name_features(te["GeneID"], te["option_GeneIDs"], sym, groups)
    ytr, yte = ylab(tr.assign(family="neighbour")), ylab(T)
    b = fit_conditional_logit(Ftr, ytr)
    P = predict_conditional_logit(b, Fte)
    T = T.assign(b_name=brier(P, yte))
    correct = Fte[np.arange(len(yte)), yte]
    wrong = np.array([np.delete(Fte[i], yte[i], axis=0).mean(0) for i in range(len(yte))])
    lines += ["## b. Name-similarity rung for F-neighbour", "",
              "Conditional logit over the four options on (shared symbol prefix length, same alphabetic symbol root, shared HGNC gene "
              f"group), fitted on the {len(tr)} outside-batch neighbour training items like the other rungs; coefficients "
              f"{np.round(b, 3).tolist()}. HGNC groups are from the current HGNC file, not a release dated before each cutoff.", "",
              "Feature means, correct option vs mean of distractors (all batch neighbour items): "
              + "; ".join(f"{n} {correct[:, k].mean():.3f} vs {wrong[:, k].mean():.3f}" for k, n in enumerate(["prefix", "same root", "same group"])), "",
              "| model | stratum | bin | n | rung Brier skill vs uniform | model named Brier skill | model gain (named vs hidden) | model named gain beyond rung |",
              "|---|---|---|---|---|---|---|---|"]
    u = UNIFORM_BRIER["neighbour"]
    for m, d in q.items():
        dn = d[d["family"] == "neighbour"].join(T[["b_name"]])
        for stratum, gs in dn.groupby("stratum"):
            for bn, g in [("all", gs)] + list(gs.groupby("density_bin")):
                beyond = cluster_boot(g, lambda x: ((x["b_name"] - x["b_named"]) / u).mean(), n_boot=n_boot // 4)
                lines.append(f"| {m} | {stratum} | {bn} | {len(g)} | {1 - g['b_name'].mean() / u:.3f} | {1 - g['b_named'].mean() / u:.3f} | "
                             f"{g['gain'].mean():.3f} | {fmt(beyond)} |")
    lines.append("")


# ---------------------------------------------------------------- c. essentiality rung (F-gene)

def essentiality_tables(cfg):
    raw = Path(cfg["paths"]["data_root"]).expanduser() / "raw"
    dm = pd.read_csv(raw / "depmap/CRISPRGeneEffect_24Q4.csv", index_col=0)
    eff = dm.mean(0)
    eff.index = [int(re.search(r"\((\d+)\)", c).group(1)) for c in eff.index]  # columns are "SYMBOL (EntrezID)"
    import anndata
    obs = anndata.read_h5ad(raw / "replogle/K562_gwps_normalized_bulk_01.h5ad", backed="r").obs
    ens = build_maps(read_gene_info(cfg["ncbi"]["gene_info"])).ensembl
    # index is "<n>_<symbol>_<promoter>_<Ensembl ID>"; pct_expr is the fractional change in target expression
    gid = obs.index.str.rsplit("_", n=1).str[1].map(ens.get)
    kd = (-obs["pct_expr"]).groupby(gid).mean()
    kd.index = kd.index.astype(int)
    return eff, kd


def part_c(cfg, truth, truth_dir, q, n_boot, lines):
    eff, kd = essentiality_tables(cfg)

    def feats(a, b):
        cols = []
        for s in (eff, kd):
            x, y = s.reindex(a).to_numpy(float), s.reindex(b).to_numpy(float)
            miss = np.isnan(x) | np.isnan(y)
            cols += [np.where(miss, 0, x - y), miss.astype(float)]
        return np.column_stack(cols)

    cache = derived_path(cfg, "probe2")
    rows_cache, readouts = pd.read_parquet(cache / "rows.parquet"), pd.read_parquet(cache / "readouts.parquet")
    train = pd.read_parquet(truth_dir / "baseline_train.parquet")
    tr = S.train_frame("gene", train[train["family"] == "gene"], rows_cache, readouts)
    T = truth[truth["family"] == "gene"]
    te = S.test_frame("gene", T)
    W = fit_softmax(feats(tr["GeneID_a"], tr["GeneID_b"]), ylab(tr.assign(family="gene")), 2)
    P = predict_softmax(W, feats(te["GeneID_a"], te["GeneID_b"]))
    T = T.assign(b_ess=brier(P, ylab(T)))
    cov = {n: float(np.mean(s.reindex(te["GeneID_a"]).notna().to_numpy() & s.reindex(te["GeneID_b"]).notna().to_numpy())) for n, s in [("DepMap", eff), ("Replogle", kd)]}
    lines += ["## c. Essentiality rung for F-gene", "",
              "Multinomial logistic on the pair differences in DepMap 24Q4 mean Chronos gene effect (mean over screened lines) and "
              "Replogle 2022 K562 genome-wide knockdown strength (−pct_expr, the fractional drop in target expression; mean over guides), each with a missing indicator, fitted on the "
              f"{len(tr)} outside-batch F-gene training pairs like the other rungs. Both genes covered: DepMap {cov['DepMap']:.0%}, "
              f"Replogle {cov['Replogle']:.0%} of batch pairs.", "",
              "| model | stratum | ratio band | n | rung Brier skill vs uniform | model named Brier skill | model named gain beyond rung |",
              "|---|---|---|---|---|---|---|"]
    u = UNIFORM_BRIER["gene"]
    for m, d in q.items():
        dg = d[d["family"] == "gene"].join(T[["b_ess"]])
        dg["band"] = pd.cut(dg["nde_ratio"], [0, 2, 4, 10, np.inf], right=False, labels=["<2", "2-4", "4-10", ">10"])
        for stratum, gs in dg.groupby("stratum"):
            for bn, g in [("all", gs)] + [(b, gb) for b, gb in gs.groupby("band", observed=True)]:
                beyond = cluster_boot(g, lambda x: ((x["b_ess"] - x["b_named"]) / u).mean(), n_boot=n_boot // 4)
                lines.append(f"| {m} | {stratum} | {bn} | {len(g)} | {1 - g['b_ess'].mean() / u:.3f} | {1 - g['b_named'].mean() / u:.3f} | {fmt(beyond)} |")
    lines.append("")


# ---------------------------------------------------------------- d. discrimination vs calibration

def disc_auc(fam, P, y):
    if fam == "readout":
        return auc(1 - P[:, LABELS[fam].index("unchanged")], y != LABELS[fam].index("unchanged"))
    if fam == "gene":
        return auc(P[:, 0], y == 0)
    hit = np.zeros_like(P, dtype=bool)
    hit[np.arange(len(y)), y] = True
    return auc(P.ravel(), hit.ravel())  # correct option vs distractors, pooled


def part_d(q, n_boot, lines):
    shared = q["opus-5.5-cli"].index.intersection(q["sol-6.1-cli"].index)
    lines += ["## d. Discrimination vs calibration on shared questions", "",
              f"{len(shared)} questions answered by both models (all strata). Murphy terms over 10 forecast bins, summed one-vs-rest "
              "(resolution: higher is better discrimination; reliability: lower is better calibration). AUC: F-readout P(changed); "
              "F-gene P(A) for A; F-neighbour correct option vs distractors, pooled.", "",
              "| family | version | model | resolution | reliability | ECE | AUC | Brier skill vs uniform |", "|---|---|---|---|---|---|---|---|"]
    stats = {}
    for fam in ("readout", "gene", "neighbour"):
        for v in ("named", "hidden"):
            for m, d in q.items():
                g = d.loc[shared][lambda x: x["family"] == fam]
                P, y = np.stack(g[f"p_{v}"].to_numpy()), ylab(g)
                mu = murphy(P, y)
                skill = 1 - brier(P, y).mean() / UNIFORM_BRIER[fam]
                lines.append(f"| {fam} | {v} | {m} | {mu['resolution']:.3f} | {mu['reliability']:.3f} | {ece(P, y):.3f} | {disc_auc(fam, P, y):.3f} | {skill:.3f} |")
                stats[(fam, v, m)] = g
    lines += ["", "Named version, Opus − Sol, gene-clustered bootstrap on shared questions:", ""]
    for fam in ("readout", "gene", "neighbour"):
        a, b = stats[(fam, "named", "opus-5.5-cli")], stats[(fam, "named", "sol-6.1-cli")]
        j = a[["family", "label", "cluster"]].assign(pa=a["p_named"], pb=b["p_named"].reindex(a.index))

        def diff(x, term):
            y = ylab(x)
            if term == "auc":
                return disc_auc(fam, np.stack(x["pa"].to_numpy()), y) - disc_auc(fam, np.stack(x["pb"].to_numpy()), y)
            return murphy(np.stack(x["pa"].to_numpy()), y)[term] - murphy(np.stack(x["pb"].to_numpy()), y)[term]
        lines.append(f"- {fam}: resolution {fmt(cluster_boot(j, lambda x: diff(x, 'resolution'), n_boot=n_boot // 4))}; "
                     f"reliability {fmt(cluster_boot(j, lambda x: diff(x, 'reliability'), n_boot=n_boot // 4))}; "
                     f"AUC {fmt(cluster_boot(j, lambda x: diff(x, 'auc'), n_boot=n_boot // 4))}")
    lines.append("")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--parts", default="abcd")
    ap.add_argument("--n-boot", type=int, default=2000)
    args = ap.parse_args()
    cfg = load_config()
    truth, truth_dir, q = load(cfg)
    lines = [f"# Probe v2 exploratory aggregates: batch {BATCH}", "",
             "**Exploratory, not pre-registered.** Written after the final report and D-025; nothing here changes the checks or "
             "the branch. Aggregates only; produced by `analysis/exploratory/probe2_explore.py`.", ""]
    for p in args.parts:
        {"a": lambda: part_a(cfg, truth, q, args.n_boot, lines), "b": lambda: part_b(cfg, truth, truth_dir, q, args.n_boot, lines),
         "c": lambda: part_c(cfg, truth, truth_dir, q, args.n_boot, lines), "d": lambda: part_d(q, args.n_boot, lines)}[p]()
    out = REPO / "analysis" / "exploratory" / "probe2_explore.md"
    out.write_text("\n".join(lines))
    print("\n".join(lines))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
