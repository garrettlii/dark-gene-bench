# Pre-registration

Every batch is generated from a pre-registration file in this folder. The batch generator checks that the file

1. has no unfilled placeholders,
2. is committed with no local changes, and
3. is on a remote branch (pushed), which gives an external timestamp.

It then records the commit hash in the batch manifest and appends the batch to `truth_root/ledger.jsonl`. A second batch under the same pre-registration commit is refused unless `--additional-batch-reason` is given, and the reason is logged.

## Workflow

1. Copy the template for the phase (for Phase 0, edit `phase0_prior_probe.md` directly).
2. Fill in every field marked FILL, including the numeric thresholds in the `predictions` YAML block, which the scorer applies mechanically.
3. Commit and push. Only then generate the batch.
4. After scoring, do not edit the file. Record deviations in `docs/DECISIONS.md` and write a new pre-registration for any new batch.

Thresholds and predictions are set by the human authors, not by any evaluated model.
