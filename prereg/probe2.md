# Pre-registration: probe v2 (prior-only, named vs hidden gene)

Status: draft. Replace every FILL field, then commit and push before generating the batch (`scripts/08_make_probe2_batch.py --prereg prereg/probe2.md`). The generator also refuses to run while any probe v2 FILL value in `config/default.yaml` is null.

## Purpose

Phase 0 found no density gradient in prior-only skill, with most predictable structure coming from readout × condition rather than the knocked-down gene (D-014; exploratory analysis in `analysis/exploratory/phase0_explore.py`). Probe v2 measures directly how much naming the gene helps: every question is asked with the gene named and with it hidden, among perturbations with clear transcriptional effects (D-015).

## Fixed inputs

Recorded automatically in the batch manifest: config hash and full config, SHA-256 of the combined and donor-pair DE files and the GO annotation file, CLI versions and full command lines, this file's commit hash, seed, k.

- Models and harness settings (model IDs, CLI versions, effort, tools, config directories): opus-5.5-cli: Claude Opus 5.5 (claude-opus-5-5) via Claude Code 2.1.309, print mode, all tools disallowed, --effort xhigh (accepted; not echoed by the CLI), CLAUDE_CONFIG_DIR=~/.claude-bench, 2 workers. sol-6.1-cli: GPT-6.1 Sol (gpt-6.1-sol) via Codex CLI 0.163.0 exec, reasoning effort xhigh and sandbox read-only (both confirmed in the run header), approval on-request (forced by workspace policy), CODEX_HOME=~/.codex-bench, 4 workers. Full command lines are in the batch manifest.
- Run size per model (questions, and the share run on sol-6.1-cli, `probe2.sol_fraction`): opus-5.5-cli: 1,440 questions (main stratum: 675 F-readout, 300 F-gene, 135 F-neighbour; flagged stratum: 180 F-readout, 120 F-gene, 30 F-neighbour), × 2 versions × k = 2 = 5,760 calls. sol-6.1-cli: probe2.sol_fraction = 0.5, sampled with the same strata (within each family × stratum × cell × bin, half of the questions with halves rounded up): 817 questions (main: 405 F-readout, 150 F-gene, 75 F-neighbour; flagged: 101 F-readout, 68 F-gene, 18 F-neighbour), × 2 versions × k = 2 = 3,268 calls. Counts from the final dry run; every stratum cell filled.
- Per-model date cutoffs and PMID cutoffs (`models[].cutoff_date`; density_<date>_meta.json): opus-5.5-cli: 2026-07-01, PMID cutoff 42378835. sol-6.1-cli: 2026-05-01, PMID cutoff 42060948.
- Strata bins: quintiles of log10 fractional density at the earliest model cutoff over all QC-passing genes; each model is analysed against its own cutoff's log density. Confirmed.
- GO releases (D-021): archived GOA human release closest before each cutoff; main annotation baseline includes IEA, no-IEA variant secondary. Confirmed: release 234 (generated 2026-04-30) for sol-6.1-cli; release 236 (generated 2026-06-17) for opus-5.5-cli.
- Families included (`probe2.families`): readout, gene, neighbour. F-neighbour main-stratum results are descriptive (D-023); flagged F-neighbour items are reported descriptively with the positive control.
- Donor-agreement filter (`probe2.agreement.chosen`): for F-gene and F-neighbour by the D-016 order; for F-readout jointly with the strata by the D-023 order (effect-size terciles under the strictest filter that fills them, ahead of any filter without terciles). F-readout: d12_d34 with effect-size terciles (D-023: all_three cannot fill terciles; d12_d34 fills them at 5 per cell). F-gene: all_three (first in the D-016 order that fills 10 per cell; capacity 34–83). F-neighbour: all_three (first in the D-016 order that fills 5 / 2 / 2 per cell).
- F-readout: R (`probe2.readout.R`) R = 50; strata with or without the target effect-size tercile by the D-016/D-019 rule. Tercile.
- F-gene: DE-count ratio (`probe2.gene.ratio`) ratio = 2; expression match tolerance in log2 target baseMean (`probe2.gene.match_log2_tol`) match_log2_tol = 0.5.
- F-neighbour: informative readouts per condition (`n_inf`, D-020) n\_inf = 500; options and distractors also exclude Phase 0 genes (`options_exclude_phase0`) yes; minimum DE genes (`min_de`) min\_de = 30; minimum self-reliability (`min_self_corr`) min_self_corr = 50th percentile of covered perturbations' self-reliability for the chosen split (all_three), n_inf and condition (`min_self_corr_quantile` 0.5; dry-run values Rest 0.213, Stim8hr 0.244, Stim48hr 0.262; absolute values recorded in the manifest); margin over the best distractor = 25th percentile of the condition's main-stratum candidate items' gaps (`margin_quantile` 0.25; dry-run values Rest 0.583, Stim8hr 0.513, Stim48hr 0.505); GO term size limit for the discovery tier (`go_max_genes`) go_max_genes = 500; distractor expression match (`match_log2_tol`) match_log2_tol = 1.0.
- Questions per stratum cell per bin, per family (`probe2.<family>.per_cell`): readout 5; gene 10; neighbour 5 (easy) / 2 (hard) / 2 (discovery).
- Maximum questions per gene per family (`probe2.max_per_gene`): 3 
- Samples per prompt k (`run.samples`) k = 2, and how samples are combined for the primary estimand (`probe2.combine_samples`): mean_brier (brier_of_mean reported as secondary)
- Flagged genes (`config/flagged_genes.txt`, 114) form a separate positive-control stratum, pooled across bins (D-022); questions per cell (`probe2.flagged_per_cell`) readout 20; gene 20; neighbour 10 (easy tier only), pooled across bins. Phase 0 genes (522) are excluded as targets.

## Design

- Families (no data shown to the model; `src/dgbench/probe2.py`):
  - F-readout: does readout R decrease, stay unchanged or increase when G is knocked down? Readouts come from the whole transcriptome; decreased/increased from G's significant effects; unchanged readouts respond to at least R other perturbations in the same condition but not to G. Strata: condition × label × target effect-size tercile (fallback: condition × label; D-016, D-019).
  - F-gene: which of two knockdowns (same bin and condition, matched on target expression) changes more genes? Strata: condition × label.
  - F-neighbour: which of four knockdowns has the LFC profile (over the n_inf most responsive readouts) most similar to G's? Tiers easy, hard and discovery (D-018, D-020). Strata: condition, per tier.
- Every question has a named and a hidden prompt, identical except that the knocked-down gene (both genes in F-gene) is "a gene whose identity is hidden". Run order is shuffled so a question's calls are never adjacent. Each prompt is asked k times.
- Truth: combined-donor DE with the Phase 0 thresholds, kept only where the chosen donor-pair halves agree (D-016).
- Every density bin has the same count in each stratum cell; cells that cannot fill in every bin are dropped and reported.

## Primary estimand

Per question, gain in skill points (D-024) = (Brier(hidden) − Brier(named)) / uniform Brier for the question's family (F-readout 2/3, F-gene 1/2, F-neighbour 3/4), with samples combined as pre-registered above. Gate A's pooled gain weights F-readout and F-gene equally: the mean of the two family means. Analysis B regresses the per-question skill-point gains, with family as a covariate. Per-family results, per density bin and pooled, are reported descriptively. All CIs are 95% from a bootstrap that resamples genes (a question's first gene) with all their questions.

## Analysis plan

- A (gate): pooled gain, main stratum, F-readout and F-gene, per model.
- F-neighbour main-stratum results (all tiers) are descriptive and outside analyses A and B (D-023).
- B (only if A passes): slope of the gain on the model's own log density, with covariates effect size (n_downstream), log2 target expression, knockdown efficiency (on-target effect size) and reliability (cross-donor correlation); gene-clustered bootstrap.
- C (descriptive): gain by F-neighbour tier.
- F-gene gain by DE-count ratio band (2–4, 4–10, >10), descriptive.
- Secondary: Brier skill per version; F-readout AUC on P(changed) and direction accuracy among changed; ECE and a Murphy decomposition (10 forecast bins).
- Baseline ladder, each a calibrated probabilistic forecast scored like the models: uniform and label frequencies; the hidden version; fame-only (log density + target expression); annotation-only (GO from each model's archived release, IEA included; no-IEA variant secondary). Fame-only and annotation-only are fitted on strata-balanced questions about genes outside the batch: multinomial logistic for F-readout and F-gene; conditional logit over the four options for F-neighbour (for annotation-only, a softmax over GO Jaccard with its temperature fitted). Each model's named gain beyond the fame-only and annotation-only rungs is reported alongside named − hidden.
- Secondary density measure: T-cell literature (gene2pubmed papers with the "T-Lymphocytes" MeSH heading, exploded), reported descriptively.

## Predictions

The scorer applies these mechanically to the pre-registered combine method. All gains are in skill points (D-024).
- Scope of A, B and the top-bin check: main stratum, F-readout and F-gene.
- A passes if the lower 95% CI bound of the pooled gain (mean of the F-readout and F-gene family means) exceeds `min_pooled_gain`.
- B passes if the lower 95% CI bound of the slope of per-question gains on the model's own log density, adjusted for the covariates and family, exceeds `min_slope` (evaluated only if A passes).
- The top density bin's gain (mean of the two family means within the bin) has a lower 95% CI bound of at least `top_bin_min_gain`.
- Positive control: the flagged stratum's pooled gain over F-readout and F-gene (mean of the two family means) has a lower 95% CI bound of at least `positive_control_min_gain`. It is excluded from A and B.

```yaml
predictions:
  min_pooled_gain: 0.01
  min_slope: 0.0
  top_bin_min_gain: 0.02
  positive_control_min_gain: 0.02
```

Expected direction and reasoning, per model:
opus-5.5-cli: small positive pooled gain, larger on F-gene than F-readout and larger in the flagged stratum than the main stratum; modest positive slope with density. Its training data extend past the 28 May 2026 data release, so part of any gain may reflect exposure to this screen; if so, its gain should exceed Sol's on the same questions.
sol-6.1-cli: same pattern if gene knowledge comes from the literature. Its 30 April 2026 cutoff precedes the data release (not the December 2025 preprint), so a clearly smaller gain than Opus's would point to exposure rather than literature.

## Outcome interpretation (fixed before data)

| Pattern | Reading |
|---|---|
| named ≈ hidden everywhere | No usable gene-specific information in these formats; prior knowledge does not inform these assay outcomes, and density cannot act through priors. |
| named > hidden mainly for well-studied genes | Gene-specific predictive information rises with literature coverage, the premise of the density axis. |
| named > hidden equally across density | Models hold useful gene-specific information, but publication volume does not explain it (e.g. sequence, family or annotation-level knowledge). |
| strong F-neighbour similarity but weak F-readout prediction (descriptive) | Models know functional relationships better than assay-specific outcomes. |
| strong easy tier but negligible hard tier (descriptive) | Gains come mainly from broad functional annotation rather than detailed phenotype knowledge. |
| positive control fails | The formats cannot capture gene knowledge even for the best-known genes; main-stratum A and B are uninterpretable. |
| opus-5.5-cli gain clearly exceeds sol-6.1-cli's | Exposure to the released dataset is a candidate explanation for Opus's gain; literature-based readings apply only to what both models share. |

## Decision rule

Evaluated on opus-5.5-cli, the full-size run. sol-6.1-cli is the exposure contrast: its checks are reported but do not change the branch.
1. Positive control fails: stop. Record the result; redesign the formats before Phase 1.
2. Positive control passes, A fails: the main stratum shows no usable gene-specific signal. The density axis is unsupported for prior knowledge. Phase 1 proceeds only under a new pre-registration that measures data-attributable skill without density as the manipulated variable.
3. A passes; B fails, or B passes but the top-bin check fails: gene identity helps, but not in proportion to literature volume. Phase 1 keeps the named/hidden contrast and treats density as secondary.
4. A, B and the top-bin check all pass: proceed to Phase 1 with density as the manipulated variable.
In branches 3 and 4, if Opus's pooled gain exceeds Sol's (95% CI of the paired difference on shared questions excludes 0), Phase 1 must include a second model whose cutoff precedes the data release, and the paper reports the exposure contrast.
## Handling

- Parse failures: scored as the uniform forecast and counted per model, family and bin.
- Infrastructure errors: excluded from scoring and rerun until none remain; the report is final only then.
- The batch is never regenerated. Any further batch needs a recorded reason or a new pre-registration.

## Deviations

None at commit. Later deviations go in `docs/DECISIONS.md` with a date.
