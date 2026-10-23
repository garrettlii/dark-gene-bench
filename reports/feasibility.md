# Feasibility report

Generated 2026-10-23. Aggregate counts only.

## Perturbations

- rows (perturbation x condition): 33983
- unique targets: 11526
- conditions: Rest, Stim48hr, Stim8hr

Target mapping to Entrez GeneID:
- ensembl: 11460
- symbol: 62
- synonym: 2
- unmapped: 2

QC (rows):
- flag_neighboring_gene_KD: 2619 true
- flag_distal_offtarget_flag: 433 true
- flag_low_target_gex: 7806 true
- qc_pass: 23317 of 33983
  - Rest: 7640 pass
  - Stim48hr: 7939 pass
  - Stim8hr: 7738 pass

Genes passing QC in at least one condition: 8436
Flagged (named in the dataset paper): 114

## Literature density by bin (QC-passing genes; bin 0 = least studied)

| bin | genes | papers min | papers median | papers max | share with 0 papers | flagged | effect size median | on-target KD significant (mean share of QC conditions) |
|---|---|---|---|---|---|---|---|---|
| 0 | 1688 | 0 | 4 | 56 | 0.07 | 4 | 1.0 | 0.73 |
| 1 | 1687 | 3 | 13 | 116 | 0.00 | 9 | 2.0 | 0.79 |
| 2 | 1687 | 10 | 29 | 129 | 0.00 | 7 | 2.0 | 0.79 |
| 3 | 1687 | 26 | 67 | 247 | 0.00 | 20 | 2.0 | 0.79 |
| 4 | 1687 | 75 | 262 | 16629 | 0.00 | 62 | 2.0 | 0.77 |

Readout panel: 14 of 14 present
