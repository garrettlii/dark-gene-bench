# Pre-registration: Phase 0 prior-only probe

Status: draft. Replace every FILL field, then commit and push before generating the batch.

## Purpose

Manipulation check for the density axis. Do models' no-data answers about knockdown effects get worse as a gene's literature density falls? If not, density does not separate prior knowledge from analysis and the design stops before Phase 1.

## Fixed inputs

Recorded automatically in the batch manifest: config hash and full config, dataset checksum, this file's commit hash, seed.

- Density cutoff date (`density.cutoff_date`) and resolved PMID cutoff: 2026-05-01, the day after the earliest knowledge cutoff among the evaluated models (GPT-6.1 Sol, 2026-04-30; Claude Opus 5.5 reliable-knowledge and training-data cutoffs are both June 2026; D-012). PMID cutoff 42060948 (smallest PMID entered that day after ignoring PMIDs more than 1,000,000 below the day's median as re-dated old records; 5 records ignored; D-008), resolved 2026-10-23 via NCBI E-utilities, truncated: false. gene2pubmed downloaded 2026-10-22, SHA-256 894da35d6648.
- Evaluated models and backends (API or CLI, with model IDs): opus-5.5-cli and sol-6.1-cli. opus-5.5-cli: Claude Opus 5.5 (claude-opus-5-5) via Claude Code 2.1.309 in print mode; all tools disallowed; effort xhigh; CLAUDE_CONFIG_DIR=~/.claude-bench (no plugins, MCP servers or CLAUDE.md; nine account-synced skills are present in that directory but cannot run with all tools disallowed). sol-6.1-cli: GPT-6.1 Sol (gpt-6.1-sol) via codex-cli 0.163.0 exec; shell, unified exec, apps, plugins, browser, image and multi-agent tools disabled; web search off; no MCP servers configured; read-only sandbox; reasoning effort xhigh; ephemeral sessions; CODEX_HOME=~/.codex-bench (no AGENTS.md). Added before any batch (D-011).
- Number of density bins, and the rule if ties at low density collapse bins: 5 quintiles of log10 fractional density over QC-passing genes; genes with no papers fall in the lowest quintile; tied genes share a bin; bins reported as produced (5 in the feasibility report). A separate zero-paper bin (D-007) was dropped before any model call because it had too few up/down candidates for label balance (D-010).
- Questions per bin and maximum per gene: 120 per bin (40 per label), at most 3 per gene; the largest of 120, 105, 90, 75 and 60 for which the dry run showed no bin, including bin 0, below quota.
- Genes named in the dataset paper (`config/flagged_genes.txt`) filled in and excluded: Yes. 114 genes named as knockdown targets with reported effects anywhere in the text layers (main text, figure captions and methods; references and supplementary files excluded) of the preprint (bioRxiv, DOI 10.64898/2025.12.23.696273, v1) and the Cell article (DOI 10.1016/j.cell.2026.08.002); unclear target-or-readout calls were flagged; figure panels are images, so names shown only inside panels were not captured; 114 are in the screen and 102 pass QC; all are excluded from sampling (probe.exclude_flagged_genes: true).

Readout panel, condition labels and truth thresholds are as in `config/default.yaml` at this commit.

## Design

- Family F1, single-readout version: "when gene G is knocked down in condition C, does readout R decrease, stay unchanged, or increase?"
- Provisional truth: combined-donor differential-expression results; borderline cases dropped by the configured thresholds.
- Labels balanced within each bin; prompts state that the three answers are about equally common.
- No data and no tools; one call per question.

## Primary outcome

Multi-class Brier skill relative to the batch's label frequencies, per density bin and model, with 95% CIs from a bootstrap that resamples genes within bins. Secondary: accuracy, top-label calibration error, parse-failure rate.

## Predictions

The scorer applies these mechanically:
- P1a passes if the top bin's lower 95% CI bound is at least `top_bin_min_skill`.
- P1b passes if the bottom bin's point estimate is at most `bottom_bin_max_skill`.
- P1c passes if the lower 95% CI bound of the slope of skill on bin index exceeds `min_slope`.

```yaml
predictions:
  top_bin_min_skill: 0.1
  bottom_bin_max_skill: 0.01
  min_slope: 0.02
```

Expected direction and reasoning: I predict that Claude Opus 5.5 and ChatGPT 6.1 Sol will exhibit a positive relationship between gene literature density and prior-only prediction skill. For well-studied genes, the model may leverage previously learned gene functions, regulatory relationships, and biological mechanisms to predict knockdown effects. For poorly studied genes, this information is expected to be less accessible or less complete, leading to performance closer to the label-frequency baseline. We expect the strongest skill in the highest-density bin and a positive overall density gradient. Since Sol's cutoff date is earlier (April) than Opus', it is predicted that Opus' greater knowledge base will enable it to produce slightly better predictions for genes with little-to-no literature.

## Decision rule

- Proceed to Phase 1 if P1a and P1c pass for at least one model.
- If P1a and P1c pass but P1b fails, the least-studied bin is not dark enough: Write a new pre-registration for a Phase 0b batch restricted to the zero-paper genes, with readouts drawn from each gene's transcriptome-wide differential expression instead of the fixed T-cell panel, which these genes rarely affect; label-balanced as here. Phase 1 waits for its result.
- If P1a or P1c fails for every model, stop and record the result in `docs/DECISIONS.md`.

## Handling

- Responses that arrive but cannot be parsed are scored as the uniform forecast and counted.
- Infrastructure errors (no response: quota, auth, timeouts) are excluded, rerun, and counted.
- The batch is never regenerated. Any further batch needs a recorded reason or a new pre-registration.

## Deviations

None at commit. Later deviations go in `docs/DECISIONS.md` with a date.
