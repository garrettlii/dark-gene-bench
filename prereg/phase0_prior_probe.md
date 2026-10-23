# Pre-registration: Phase 0 prior-only probe

Status: draft. Replace every FILL field, then commit and push before generating the batch.

## Purpose

Manipulation check for the density axis. Do models' no-data answers about knockdown effects get worse as a gene's literature density falls? If not, density does not separate prior knowledge from analysis and the design stops before Phase 1.

## Fixed inputs

Recorded automatically in the batch manifest: config hash and full config, dataset checksum, this file's commit hash, seed.

- Density cutoff date (`density.cutoff_date`) and resolved PMID cutoff: <<FILL: date and PMID>>
- Evaluated models and backends (API or CLI, with model IDs): <<FILL: list>>
- Number of density bins, and the rule if ties at low density collapse bins: <<FILL: e.g. 5 quintiles; ties kept together and bins reported as produced>>
- Questions per bin and maximum per gene: <<FILL: e.g. 120 and 3>>
- Genes named in the dataset paper (`config/flagged_genes.txt`) filled in and excluded: <<FILL: yes/no, count>>

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
  top_bin_min_skill: <<FILL: number>>
  bottom_bin_max_skill: <<FILL: number>>
  min_slope: <<FILL: number>>
```

Expected direction and reasoning: <<FILL: one or two sentences per model>>

## Decision rule

- Proceed to Phase 1 if P1a and P1c pass for at least one model.
- If P1a and P1c pass but P1b fails, the least-studied bin is not dark enough: <<FILL: e.g. split the bottom bin further before Phase 1>>.
- If P1a or P1c fails for every model, stop and record the result in `docs/DECISIONS.md`.

## Handling

- Responses that arrive but cannot be parsed are scored as the uniform forecast and counted.
- Infrastructure errors (no response: quota, auth, timeouts) are excluded, rerun, and counted.
- The batch is never regenerated. Any further batch needs a recorded reason or a new pre-registration.

## Deviations

None at commit. Later deviations go in `docs/DECISIONS.md` with a date.
