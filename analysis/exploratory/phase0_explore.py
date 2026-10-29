"""Phase 0 exploratory aggregates (batch p0-20261023-165705-9eb7).

Written on 2026-10-23 AFTER seeing the Phase 0 data. Not pre-registered: nothing here
feeds the pre-registered checks, and any use of these numbers must be labelled exploratory.
Prints aggregates only (pooled and per-bin statistics); it reads scored responses from
runs_root and writes nothing.

Usage: python analysis/exploratory/phase0_explore.py
"""
import os
import numpy as np, pandas as pd
from scipy.stats import spearmanr

D = os.path.expanduser("~/benchmarks/dgb/dgb-runs/p0-20261023-165705-9eb7")
L = ["decreased", "unchanged", "increased"]
rng = np.random.default_rng(0)

def brier_rows(df):
    P = df[[f"p_{l}" for l in L]].to_numpy(); Y = pd.get_dummies(df["label"])[L].to_numpy(float)
    return ((P - Y) ** 2).sum(1)

def skill(df, ref=np.array([1/3, 1/3, 1/3])):
    Y = pd.get_dummies(df["label"]).reindex(columns=L, fill_value=0).to_numpy(float)
    b_ref = ((ref - Y) ** 2).sum(1).mean()
    return 1 - brier_rows_full(df).mean() / b_ref

def brier_rows_full(df):
    P = df[[f"p_{l}" for l in L]].to_numpy(); Y = pd.get_dummies(df["label"]).reindex(columns=L, fill_value=0).to_numpy(float)
    return ((P - Y) ** 2).sum(1)

def boot_gene(df, f, n=2000):
    g = df.groupby("GeneID").indices; keys = list(g)
    out = []
    for _ in range(n):
        ix = np.concatenate([g[keys[k]] for k in rng.integers(0, len(keys), len(keys))])
        out.append(f(df.iloc[ix]))
    return np.percentile(out, [2.5, 97.5])

m = {k: pd.read_parquet(f"{D}/scored_{k}.parquet") for k in ["opus-5.5-cli", "sol-6.1-cli"]}
for k, df in m.items():
    df = df[~df["infra_error"].astype(bool)]
    m[k] = df
    print(f"\n===== {k}  n={len(df)}")
    s = skill(df); lo, hi = boot_gene(df, skill)
    print(f"pooled skill vs uniform {s:.3f} [{lo:.3f}, {hi:.3f}]")
    P = df[[f"p_{l}" for l in L]]
    print("mean predicted prob per label:", P.mean().round(3).to_dict())
    print("argmax share per label:", P.idxmax(axis=1).str[2:].value_counts(normalize=True).round(3).to_dict())
    print("mean max prob %.3f; share with max<=0.40: %.3f; share with max>=0.70: %.3f" %
          (P.max(1).mean(), (P.max(1) <= 0.40).mean(), (P.max(1) >= 0.70).mean()))
    print("mean prob on true label by true label:",
          {l: round(float(df.loc[df.label == l, f'p_{l}'].mean()), 3) for l in L})
    print("skill by true label (vs uniform):", {l: round(float(skill(df[df.label == l])), 3) for l in L})
    print("skill by condition:", {c: round(float(skill(g)), 3) for c, g in df.groupby("condition")})
    ch = df[df.label != "unchanged"]
    corr = np.where(ch.label == "increased", ch.p_increased > ch.p_decreased, ch.p_decreased > ch.p_increased)
    print("direction right among changed (P(correct dir) > P(opposite)): %.3f (n=%d)" % (corr.mean(), len(ch)))
    print("  by bin:", ch.assign(c=corr).groupby("density_bin")["c"].mean().round(3).to_dict())
    un = df[df.label == "unchanged"]; chg = df[df.label != "unchanged"]
    print("mean p_unchanged when truly unchanged %.3f vs when changed %.3f" % (un.p_unchanged.mean(), chg.p_unchanged.mean()))
    imp = (2/3) - brier_rows_full(df)   # per-question improvement over uniform
    r, p = spearmanr(df.log_density, imp)
    print(f"spearman(log_density, Brier improvement) = {r:.3f} (p={p:.2f})")
    print("skill by readout (n):", {ro: (round(float(skill(g)), 2), len(g)) for ro, g in df.groupby("readout")})

o, s_ = m["opus-5.5-cli"].set_index("qid"), m["sol-6.1-cli"].set_index("qid")
common = o.index.intersection(s_.index)
oc, sc = o.loc[common].reset_index(), s_.loc[common].reset_index()
print(f"\n===== paired on {len(common)} shared questions")
print("opus skill %.3f, sol skill %.3f" % (skill(oc), skill(sc)))
def diff(ix_df):
    q = ix_df["qid"]; return skill(o.loc[q].reset_index()) - skill(s_.loc[q].reset_index())
lo, hi = boot_gene(oc, diff, 1000)
print(f"opus - sol skill difference {diff(oc):.3f} [{lo:.3f}, {hi:.3f}]")
lean_o = oc.p_increased - oc.p_decreased; lean_s = sc.p_increased - sc.p_decreased
print("correlation of up-vs-down lean between models: %.3f" % np.corrcoef(lean_o, lean_s)[0, 1])
print("argmax agreement: %.3f" % (oc[[f'p_{l}' for l in L]].idxmax(1).values == sc[[f'p_{l}' for l in L]].idxmax(1).values).mean())

print("\n===== decomposition and condition structure")
for k, df in m.items():
    mean_fc = df[[f"p_{l}" for l in L]].mean().to_numpy()
    const = df.copy()
    for i, l in enumerate(L): const[f"p_{l}"] = mean_fc[i]
    print(f"{k}: skill {skill(df):.3f}; same model's average forecast given to every question {skill(const):.3f}; "
          f"=> discrimination part {skill(df) - skill(const):.3f}")
    print("  truth label share by condition:", df.groupby("condition")["label"].value_counts(normalize=True).unstack().round(2).to_dict("index"))
    print("  mean forecast by condition:", df.groupby("condition")[[f"p_{l}" for l in L]].mean().round(2).to_dict("index"))
    ch = df[df.label != "unchanged"]
    corr = np.where(ch.label == "increased", ch.p_increased > ch.p_decreased, ch.p_decreased > ch.p_increased)
    print("  direction right among changed, by condition:", ch.assign(c=corr).groupby("condition")["c"].mean().round(3).to_dict())
    il2 = df[df.readout.isin(["IL2", "IL4", "IFNG", "TNF", "IL13"])]
    print("  cytokine readouts: truth share", il2.label.value_counts(normalize=True).round(2).to_dict(),
          "| mean forecast", il2[[f"p_{l}" for l in L]].mean().round(2).to_dict())
    # does skill track density at all within changed questions?
    r, p = spearmanr(ch.log_density, np.where(ch.label == "increased", ch.p_increased, ch.p_decreased))
    print(f"  spearman(log_density, prob on correct direction | changed) = {r:.3f} (p={p:.2f})")

print("\n===== gene-blind baseline: label frequencies by (readout, condition), leave-one-gene-out, add-1 smoothing")
df = m["opus-5.5-cli"].copy()   # all 600 questions; truth identical across models
Y = pd.get_dummies(df["label"]).reindex(columns=L, fill_value=0).astype(float)
for key in [["condition"], ["readout"], ["readout", "condition"]]:
    base = df.copy()
    for i in df.index:
        other = df[(df.GeneID != df.at[i, "GeneID"])]
        cell = other
        for c in key: cell = cell[cell[c] == df.at[i, c]]
        cnt = Y.loc[cell.index].sum().to_numpy() + 1
        for j, l in enumerate(L): base.at[i, f"p_{l}"] = cnt[j] / cnt.sum()
    s = skill(base); lo, hi = boot_gene(base, skill, 500)
    print(f"by {'+'.join(key)}: pooled skill {s:.3f} [{lo:.3f}, {hi:.3f}]; by bin",
          {b: round(float(skill(g)), 3) for b, g in base.groupby("density_bin")})
