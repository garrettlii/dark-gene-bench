# Probe v2 dry run

Generated 2026-10-23. Aggregate counts only; nothing written to runs_root or truth_root.
Capacities: main stratum = the largest per-cell count every cell reaches in every bin at one item per gene per cell; flagged stratum = distinct genes in the smallest cell, pooled over bins (D-022).

## Scope and Phase 0 exclusion (genes per strata bin)

Phase 0 genes excluded from sampling: 522.

| bin | qc_genes | covered | minus_phase0 | main_targets | flagged_targets |
|---|---|---|---|---|---|
| 0 | 1688 | 283 | 227 | 223 | 4 |
| 1 | 1687 | 381 | 326 | 319 | 7 |
| 2 | 1687 | 408 | 350 | 343 | 7 |
| 3 | 1687 | 408 | 349 | 332 | 17 |
| 4 | 1687 | 441 | 384 | 335 | 49 |

## GO annotations (archived release closest before each cutoff; D-021)

- cutoff 2026-05-01: release 234, date_generated 2026-04-30, annotations 815574, kept 815574, IEA 162953, citing_dataset_paper 0, genes_with_terms 19552
- cutoff 2026-05-01 (no-IEA variant): release 234, date_generated 2026-04-30, annotations 815574, kept 652621, IEA 162953, citing_dataset_paper 0, genes_with_terms 19063
- cutoff 2026-07-01: release 236, date_generated 2026-06-17, annotations 824764, kept 824764, IEA 163042, citing_dataset_paper 0, genes_with_terms 19553
- cutoff 2026-07-01 (no-IEA variant): release 236, date_generated 2026-06-17, annotations 824764, kept 661722, IEA 163042, citing_dataset_paper 0, genes_with_terms 19081

## F-readout (strata: condition x label x target effect-size tercile, D-019)

### R=5, top_k=all: agreement attrition (main, candidates)

| bin | label | before | after_all_three |
|---|---|---|---|
| 0 | decreased | 11886 | 232 |
| 0 | increased | 25314 | 219 |
| 0 | unchanged | 1205491 | 124112 |
| 1 | decreased | 22179 | 361 |
| 1 | increased | 40119 | 746 |
| 1 | unchanged | 1895947 | 210109 |
| 2 | decreased | 28699 | 745 |
| 2 | increased | 56380 | 1670 |
| 2 | unchanged | 1970758 | 190952 |
| 3 | decreased | 26871 | 430 |
| 3 | increased | 52671 | 1365 |
| 3 | unchanged | 2007160 | 189910 |
| 4 | decreased | 30956 | 646 |
| 4 | increased | 54033 | 1234 |
| 4 | unchanged | 2296988 | 253671 |

### R=5, top_k=50: agreement attrition (main, candidates)

| bin | label | before | after_all_three |
|---|---|---|---|
| 0 | decreased | 3320 | 137 |
| 0 | increased | 8132 | 213 |
| 0 | unchanged | 1205491 | 124112 |
| 1 | decreased | 5919 | 261 |
| 1 | increased | 13272 | 659 |
| 1 | unchanged | 1895947 | 210109 |
| 2 | decreased | 6112 | 478 |
| 2 | increased | 14613 | 1039 |
| 2 | unchanged | 1970758 | 190952 |
| 3 | decreased | 6290 | 290 |
| 3 | increased | 14859 | 918 |
| 3 | unchanged | 2007160 | 189910 |
| 4 | decreased | 7490 | 534 |
| 4 | increased | 15147 | 861 |
| 4 | unchanged | 2296988 | 253671 |

### R=20, top_k=all, agreement all_three, main, with effect tercile: distinct genes per cell and bin

| condition | label | eff_class | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|---|---|
| Rest | decreased | 0 | 4.0 | 12.0 | 9.0 | 3.0 | 7.0 |
| Rest | decreased | 1 | 4.0 | 9.0 | 3.0 | 7.0 | 10.0 |
| Rest | decreased | 2 | 5.0 | 9.0 | 17.0 | 13.0 | 17.0 |
| Rest | increased | 0 | 0.0 | 5.0 | 4.0 | 3.0 | 5.0 |
| Rest | increased | 1 | 3.0 | 11.0 | 7.0 | 9.0 | 13.0 |
| Rest | increased | 2 | 5.0 | 11.0 | 22.0 | 22.0 | 19.0 |
| Rest | unchanged | 0 | 50.0 | 62.0 | 70.0 | 71.0 | 71.0 |
| Rest | unchanged | 1 | 41.0 | 68.0 | 58.0 | 60.0 | 77.0 |
| Rest | unchanged | 2 | 28.0 | 42.0 | 61.0 | 47.0 | 48.0 |
| Stim48hr | decreased | 0 | 4.0 | 7.0 | 7.0 | 4.0 | 5.0 |
| Stim48hr | decreased | 1 | 6.0 | 6.0 | 6.0 | 10.0 | 12.0 |
| Stim48hr | decreased | 2 | 9.0 | 22.0 | 24.0 | 15.0 | 30.0 |
| Stim48hr | increased | 0 | 4.0 | 3.0 | 7.0 | 3.0 | 4.0 |
| Stim48hr | increased | 1 | 3.0 | 8.0 | 7.0 | 9.0 | 10.0 |
| Stim48hr | increased | 2 | 11.0 | 15.0 | 28.0 | 18.0 | 32.0 |
| Stim48hr | unchanged | 0 | 46.0 | 76.0 | 68.0 | 84.0 | 78.0 |
| Stim48hr | unchanged | 1 | 41.0 | 60.0 | 69.0 | 76.0 | 76.0 |
| Stim48hr | unchanged | 2 | 22.0 | 49.0 | 56.0 | 42.0 | 57.0 |
| Stim8hr | decreased | 0 | 6.0 | 9.0 | 9.0 | 8.0 | 13.0 |
| Stim8hr | decreased | 1 | 4.0 | 12.0 | 12.0 | 9.0 | 11.0 |
| Stim8hr | decreased | 2 | 7.0 | 15.0 | 21.0 | 20.0 | 23.0 |
| Stim8hr | increased | 0 | 3.0 | 4.0 | 3.0 | 3.0 | 7.0 |
| Stim8hr | increased | 1 | 9.0 | 15.0 | 11.0 | 12.0 | 18.0 |
| Stim8hr | increased | 2 | 9.0 | 21.0 | 28.0 | 32.0 | 26.0 |
| Stim8hr | unchanged | 0 | 55.0 | 74.0 | 77.0 | 79.0 | 67.0 |
| Stim8hr | unchanged | 1 | 35.0 | 63.0 | 68.0 | 68.0 | 82.0 |
| Stim8hr | unchanged | 2 | 24.0 | 38.0 | 49.0 | 52.0 | 57.0 |

### R=20, top_k=all: agreement attrition (main, candidates)

| bin | label | before | after_all_three |
|---|---|---|---|
| 0 | decreased | 11886 | 232 |
| 0 | increased | 25314 | 219 |
| 0 | unchanged | 682655 | 65533 |
| 1 | decreased | 22179 | 361 |
| 1 | increased | 40119 | 746 |
| 1 | unchanged | 1071872 | 110287 |
| 2 | decreased | 28699 | 745 |
| 2 | increased | 56380 | 1670 |
| 2 | unchanged | 1112212 | 100887 |
| 3 | decreased | 26871 | 430 |
| 3 | increased | 52671 | 1365 |
| 3 | unchanged | 1135206 | 100406 |
| 4 | decreased | 30956 | 646 |
| 4 | increased | 54033 | 1234 |
| 4 | unchanged | 1290405 | 133270 |

### R=20, top_k=all, agreement d12_d34, main, with effect tercile: distinct genes per cell and bin

| condition | label | eff_class | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|---|---|
| Rest | decreased | 0 | 5.0 | 18.0 | 10.0 | 10.0 | 7.0 |
| Rest | decreased | 1 | 6.0 | 22.0 | 9.0 | 14.0 | 20.0 |
| Rest | decreased | 2 | 8.0 | 18.0 | 27.0 | 25.0 | 24.0 |
| Rest | increased | 0 | 5.0 | 11.0 | 11.0 | 7.0 | 12.0 |
| Rest | increased | 1 | 7.0 | 20.0 | 15.0 | 17.0 | 23.0 |
| Rest | increased | 2 | 8.0 | 21.0 | 35.0 | 31.0 | 30.0 |
| Rest | unchanged | 0 | 50.0 | 62.0 | 70.0 | 71.0 | 71.0 |
| Rest | unchanged | 1 | 41.0 | 68.0 | 58.0 | 60.0 | 77.0 |
| Rest | unchanged | 2 | 28.0 | 42.0 | 61.0 | 49.0 | 48.0 |
| Stim48hr | decreased | 0 | 5.0 | 12.0 | 13.0 | 18.0 | 11.0 |
| Stim48hr | decreased | 1 | 9.0 | 13.0 | 12.0 | 26.0 | 20.0 |
| Stim48hr | decreased | 2 | 14.0 | 29.0 | 46.0 | 26.0 | 42.0 |
| Stim48hr | increased | 0 | 9.0 | 10.0 | 15.0 | 10.0 | 7.0 |
| Stim48hr | increased | 1 | 7.0 | 21.0 | 15.0 | 22.0 | 22.0 |
| Stim48hr | increased | 2 | 15.0 | 29.0 | 43.0 | 27.0 | 44.0 |
| Stim48hr | unchanged | 0 | 46.0 | 76.0 | 68.0 | 84.0 | 78.0 |
| Stim48hr | unchanged | 1 | 41.0 | 60.0 | 69.0 | 76.0 | 76.0 |
| Stim48hr | unchanged | 2 | 22.0 | 49.0 | 56.0 | 42.0 | 58.0 |
| Stim8hr | decreased | 0 | 11.0 | 16.0 | 13.0 | 18.0 | 17.0 |
| Stim8hr | decreased | 1 | 6.0 | 18.0 | 17.0 | 16.0 | 21.0 |
| Stim8hr | decreased | 2 | 11.0 | 20.0 | 29.0 | 31.0 | 33.0 |
| Stim8hr | increased | 0 | 7.0 | 10.0 | 12.0 | 8.0 | 13.0 |
| Stim8hr | increased | 1 | 12.0 | 24.0 | 26.0 | 29.0 | 27.0 |
| Stim8hr | increased | 2 | 15.0 | 26.0 | 36.0 | 39.0 | 39.0 |
| Stim8hr | unchanged | 0 | 55.0 | 74.0 | 77.0 | 79.0 | 67.0 |
| Stim8hr | unchanged | 1 | 35.0 | 63.0 | 68.0 | 68.0 | 82.0 |
| Stim8hr | unchanged | 2 | 25.0 | 38.0 | 50.0 | 53.0 | 57.0 |

### R=20, top_k=all, agreement d14_d23, main, with effect tercile: distinct genes per cell and bin

| condition | label | eff_class | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|---|---|
| Rest | decreased | 0 | 7.0 | 16.0 | 12.0 | 10.0 | 9.0 |
| Rest | decreased | 1 | 8.0 | 13.0 | 8.0 | 14.0 | 22.0 |
| Rest | decreased | 2 | 7.0 | 15.0 | 29.0 | 22.0 | 27.0 |
| Rest | increased | 0 | 4.0 | 13.0 | 12.0 | 7.0 | 13.0 |
| Rest | increased | 1 | 7.0 | 17.0 | 15.0 | 17.0 | 25.0 |
| Rest | increased | 2 | 8.0 | 19.0 | 31.0 | 31.0 | 26.0 |
| Rest | unchanged | 0 | 50.0 | 62.0 | 70.0 | 71.0 | 71.0 |
| Rest | unchanged | 1 | 41.0 | 68.0 | 58.0 | 60.0 | 77.0 |
| Rest | unchanged | 2 | 28.0 | 42.0 | 61.0 | 49.0 | 48.0 |
| Stim48hr | decreased | 0 | 7.0 | 13.0 | 11.0 | 12.0 | 12.0 |
| Stim48hr | decreased | 1 | 9.0 | 11.0 | 12.0 | 16.0 | 17.0 |
| Stim48hr | decreased | 2 | 13.0 | 36.0 | 34.0 | 22.0 | 43.0 |
| Stim48hr | increased | 0 | 6.0 | 6.0 | 13.0 | 10.0 | 6.0 |
| Stim48hr | increased | 1 | 9.0 | 21.0 | 12.0 | 19.0 | 22.0 |
| Stim48hr | increased | 2 | 14.0 | 29.0 | 41.0 | 30.0 | 41.0 |
| Stim48hr | unchanged | 0 | 46.0 | 76.0 | 68.0 | 84.0 | 78.0 |
| Stim48hr | unchanged | 1 | 41.0 | 60.0 | 69.0 | 76.0 | 76.0 |
| Stim48hr | unchanged | 2 | 22.0 | 49.0 | 56.0 | 42.0 | 58.0 |
| Stim8hr | decreased | 0 | 11.0 | 14.0 | 14.0 | 14.0 | 15.0 |
| Stim8hr | decreased | 1 | 7.0 | 19.0 | 18.0 | 18.0 | 19.0 |
| Stim8hr | decreased | 2 | 12.0 | 21.0 | 32.0 | 32.0 | 31.0 |
| Stim8hr | increased | 0 | 6.0 | 14.0 | 12.0 | 8.0 | 11.0 |
| Stim8hr | increased | 1 | 13.0 | 24.0 | 28.0 | 29.0 | 29.0 |
| Stim8hr | increased | 2 | 14.0 | 26.0 | 37.0 | 45.0 | 38.0 |
| Stim8hr | unchanged | 0 | 55.0 | 74.0 | 77.0 | 79.0 | 67.0 |
| Stim8hr | unchanged | 1 | 35.0 | 63.0 | 68.0 | 68.0 | 82.0 |
| Stim8hr | unchanged | 2 | 25.0 | 38.0 | 50.0 | 53.0 | 57.0 |

### R=20, top_k=50, agreement all_three, main, with effect tercile: distinct genes per cell and bin

| condition | label | eff_class | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|---|---|
| Rest | decreased | 0 | 4.0 | 12.0 | 9.0 | 3.0 | 7.0 |
| Rest | decreased | 1 | 4.0 | 9.0 | 3.0 | 7.0 | 10.0 |
| Rest | decreased | 2 | 5.0 | 9.0 | 16.0 | 12.0 | 17.0 |
| Rest | increased | 0 | 0.0 | 5.0 | 4.0 | 3.0 | 5.0 |
| Rest | increased | 1 | 3.0 | 11.0 | 7.0 | 9.0 | 13.0 |
| Rest | increased | 2 | 5.0 | 11.0 | 22.0 | 22.0 | 18.0 |
| Rest | unchanged | 0 | 50.0 | 62.0 | 70.0 | 71.0 | 71.0 |
| Rest | unchanged | 1 | 41.0 | 68.0 | 58.0 | 60.0 | 77.0 |
| Rest | unchanged | 2 | 28.0 | 42.0 | 61.0 | 47.0 | 48.0 |
| Stim48hr | decreased | 0 | 4.0 | 7.0 | 7.0 | 4.0 | 5.0 |
| Stim48hr | decreased | 1 | 6.0 | 6.0 | 5.0 | 10.0 | 12.0 |
| Stim48hr | decreased | 2 | 9.0 | 22.0 | 24.0 | 12.0 | 30.0 |
| Stim48hr | increased | 0 | 4.0 | 3.0 | 7.0 | 3.0 | 4.0 |
| Stim48hr | increased | 1 | 3.0 | 8.0 | 7.0 | 9.0 | 9.0 |
| Stim48hr | increased | 2 | 11.0 | 15.0 | 28.0 | 18.0 | 31.0 |
| Stim48hr | unchanged | 0 | 46.0 | 76.0 | 68.0 | 84.0 | 78.0 |
| Stim48hr | unchanged | 1 | 41.0 | 60.0 | 69.0 | 76.0 | 76.0 |
| Stim48hr | unchanged | 2 | 22.0 | 49.0 | 56.0 | 42.0 | 57.0 |
| Stim8hr | decreased | 0 | 6.0 | 9.0 | 9.0 | 8.0 | 13.0 |
| Stim8hr | decreased | 1 | 4.0 | 12.0 | 12.0 | 9.0 | 11.0 |
| Stim8hr | decreased | 2 | 7.0 | 15.0 | 20.0 | 17.0 | 22.0 |
| Stim8hr | increased | 0 | 3.0 | 4.0 | 3.0 | 3.0 | 7.0 |
| Stim8hr | increased | 1 | 9.0 | 14.0 | 11.0 | 12.0 | 18.0 |
| Stim8hr | increased | 2 | 9.0 | 21.0 | 28.0 | 32.0 | 26.0 |
| Stim8hr | unchanged | 0 | 55.0 | 74.0 | 77.0 | 79.0 | 67.0 |
| Stim8hr | unchanged | 1 | 35.0 | 63.0 | 68.0 | 68.0 | 82.0 |
| Stim8hr | unchanged | 2 | 24.0 | 38.0 | 49.0 | 52.0 | 57.0 |

### R=20, top_k=50: agreement attrition (main, candidates)

| bin | label | before | after_all_three |
|---|---|---|---|
| 0 | decreased | 3320 | 137 |
| 0 | increased | 8132 | 213 |
| 0 | unchanged | 682655 | 65533 |
| 1 | decreased | 5919 | 261 |
| 1 | increased | 13272 | 659 |
| 1 | unchanged | 1071872 | 110287 |
| 2 | decreased | 6112 | 478 |
| 2 | increased | 14613 | 1039 |
| 2 | unchanged | 1112212 | 100887 |
| 3 | decreased | 6290 | 290 |
| 3 | increased | 14859 | 918 |
| 3 | unchanged | 1135206 | 100406 |
| 4 | decreased | 7490 | 534 |
| 4 | increased | 15147 | 861 |
| 4 | unchanged | 1290405 | 133270 |

### R=20, top_k=50, agreement d12_d34, main, with effect tercile: distinct genes per cell and bin

| condition | label | eff_class | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|---|---|
| Rest | decreased | 0 | 5.0 | 18.0 | 10.0 | 10.0 | 7.0 |
| Rest | decreased | 1 | 6.0 | 21.0 | 9.0 | 14.0 | 20.0 |
| Rest | decreased | 2 | 8.0 | 16.0 | 26.0 | 22.0 | 24.0 |
| Rest | increased | 0 | 4.0 | 11.0 | 11.0 | 7.0 | 12.0 |
| Rest | increased | 1 | 7.0 | 20.0 | 15.0 | 17.0 | 23.0 |
| Rest | increased | 2 | 8.0 | 21.0 | 34.0 | 31.0 | 30.0 |
| Rest | unchanged | 0 | 50.0 | 62.0 | 70.0 | 71.0 | 71.0 |
| Rest | unchanged | 1 | 41.0 | 68.0 | 58.0 | 60.0 | 77.0 |
| Rest | unchanged | 2 | 28.0 | 42.0 | 61.0 | 49.0 | 48.0 |
| Stim48hr | decreased | 0 | 5.0 | 12.0 | 13.0 | 18.0 | 11.0 |
| Stim48hr | decreased | 1 | 9.0 | 13.0 | 12.0 | 26.0 | 20.0 |
| Stim48hr | decreased | 2 | 14.0 | 29.0 | 44.0 | 23.0 | 41.0 |
| Stim48hr | increased | 0 | 9.0 | 10.0 | 15.0 | 10.0 | 7.0 |
| Stim48hr | increased | 1 | 7.0 | 21.0 | 15.0 | 22.0 | 22.0 |
| Stim48hr | increased | 2 | 15.0 | 28.0 | 43.0 | 26.0 | 43.0 |
| Stim48hr | unchanged | 0 | 46.0 | 76.0 | 68.0 | 84.0 | 78.0 |
| Stim48hr | unchanged | 1 | 41.0 | 60.0 | 69.0 | 76.0 | 76.0 |
| Stim48hr | unchanged | 2 | 22.0 | 49.0 | 56.0 | 42.0 | 58.0 |
| Stim8hr | decreased | 0 | 11.0 | 16.0 | 13.0 | 18.0 | 17.0 |
| Stim8hr | decreased | 1 | 5.0 | 18.0 | 17.0 | 16.0 | 21.0 |
| Stim8hr | decreased | 2 | 10.0 | 20.0 | 28.0 | 28.0 | 31.0 |
| Stim8hr | increased | 0 | 7.0 | 10.0 | 12.0 | 8.0 | 13.0 |
| Stim8hr | increased | 1 | 12.0 | 24.0 | 26.0 | 29.0 | 27.0 |
| Stim8hr | increased | 2 | 15.0 | 26.0 | 34.0 | 39.0 | 38.0 |
| Stim8hr | unchanged | 0 | 55.0 | 74.0 | 77.0 | 79.0 | 67.0 |
| Stim8hr | unchanged | 1 | 35.0 | 63.0 | 68.0 | 68.0 | 82.0 |
| Stim8hr | unchanged | 2 | 25.0 | 38.0 | 50.0 | 53.0 | 57.0 |

### R=20, top_k=50, agreement d14_d23, main, with effect tercile: distinct genes per cell and bin

| condition | label | eff_class | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|---|---|
| Rest | decreased | 0 | 7.0 | 16.0 | 12.0 | 10.0 | 9.0 |
| Rest | decreased | 1 | 8.0 | 13.0 | 8.0 | 14.0 | 22.0 |
| Rest | decreased | 2 | 7.0 | 14.0 | 28.0 | 18.0 | 27.0 |
| Rest | increased | 0 | 4.0 | 13.0 | 12.0 | 7.0 | 13.0 |
| Rest | increased | 1 | 7.0 | 17.0 | 15.0 | 16.0 | 24.0 |
| Rest | increased | 2 | 7.0 | 19.0 | 31.0 | 30.0 | 26.0 |
| Rest | unchanged | 0 | 50.0 | 62.0 | 70.0 | 71.0 | 71.0 |
| Rest | unchanged | 1 | 41.0 | 68.0 | 58.0 | 60.0 | 77.0 |
| Rest | unchanged | 2 | 28.0 | 42.0 | 61.0 | 49.0 | 48.0 |
| Stim48hr | decreased | 0 | 7.0 | 13.0 | 11.0 | 12.0 | 12.0 |
| Stim48hr | decreased | 1 | 9.0 | 11.0 | 12.0 | 16.0 | 17.0 |
| Stim48hr | decreased | 2 | 13.0 | 36.0 | 33.0 | 18.0 | 43.0 |
| Stim48hr | increased | 0 | 6.0 | 6.0 | 13.0 | 10.0 | 6.0 |
| Stim48hr | increased | 1 | 9.0 | 21.0 | 12.0 | 19.0 | 22.0 |
| Stim48hr | increased | 2 | 14.0 | 28.0 | 41.0 | 29.0 | 41.0 |
| Stim48hr | unchanged | 0 | 46.0 | 76.0 | 68.0 | 84.0 | 78.0 |
| Stim48hr | unchanged | 1 | 41.0 | 60.0 | 69.0 | 76.0 | 76.0 |
| Stim48hr | unchanged | 2 | 22.0 | 49.0 | 56.0 | 42.0 | 58.0 |
| Stim8hr | decreased | 0 | 11.0 | 14.0 | 14.0 | 14.0 | 15.0 |
| Stim8hr | decreased | 1 | 7.0 | 19.0 | 18.0 | 17.0 | 19.0 |
| Stim8hr | decreased | 2 | 12.0 | 20.0 | 30.0 | 28.0 | 29.0 |
| Stim8hr | increased | 0 | 6.0 | 14.0 | 12.0 | 8.0 | 11.0 |
| Stim8hr | increased | 1 | 13.0 | 23.0 | 28.0 | 29.0 | 29.0 |
| Stim8hr | increased | 2 | 14.0 | 26.0 | 36.0 | 44.0 | 37.0 |
| Stim8hr | unchanged | 0 | 55.0 | 74.0 | 77.0 | 79.0 | 67.0 |
| Stim8hr | unchanged | 1 | 35.0 | 63.0 | 68.0 | 68.0 | 82.0 |
| Stim8hr | unchanged | 2 | 25.0 | 38.0 | 50.0 | 53.0 | 57.0 |

### R=50, top_k=all: agreement attrition (main, candidates)

| bin | label | before | after_all_three |
|---|---|---|---|
| 0 | decreased | 11886 | 232 |
| 0 | increased | 25314 | 219 |
| 0 | unchanged | 186800 | 15086 |
| 1 | decreased | 22179 | 361 |
| 1 | increased | 40119 | 746 |
| 1 | unchanged | 292530 | 25144 |
| 2 | decreased | 28699 | 745 |
| 2 | increased | 56380 | 1670 |
| 2 | unchanged | 302299 | 23544 |
| 3 | decreased | 26871 | 430 |
| 3 | increased | 52671 | 1365 |
| 3 | unchanged | 308795 | 23048 |
| 4 | decreased | 30956 | 646 |
| 4 | increased | 54033 | 1234 |
| 4 | unchanged | 347716 | 30330 |

### R=50, top_k=50: agreement attrition (main, candidates)

| bin | label | before | after_all_three |
|---|---|---|---|
| 0 | decreased | 3320 | 137 |
| 0 | increased | 8132 | 213 |
| 0 | unchanged | 186800 | 15086 |
| 1 | decreased | 5919 | 261 |
| 1 | increased | 13272 | 659 |
| 1 | unchanged | 292530 | 25144 |
| 2 | decreased | 6112 | 478 |
| 2 | increased | 14613 | 1039 |
| 2 | unchanged | 302299 | 23544 |
| 3 | decreased | 6290 | 290 |
| 3 | increased | 14859 | 918 |
| 3 | unchanged | 308795 | 23048 |
| 4 | decreased | 7490 | 534 |
| 4 | increased | 15147 | 861 |
| 4 | unchanged | 347716 | 30330 |

## Donor-agreement filter: target effect size (n_downstream) of changed readout questions, by bin and condition

Each changed (decreased or increased) candidate question counts once.

Before agreement (R=20):

| density_bin | condition | n | p25 | median | p75 |
|---|---|---|---|---|---|
| 0 | Rest | 12567 | 196.0 | 486.0 | 788.0 |
| 0 | Stim48hr | 11325 | 204.0 | 519.0 | 1103.0 |
| 0 | Stim8hr | 13308 | 238.0 | 594.0 | 1424.0 |
| 1 | Rest | 18944 | 160.0 | 392.0 | 675.0 |
| 1 | Stim48hr | 23787 | 277.0 | 611.0 | 1156.0 |
| 1 | Stim8hr | 19567 | 196.0 | 427.0 | 876.0 |
| 2 | Rest | 27858 | 291.0 | 554.0 | 1077.0 |
| 2 | Stim48hr | 26513 | 289.0 | 606.0 | 893.0 |
| 2 | Stim8hr | 30708 | 305.0 | 940.0 | 1581.0 |
| 3 | Rest | 24192 | 244.0 | 614.0 | 1254.0 |
| 3 | Stim48hr | 25077 | 220.0 | 627.0 | 1318.0 |
| 3 | Stim8hr | 30273 | 291.0 | 812.0 | 1158.0 |
| 4 | Rest | 26650 | 237.0 | 552.0 | 1271.0 |
| 4 | Stim48hr | 29504 | 297.0 | 641.0 | 1302.0 |
| 4 | Stim8hr | 28835 | 240.0 | 584.0 | 1308.0 |

After agreement all_three:

| density_bin | condition | n | p25 | median | p75 |
|---|---|---|---|---|---|
| 0 | Rest | 52 | 217.0 | 246.5 | 678.5 |
| 0 | Stim48hr | 236 | 683.5 | 1253.0 | 1253.0 |
| 0 | Stim8hr | 163 | 126.5 | 398.0 | 781.0 |
| 1 | Rest | 201 | 145.0 | 363.0 | 575.0 |
| 1 | Stim48hr | 357 | 496.0 | 697.0 | 1893.0 |
| 1 | Stim8hr | 549 | 276.0 | 560.0 | 1823.0 |
| 2 | Rest | 566 | 381.0 | 570.0 | 1238.0 |
| 2 | Stim48hr | 488 | 533.5 | 893.0 | 1027.0 |
| 2 | Stim8hr | 1361 | 650.0 | 1430.0 | 5171.0 |
| 3 | Rest | 547 | 720.0 | 1376.0 | 2326.0 |
| 3 | Stim48hr | 498 | 889.0 | 1384.0 | 1613.0 |
| 3 | Stim8hr | 750 | 671.0 | 1046.0 | 1808.0 |
| 4 | Rest | 591 | 239.0 | 2129.0 | 2290.0 |
| 4 | Stim48hr | 635 | 415.0 | 1183.0 | 1821.0 |
| 4 | Stim8hr | 654 | 219.0 | 1192.0 | 1639.0 |

After agreement d12_d34:

| density_bin | condition | n | p25 | median | p75 |
|---|---|---|---|---|---|
| 0 | Rest | 146 | 217.0 | 223.0 | 767.0 |
| 0 | Stim48hr | 511 | 499.0 | 1166.0 | 1253.0 |
| 0 | Stim8hr | 326 | 196.0 | 345.0 | 781.0 |
| 1 | Rest | 553 | 145.0 | 382.0 | 675.0 |
| 1 | Stim48hr | 1103 | 496.0 | 799.0 | 1893.0 |
| 1 | Stim8hr | 1114 | 270.75 | 504.0 | 1210.0 |
| 2 | Rest | 1231 | 363.0 | 570.0 | 1238.0 |
| 2 | Stim48hr | 1393 | 553.0 | 893.0 | 1541.0 |
| 2 | Stim8hr | 2367 | 584.0 | 1381.0 | 1670.0 |
| 3 | Rest | 1268 | 710.0 | 1376.0 | 2033.0 |
| 3 | Stim48hr | 1208 | 689.0 | 1282.0 | 1613.0 |
| 3 | Stim8hr | 1816 | 674.0 | 901.0 | 1577.0 |
| 4 | Rest | 1264 | 284.0 | 1904.0 | 2129.0 |
| 4 | Stim48hr | 1580 | 415.0 | 1183.0 | 1821.0 |
| 4 | Stim8hr | 1438 | 261.0 | 1192.0 | 1705.0 |

After agreement d14_d23:

| density_bin | condition | n | p25 | median | p75 |
|---|---|---|---|---|---|
| 0 | Rest | 144 | 217.0 | 331.0 | 755.0 |
| 0 | Stim48hr | 416 | 362.5 | 1103.0 | 1253.0 |
| 0 | Stim8hr | 433 | 238.0 | 570.0 | 781.0 |
| 1 | Rest | 494 | 145.0 | 382.0 | 575.0 |
| 1 | Stim48hr | 884 | 496.0 | 697.0 | 1483.0 |
| 1 | Stim8hr | 1116 | 364.0 | 755.0 | 2724.0 |
| 2 | Rest | 1055 | 381.0 | 570.0 | 1238.0 |
| 2 | Stim48hr | 1054 | 482.0 | 855.0 | 1541.0 |
| 2 | Stim8hr | 2507 | 650.0 | 1430.0 | 1787.0 |
| 3 | Rest | 1190 | 710.0 | 1376.0 | 2326.0 |
| 3 | Stim48hr | 1153 | 889.0 | 1448.0 | 2298.0 |
| 3 | Stim8hr | 1866 | 671.0 | 1046.0 | 1808.0 |
| 4 | Rest | 1348 | 383.0 | 2129.0 | 2290.0 |
| 4 | Stim48hr | 1639 | 498.0 | 1183.0 | 1925.0 |
| 4 | Stim8hr | 1421 | 237.0 | 1192.0 | 1639.0 |

## F-gene

### ratio=1.5, tol=0.5, agreement all_three, main: candidate pairs per condition and bin (each pair can fill either label cell)

| condition | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Rest | 82 | 359 | 638 | 584 | 838 |
| Stim8hr | 157 | 735 | 1123 | 1021 | 1002 |
| Stim48hr | 163 | 646 | 814 | 717 | 1079 |

### ratio=1.5, tol=1.0, agreement all_three, main: candidate pairs per condition and bin (each pair can fill either label cell)

| condition | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Rest | 166 | 708 | 1210 | 1167 | 1600 |
| Stim8hr | 315 | 1446 | 2086 | 1999 | 1932 |
| Stim48hr | 317 | 1294 | 1584 | 1365 | 2090 |

### ratio=2, tol=0.5, agreement all_three, main: candidate pairs per condition and bin (each pair can fill either label cell)

| condition | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Rest | 75 | 333 | 603 | 554 | 779 |
| Stim8hr | 150 | 691 | 1075 | 964 | 950 |
| Stim48hr | 156 | 622 | 778 | 666 | 1022 |

### ratio=2, tol=1.0, agreement all_three, main: candidate pairs per condition and bin (each pair can fill either label cell)

| condition | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Rest | 156 | 650 | 1152 | 1105 | 1496 |
| Stim8hr | 305 | 1360 | 1995 | 1884 | 1837 |
| Stim48hr | 306 | 1247 | 1520 | 1270 | 1995 |

### ratio=2, tol=1.0, agreement all_three: pairs' effect levels and ratios per bin

| density_bin | pairs | larger_nDE_median | smaller_nDE_median | ratio_p25 | ratio_median | ratio_p75 |
|---|---|---|---|---|---|---|
| 0 | 767 | 348.0 | 28.0 | 4.9 | 9.16 | 16.43 |
| 1 | 3257 | 313.0 | 34.0 | 4.32 | 7.72 | 14.48 |
| 2 | 4667 | 415.0 | 35.0 | 4.84 | 9.42 | 18.25 |
| 3 | 4259 | 448.0 | 35.0 | 4.65 | 9.03 | 19.1 |
| 4 | 5328 | 397.0 | 36.0 | 4.55 | 8.97 | 19.57 |

### ratio=2, tol=1.0, agreement all_three: candidate pairs per DE-count ratio band (descriptive)

| density_bin | <2 | 2-4 | 4-10 | >10 |
|---|---|---|---|---|
| 0 | 0 | 141 | 273 | 353 |
| 1 | 0 | 722 | 1296 | 1239 |
| 2 | 0 | 855 | 1592 | 2220 |
| 3 | 0 | 858 | 1405 | 1996 |
| 4 | 0 | 1087 | 1797 | 2444 |

### ratio=2, tol=1.0, agreement d12_d34: pairs' effect levels and ratios per bin

| density_bin | pairs | larger_nDE_median | smaller_nDE_median | ratio_p25 | ratio_median | ratio_p75 |
|---|---|---|---|---|---|---|
| 0 | 1565 | 247.0 | 28.0 | 3.54 | 6.4 | 12.78 |
| 1 | 5648 | 280.0 | 35.0 | 3.5 | 6.22 | 11.71 |
| 2 | 7749 | 323.0 | 35.0 | 3.9 | 7.22 | 14.5 |
| 3 | 7430 | 264.0 | 35.0 | 3.58 | 6.54 | 13.89 |
| 4 | 8486 | 315.0 | 36.0 | 3.68 | 6.71 | 14.04 |

### ratio=2, tol=1.0, agreement d12_d34: candidate pairs per DE-count ratio band (descriptive)

| density_bin | <2 | 2-4 | 4-10 | >10 |
|---|---|---|---|---|
| 0 | 0 | 458 | 581 | 526 |
| 1 | 0 | 1745 | 2201 | 1702 |
| 2 | 0 | 2002 | 2811 | 2936 |
| 3 | 0 | 2194 | 2635 | 2601 |
| 4 | 0 | 2406 | 3068 | 3012 |

### ratio=2, tol=1.0, agreement d14_d23: pairs' effect levels and ratios per bin

| density_bin | pairs | larger_nDE_median | smaller_nDE_median | ratio_p25 | ratio_median | ratio_p75 |
|---|---|---|---|---|---|---|
| 0 | 1699 | 247.0 | 28.0 | 3.65 | 6.62 | 12.78 |
| 1 | 5584 | 262.0 | 33.0 | 3.44 | 5.98 | 11.35 |
| 2 | 7325 | 318.0 | 35.0 | 3.89 | 7.18 | 14.33 |
| 3 | 6675 | 294.0 | 35.0 | 3.62 | 6.88 | 14.84 |
| 4 | 8309 | 304.0 | 36.0 | 3.6 | 6.64 | 13.8 |

### ratio=2, tol=1.0, agreement d14_d23: candidate pairs per DE-count ratio band (descriptive)

| density_bin | <2 | 2-4 | 4-10 | >10 |
|---|---|---|---|---|
| 0 | 0 | 478 | 642 | 579 |
| 1 | 0 | 1797 | 2170 | 1617 |
| 2 | 0 | 1893 | 2682 | 2750 |
| 3 | 0 | 1927 | 2263 | 2485 |
| 4 | 0 | 2422 | 2995 | 2892 |

### ratio=3, tol=0.5, agreement all_three, main: candidate pairs per condition and bin (each pair can fill either label cell)

| condition | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Rest | 68 | 291 | 546 | 507 | 689 |
| Stim8hr | 144 | 595 | 959 | 866 | 845 |
| Stim48hr | 141 | 561 | 700 | 574 | 920 |

### ratio=3, tol=1.0, agreement all_three, main: candidate pairs per condition and bin (each pair can fill either label cell)

| condition | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Rest | 137 | 557 | 1033 | 1006 | 1326 |
| Stim8hr | 274 | 1180 | 1783 | 1687 | 1614 |
| Stim48hr | 272 | 1130 | 1381 | 1113 | 1804 |

## F-neighbour (similarity over the n_inf most responsive readouts per condition; D-020)

Held at reference values: min_de 100, go_max_genes 200, match_log2_tol 1.0. Self-reliability thresholds are quantiles over covered perturbations (minimum over the filter option's splits); margin thresholds are quantiles of the candidate items' gaps at that setting. Options and distractors never include flagged genes; capacity is shown with and without the Phase 0 exclusion for them.

### n_inf=500, agreement all_three, self>=q0.50 (0.24), margin>=q0.50 (0.59), tier easy: main items per condition and bin

| condition | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Rest | 9 | 16 | 30 | 15 | 22 |
| Stim8hr | 4 | 6 | 20 | 15 | 15 |
| Stim48hr | 10 | 17 | 25 | 19 | 15 |

### n_inf=500, agreement all_three, self>=q0.50 (0.24), margin>=q0.50 (0.59), tier hard: main items per condition and bin

| condition | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Rest | 9 | 15 | 30 | 14 | 16 |
| Stim8hr | 2 | 6 | 17 | 6 | 7 |
| Stim48hr | 5 | 11 | 10 | 13 | 13 |

### n_inf=500, agreement all_three, self>=q0.50 (0.24), margin>=q0.50 (0.59), tier discovery: main items per condition and bin

| condition | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Rest | 8 | 10 | 25 | 10 | 13 |
| Stim8hr | 3 | 4 | 12 | 5 | 8 |
| Stim48hr | 3 | 9 | 8 | 8 | 10 |

### n_inf=500, agreement d12_d34, self>=q0.50 (0.32), margin>=q0.50 (0.57), tier easy: main items per condition and bin

| condition | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Rest | 7 | 22 | 34 | 21 | 25 |
| Stim8hr | 3 | 14 | 25 | 17 | 15 |
| Stim48hr | 14 | 25 | 31 | 19 | 20 |

### n_inf=500, agreement d12_d34, self>=q0.50 (0.32), margin>=q0.50 (0.57), tier hard: main items per condition and bin

| condition | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Rest | 6 | 18 | 23 | 14 | 24 |
| Stim8hr | 2 | 8 | 20 | 7 | 12 |
| Stim48hr | 3 | 13 | 15 | 11 | 12 |

### n_inf=500, agreement d12_d34, self>=q0.50 (0.32), margin>=q0.50 (0.57), tier discovery: main items per condition and bin

| condition | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Rest | 7 | 15 | 18 | 14 | 18 |
| Stim8hr | 3 | 8 | 13 | 11 | 10 |
| Stim48hr | 4 | 12 | 16 | 4 | 12 |

### n_inf=500, agreement d14_d23, self>=q0.50 (0.34), margin>=q0.50 (0.58), tier easy: main items per condition and bin

| condition | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Rest | 16 | 16 | 40 | 20 | 22 |
| Stim8hr | 5 | 10 | 21 | 20 | 15 |
| Stim48hr | 13 | 19 | 29 | 22 | 19 |

### n_inf=500, agreement d14_d23, self>=q0.50 (0.34), margin>=q0.50 (0.58), tier hard: main items per condition and bin

| condition | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Rest | 15 | 13 | 30 | 18 | 17 |
| Stim8hr | 2 | 6 | 15 | 8 | 11 |
| Stim48hr | 1 | 10 | 15 | 9 | 17 |

### n_inf=500, agreement d14_d23, self>=q0.50 (0.34), margin>=q0.50 (0.58), tier discovery: main items per condition and bin

| condition | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Rest | 16 | 14 | 28 | 15 | 13 |
| Stim8hr | 2 | 7 | 13 | 14 | 8 |
| Stim48hr | 5 | 11 | 15 | 8 | 14 |

### n_inf=1000, agreement all_three, self>=q0.50 (0.22), margin>=q0.50 (0.55), tier easy: main items per condition and bin

| condition | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Rest | 9 | 18 | 25 | 19 | 24 |
| Stim8hr | 3 | 6 | 23 | 12 | 14 |
| Stim48hr | 15 | 23 | 23 | 14 | 28 |

### n_inf=1000, agreement all_three, self>=q0.50 (0.22), margin>=q0.50 (0.55), tier hard: main items per condition and bin

| condition | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Rest | 9 | 13 | 24 | 15 | 21 |
| Stim8hr | 3 | 6 | 17 | 8 | 16 |
| Stim48hr | 3 | 12 | 14 | 10 | 13 |

### n_inf=1000, agreement all_three, self>=q0.50 (0.22), margin>=q0.50 (0.55), tier discovery: main items per condition and bin

| condition | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Rest | 9 | 14 | 23 | 16 | 17 |
| Stim8hr | 4 | 2 | 11 | 8 | 12 |
| Stim48hr | 6 | 14 | 13 | 9 | 10 |

### n_inf=1000, agreement d12_d34, self>=q0.50 (0.28), margin>=q0.50 (0.54), tier easy: main items per condition and bin

| condition | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Rest | 10 | 17 | 34 | 21 | 30 |
| Stim8hr | 2 | 13 | 23 | 15 | 19 |
| Stim48hr | 12 | 24 | 30 | 21 | 31 |

### n_inf=1000, agreement d12_d34, self>=q0.50 (0.28), margin>=q0.50 (0.54), tier hard: main items per condition and bin

| condition | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Rest | 9 | 14 | 26 | 20 | 25 |
| Stim8hr | 3 | 8 | 14 | 7 | 14 |
| Stim48hr | 3 | 13 | 18 | 11 | 18 |

### n_inf=1000, agreement d12_d34, self>=q0.50 (0.28), margin>=q0.50 (0.54), tier discovery: main items per condition and bin

| condition | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Rest | 10 | 15 | 22 | 19 | 23 |
| Stim8hr | 3 | 6 | 11 | 6 | 10 |
| Stim48hr | 6 | 12 | 17 | 9 | 14 |

### n_inf=1000, agreement d14_d23, self>=q0.50 (0.30), margin>=q0.50 (0.54), tier easy: main items per condition and bin

| condition | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Rest | 14 | 18 | 36 | 21 | 33 |
| Stim8hr | 3 | 9 | 24 | 18 | 18 |
| Stim48hr | 14 | 21 | 32 | 23 | 28 |

### n_inf=1000, agreement d14_d23, self>=q0.50 (0.30), margin>=q0.50 (0.54), tier hard: main items per condition and bin

| condition | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Rest | 14 | 13 | 27 | 19 | 23 |
| Stim8hr | 3 | 5 | 18 | 10 | 14 |
| Stim48hr | 7 | 13 | 17 | 9 | 18 |

### n_inf=1000, agreement d14_d23, self>=q0.50 (0.30), margin>=q0.50 (0.54), tier discovery: main items per condition and bin

| condition | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Rest | 12 | 12 | 29 | 16 | 17 |
| Stim8hr | 3 | 4 | 16 | 10 | 11 |
| Stim48hr | 6 | 12 | 12 | 14 | 13 |

### n_inf=2000, agreement all_three, self>=q0.50 (0.19), margin>=q0.50 (0.47), tier easy: main items per condition and bin

| condition | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Rest | 5 | 17 | 27 | 18 | 23 |
| Stim8hr | 3 | 11 | 20 | 13 | 19 |
| Stim48hr | 14 | 28 | 31 | 19 | 24 |

### n_inf=2000, agreement all_three, self>=q0.50 (0.19), margin>=q0.50 (0.47), tier hard: main items per condition and bin

| condition | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Rest | 6 | 14 | 25 | 14 | 20 |
| Stim8hr | 2 | 5 | 12 | 8 | 13 |
| Stim48hr | 5 | 13 | 14 | 9 | 19 |

### n_inf=2000, agreement all_three, self>=q0.50 (0.19), margin>=q0.50 (0.47), tier discovery: main items per condition and bin

| condition | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Rest | 4 | 14 | 24 | 14 | 13 |
| Stim8hr | 2 | 5 | 11 | 9 | 12 |
| Stim48hr | 5 | 11 | 11 | 11 | 14 |

### n_inf=2000, agreement d12_d34, self>=q0.50 (0.24), margin>=q0.50 (0.47), tier easy: main items per condition and bin

| condition | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Rest | 5 | 19 | 31 | 24 | 27 |
| Stim8hr | 3 | 12 | 21 | 16 | 21 |
| Stim48hr | 14 | 30 | 34 | 22 | 31 |

### n_inf=2000, agreement d12_d34, self>=q0.50 (0.24), margin>=q0.50 (0.47), tier hard: main items per condition and bin

| condition | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Rest | 8 | 15 | 29 | 15 | 26 |
| Stim8hr | 2 | 8 | 14 | 9 | 16 |
| Stim48hr | 5 | 11 | 19 | 12 | 20 |

### n_inf=2000, agreement d12_d34, self>=q0.50 (0.24), margin>=q0.50 (0.47), tier discovery: main items per condition and bin

| condition | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Rest | 7 | 12 | 28 | 13 | 20 |
| Stim8hr | 2 | 8 | 13 | 8 | 13 |
| Stim48hr | 6 | 15 | 16 | 10 | 15 |

### n_inf=2000, agreement d14_d23, self>=q0.50 (0.26), margin>=q0.50 (0.47), tier easy: main items per condition and bin

| condition | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Rest | 16 | 18 | 36 | 22 | 27 |
| Stim8hr | 4 | 10 | 23 | 20 | 21 |
| Stim48hr | 12 | 23 | 31 | 21 | 31 |

### n_inf=2000, agreement d14_d23, self>=q0.50 (0.26), margin>=q0.50 (0.47), tier hard: main items per condition and bin

| condition | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Rest | 15 | 13 | 31 | 15 | 21 |
| Stim8hr | 2 | 6 | 15 | 15 | 16 |
| Stim48hr | 4 | 12 | 16 | 13 | 20 |

### n_inf=2000, agreement d14_d23, self>=q0.50 (0.26), margin>=q0.50 (0.47), tier discovery: main items per condition and bin

| condition | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Rest | 16 | 13 | 30 | 13 | 17 |
| Stim8hr | 2 | 5 | 14 | 11 | 16 |
| Stim48hr | 5 | 14 | 12 | 11 | 13 |

### F-neighbour diagnostics (10th/50th/90th percentiles over covered rows)

| n_inf | agreement | condition | self_reliability | top_similarity | median_similarity |
|---|---|---|---|---|---|
| 500 | all_three | Rest | -0.14/0.21/0.50 | 0.46/0.63/0.78 | -0.05/0.06/0.12 |
| 500 | all_three | Stim8hr | -0.09/0.24/0.53 | 0.45/0.60/0.72 | -0.03/0.09/0.18 |
| 500 | all_three | Stim48hr | -0.06/0.26/0.58 | 0.48/0.63/0.76 | -0.05/0.15/0.27 |
| 500 | d12_d34 | Rest | -0.04/0.29/0.55 | 0.46/0.63/0.78 | -0.05/0.06/0.12 |
| 500 | d12_d34 | Stim8hr | -0.01/0.31/0.60 | 0.45/0.60/0.72 | -0.03/0.09/0.18 |
| 500 | d12_d34 | Stim48hr | 0.02/0.35/0.64 | 0.48/0.63/0.76 | -0.05/0.15/0.27 |
| 500 | d14_d23 | Rest | -0.02/0.32/0.60 | 0.46/0.63/0.78 | -0.05/0.06/0.12 |
| 500 | d14_d23 | Stim8hr | -0.01/0.33/0.60 | 0.45/0.60/0.72 | -0.03/0.09/0.18 |
| 500 | d14_d23 | Stim48hr | 0.02/0.36/0.64 | 0.48/0.63/0.76 | -0.05/0.15/0.27 |
| 1000 | all_three | Rest | -0.10/0.20/0.45 | 0.40/0.56/0.72 | -0.04/0.05/0.10 |
| 1000 | all_three | Stim8hr | -0.06/0.21/0.50 | 0.37/0.51/0.65 | -0.01/0.06/0.12 |
| 1000 | all_three | Stim48hr | -0.03/0.24/0.53 | 0.42/0.56/0.70 | -0.03/0.11/0.22 |
| 1000 | d12_d34 | Rest | -0.02/0.26/0.50 | 0.40/0.56/0.72 | -0.04/0.05/0.10 |
| 1000 | d12_d34 | Stim8hr | 0.02/0.27/0.53 | 0.37/0.51/0.65 | -0.01/0.06/0.12 |
| 1000 | d12_d34 | Stim48hr | 0.05/0.32/0.59 | 0.42/0.56/0.70 | -0.03/0.11/0.22 |
| 1000 | d14_d23 | Rest | 0.00/0.30/0.55 | 0.40/0.56/0.72 | -0.04/0.05/0.10 |
| 1000 | d14_d23 | Stim8hr | 0.02/0.29/0.55 | 0.37/0.51/0.65 | -0.01/0.06/0.12 |
| 1000 | d14_d23 | Stim48hr | 0.04/0.33/0.59 | 0.42/0.56/0.70 | -0.03/0.11/0.22 |
| 2000 | all_three | Rest | -0.08/0.17/0.41 | 0.32/0.49/0.63 | -0.03/0.03/0.07 |
| 2000 | all_three | Stim8hr | -0.03/0.18/0.45 | 0.31/0.43/0.59 | -0.01/0.05/0.09 |
| 2000 | all_three | Stim48hr | 0.01/0.22/0.48 | 0.37/0.49/0.63 | -0.02/0.10/0.18 |
| 2000 | d12_d34 | Rest | -0.01/0.21/0.44 | 0.32/0.49/0.63 | -0.03/0.03/0.07 |
| 2000 | d12_d34 | Stim8hr | 0.02/0.23/0.48 | 0.31/0.43/0.59 | -0.01/0.05/0.09 |
| 2000 | d12_d34 | Stim48hr | 0.07/0.29/0.53 | 0.37/0.49/0.63 | -0.02/0.10/0.18 |
| 2000 | d14_d23 | Rest | 0.00/0.25/0.48 | 0.32/0.49/0.63 | -0.03/0.03/0.07 |
| 2000 | d14_d23 | Stim8hr | 0.02/0.24/0.49 | 0.31/0.43/0.59 | -0.01/0.05/0.09 |
| 2000 | d14_d23 | Stim48hr | 0.06/0.29/0.52 | 0.37/0.49/0.63 | -0.02/0.10/0.18 |

## Summary

max_per_cell: main = largest count every cell reaches in every bin; flagged = smallest pooled cell. cells_empty: cells with no candidate in some bin (main) or at all (flagged).

| family | stratum | parameters | agreement | strata | max_per_cell | cells_empty |
|---|---|---|---|---|---|---|
| readout | main | R=5, top_k=all | all_three | effect tercile | 0 | 1 |
| readout | main | R=5, top_k=all | all_three | no tercile | 8 | 0 |
| readout | flagged (pooled) | R=5, top_k=all | all_three | condition x label | 29 | 0 |
| readout | main | R=5, top_k=all | d12_d34 | effect tercile | 5 | 0 |
| readout | main | R=5, top_k=all | d12_d34 | no tercile | 19 | 0 |
| readout | flagged (pooled) | R=5, top_k=all | d12_d34 | condition x label | 37 | 0 |
| readout | main | R=5, top_k=all | d14_d23 | effect tercile | 4 | 0 |
| readout | main | R=5, top_k=all | d14_d23 | no tercile | 19 | 0 |
| readout | flagged (pooled) | R=5, top_k=all | d14_d23 | condition x label | 35 | 0 |
| readout | main | R=5, top_k=50 | all_three | effect tercile | 0 | 1 |
| readout | main | R=5, top_k=50 | all_three | no tercile | 8 | 0 |
| readout | flagged (pooled) | R=5, top_k=50 | all_three | condition x label | 29 | 0 |
| readout | main | R=5, top_k=50 | d12_d34 | effect tercile | 4 | 0 |
| readout | main | R=5, top_k=50 | d12_d34 | no tercile | 19 | 0 |
| readout | flagged (pooled) | R=5, top_k=50 | d12_d34 | condition x label | 36 | 0 |
| readout | main | R=5, top_k=50 | d14_d23 | effect tercile | 4 | 0 |
| readout | main | R=5, top_k=50 | d14_d23 | no tercile | 18 | 0 |
| readout | flagged (pooled) | R=5, top_k=50 | d14_d23 | condition x label | 34 | 0 |
| readout | main | R=20, top_k=all | all_three | effect tercile | 0 | 1 |
| readout | main | R=20, top_k=all | all_three | no tercile | 8 | 0 |
| readout | flagged (pooled) | R=20, top_k=all | all_three | condition x label | 29 | 0 |
| readout | main | R=20, top_k=all | d12_d34 | effect tercile | 5 | 0 |
| readout | main | R=20, top_k=all | d12_d34 | no tercile | 19 | 0 |
| readout | flagged (pooled) | R=20, top_k=all | d12_d34 | condition x label | 37 | 0 |
| readout | main | R=20, top_k=all | d14_d23 | effect tercile | 4 | 0 |
| readout | main | R=20, top_k=all | d14_d23 | no tercile | 19 | 0 |
| readout | flagged (pooled) | R=20, top_k=all | d14_d23 | condition x label | 35 | 0 |
| readout | main | R=20, top_k=50 | all_three | effect tercile | 0 | 1 |
| readout | main | R=20, top_k=50 | all_three | no tercile | 8 | 0 |
| readout | flagged (pooled) | R=20, top_k=50 | all_three | condition x label | 29 | 0 |
| readout | main | R=20, top_k=50 | d12_d34 | effect tercile | 4 | 0 |
| readout | main | R=20, top_k=50 | d12_d34 | no tercile | 19 | 0 |
| readout | flagged (pooled) | R=20, top_k=50 | d12_d34 | condition x label | 36 | 0 |
| readout | main | R=20, top_k=50 | d14_d23 | effect tercile | 4 | 0 |
| readout | main | R=20, top_k=50 | d14_d23 | no tercile | 18 | 0 |
| readout | flagged (pooled) | R=20, top_k=50 | d14_d23 | condition x label | 34 | 0 |
| readout | main | R=50, top_k=all | all_three | effect tercile | 0 | 1 |
| readout | main | R=50, top_k=all | all_three | no tercile | 8 | 0 |
| readout | flagged (pooled) | R=50, top_k=all | all_three | condition x label | 29 | 0 |
| readout | main | R=50, top_k=all | d12_d34 | effect tercile | 5 | 0 |
| readout | main | R=50, top_k=all | d12_d34 | no tercile | 19 | 0 |
| readout | flagged (pooled) | R=50, top_k=all | d12_d34 | condition x label | 37 | 0 |
| readout | main | R=50, top_k=all | d14_d23 | effect tercile | 4 | 0 |
| readout | main | R=50, top_k=all | d14_d23 | no tercile | 19 | 0 |
| readout | flagged (pooled) | R=50, top_k=all | d14_d23 | condition x label | 35 | 0 |
| readout | main | R=50, top_k=50 | all_three | effect tercile | 0 | 1 |
| readout | main | R=50, top_k=50 | all_three | no tercile | 8 | 0 |
| readout | flagged (pooled) | R=50, top_k=50 | all_three | condition x label | 29 | 0 |
| readout | main | R=50, top_k=50 | d12_d34 | effect tercile | 4 | 0 |
| readout | main | R=50, top_k=50 | d12_d34 | no tercile | 19 | 0 |
| readout | flagged (pooled) | R=50, top_k=50 | d12_d34 | condition x label | 36 | 0 |
| readout | main | R=50, top_k=50 | d14_d23 | effect tercile | 4 | 0 |
| readout | main | R=50, top_k=50 | d14_d23 | no tercile | 18 | 0 |
| readout | flagged (pooled) | R=50, top_k=50 | d14_d23 | condition x label | 34 | 0 |
| gene | main | ratio=1.5, tol=0.5 | all_three | condition x label | 41 | 0 |
| gene | flagged (pooled) | ratio=1.5, tol=0.5 | all_three | condition x label | 25 | 0 |
| gene | main | ratio=1.5, tol=0.5 | d12_d34 | condition x label | 121 | 0 |
| gene | flagged (pooled) | ratio=1.5, tol=0.5 | d12_d34 | condition x label | 27 | 0 |
| gene | main | ratio=1.5, tol=0.5 | d14_d23 | condition x label | 126 | 0 |
| gene | flagged (pooled) | ratio=1.5, tol=0.5 | d14_d23 | condition x label | 28 | 0 |
| gene | main | ratio=1.5, tol=1.0 | all_three | condition x label | 83 | 0 |
| gene | flagged (pooled) | ratio=1.5, tol=1.0 | all_three | condition x label | 28 | 0 |
| gene | main | ratio=1.5, tol=1.0 | d12_d34 | condition x label | 241 | 0 |
| gene | flagged (pooled) | ratio=1.5, tol=1.0 | d12_d34 | condition x label | 28 | 0 |
| gene | main | ratio=1.5, tol=1.0 | d14_d23 | condition x label | 246 | 0 |
| gene | flagged (pooled) | ratio=1.5, tol=1.0 | d14_d23 | condition x label | 28 | 0 |
| gene | main | ratio=2, tol=0.5 | all_three | condition x label | 37 | 0 |
| gene | flagged (pooled) | ratio=2, tol=0.5 | all_three | condition x label | 25 | 0 |
| gene | main | ratio=2, tol=0.5 | d12_d34 | condition x label | 103 | 0 |
| gene | flagged (pooled) | ratio=2, tol=0.5 | d12_d34 | condition x label | 26 | 0 |
| gene | main | ratio=2, tol=0.5 | d14_d23 | condition x label | 116 | 0 |
| gene | flagged (pooled) | ratio=2, tol=0.5 | d14_d23 | condition x label | 27 | 0 |
| gene | main | ratio=2, tol=1.0 | all_three | condition x label | 78 | 0 |
| gene | flagged (pooled) | ratio=2, tol=1.0 | all_three | condition x label | 28 | 0 |
| gene | main | ratio=2, tol=1.0 | d12_d34 | condition x label | 207 | 0 |
| gene | flagged (pooled) | ratio=2, tol=1.0 | d12_d34 | condition x label | 28 | 0 |
| gene | main | ratio=2, tol=1.0 | d14_d23 | condition x label | 222 | 0 |
| gene | flagged (pooled) | ratio=2, tol=1.0 | d14_d23 | condition x label | 28 | 0 |
| gene | main | ratio=3, tol=0.5 | all_three | condition x label | 34 | 0 |
| gene | flagged (pooled) | ratio=3, tol=0.5 | all_three | condition x label | 25 | 0 |
| gene | main | ratio=3, tol=0.5 | d12_d34 | condition x label | 84 | 0 |
| gene | flagged (pooled) | ratio=3, tol=0.5 | d12_d34 | condition x label | 26 | 0 |
| gene | main | ratio=3, tol=0.5 | d14_d23 | condition x label | 94 | 0 |
| gene | flagged (pooled) | ratio=3, tol=0.5 | d14_d23 | condition x label | 27 | 0 |
| gene | main | ratio=3, tol=1.0 | all_three | condition x label | 68 | 0 |
| gene | flagged (pooled) | ratio=3, tol=1.0 | all_three | condition x label | 28 | 0 |
| gene | main | ratio=3, tol=1.0 | d12_d34 | condition x label | 165 | 0 |
| gene | flagged (pooled) | ratio=3, tol=1.0 | d12_d34 | condition x label | 28 | 0 |
| gene | main | ratio=3, tol=1.0 | d14_d23 | condition x label | 176 | 0 |
| gene | flagged (pooled) | ratio=3, tol=1.0 | d14_d23 | condition x label | 28 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.50 (0.24), margin>=q0.25 (0.51) | all_three | options excl. Phase 0 | 7 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.50 (0.24), margin>=q0.25 (0.51) | all_three | options excl. Phase 0 | 4 | 0 |
| neighbour/discovery | main | n_inf=500, self>=q0.50 (0.24), margin>=q0.25 (0.51) | all_three | options excl. Phase 0 | 4 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.50 (0.24), margin>=q0.50 (0.59) | all_three | options excl. Phase 0 | 4 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.50 (0.24), margin>=q0.50 (0.59) | all_three | options excl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=500, self>=q0.50 (0.24), margin>=q0.50 (0.59) | all_three | options excl. Phase 0 | 3 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.50 (0.24), margin>=q0.75 (0.71) | all_three | options excl. Phase 0 | 0 | 1 |
| neighbour/hard | main | n_inf=500, self>=q0.50 (0.24), margin>=q0.75 (0.71) | all_three | options excl. Phase 0 | 0 | 1 |
| neighbour/discovery | main | n_inf=500, self>=q0.50 (0.24), margin>=q0.75 (0.71) | all_three | options excl. Phase 0 | 0 | 1 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.50 (0.24), margin>=q0.25 (0.48) | all_three | options excl. Phase 0 | 16 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.50 (0.24), margin>=q0.25 (0.48) | all_three | options excl. Phase 0 | 16 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.50 (0.24), margin>=q0.25 (0.48) | all_three | options excl. Phase 0 | 15 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.50 (0.24), margin>=q0.50 (0.57) | all_three | options excl. Phase 0 | 14 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.50 (0.24), margin>=q0.50 (0.57) | all_three | options excl. Phase 0 | 14 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.50 (0.24), margin>=q0.50 (0.57) | all_three | options excl. Phase 0 | 8 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.50 (0.24), margin>=q0.75 (0.67) | all_three | options excl. Phase 0 | 6 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.50 (0.24), margin>=q0.75 (0.67) | all_three | options excl. Phase 0 | 5 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.50 (0.24), margin>=q0.75 (0.67) | all_three | options excl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.50 (0.24), margin>=q0.25 (0.52) | all_three | options incl. Phase 0 | 7 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.50 (0.24), margin>=q0.25 (0.52) | all_three | options incl. Phase 0 | 4 | 0 |
| neighbour/discovery | main | n_inf=500, self>=q0.50 (0.24), margin>=q0.25 (0.52) | all_three | options incl. Phase 0 | 4 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.50 (0.24), margin>=q0.50 (0.61) | all_three | options incl. Phase 0 | 3 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.50 (0.24), margin>=q0.50 (0.61) | all_three | options incl. Phase 0 | 3 | 0 |
| neighbour/discovery | main | n_inf=500, self>=q0.50 (0.24), margin>=q0.50 (0.61) | all_three | options incl. Phase 0 | 3 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.50 (0.24), margin>=q0.75 (0.73) | all_three | options incl. Phase 0 | 0 | 1 |
| neighbour/hard | main | n_inf=500, self>=q0.50 (0.24), margin>=q0.75 (0.73) | all_three | options incl. Phase 0 | 1 | 0 |
| neighbour/discovery | main | n_inf=500, self>=q0.50 (0.24), margin>=q0.75 (0.73) | all_three | options incl. Phase 0 | 1 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.50 (0.24), margin>=q0.25 (0.52) | all_three | options incl. Phase 0 | 21 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.50 (0.24), margin>=q0.25 (0.52) | all_three | options incl. Phase 0 | 17 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.50 (0.24), margin>=q0.25 (0.52) | all_three | options incl. Phase 0 | 13 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.50 (0.24), margin>=q0.50 (0.61) | all_three | options incl. Phase 0 | 11 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.50 (0.24), margin>=q0.50 (0.61) | all_three | options incl. Phase 0 | 12 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.50 (0.24), margin>=q0.50 (0.61) | all_three | options incl. Phase 0 | 8 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.50 (0.24), margin>=q0.75 (0.72) | all_three | options incl. Phase 0 | 3 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.50 (0.24), margin>=q0.75 (0.72) | all_three | options incl. Phase 0 | 3 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.50 (0.24), margin>=q0.75 (0.72) | all_three | options incl. Phase 0 | 3 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.75 (0.40), margin>=q0.25 (0.50) | all_three | options excl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.75 (0.40), margin>=q0.25 (0.50) | all_three | options excl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=500, self>=q0.75 (0.40), margin>=q0.25 (0.50) | all_three | options excl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.75 (0.40), margin>=q0.50 (0.59) | all_three | options excl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.75 (0.40), margin>=q0.50 (0.59) | all_three | options excl. Phase 0 | 1 | 0 |
| neighbour/discovery | main | n_inf=500, self>=q0.75 (0.40), margin>=q0.50 (0.59) | all_three | options excl. Phase 0 | 1 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.75 (0.40), margin>=q0.75 (0.70) | all_three | options excl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.75 (0.40), margin>=q0.75 (0.70) | all_three | options excl. Phase 0 | 0 | 1 |
| neighbour/discovery | main | n_inf=500, self>=q0.75 (0.40), margin>=q0.75 (0.70) | all_three | options excl. Phase 0 | 0 | 1 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.75 (0.40), margin>=q0.25 (0.49) | all_three | options excl. Phase 0 | 14 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.75 (0.40), margin>=q0.25 (0.49) | all_three | options excl. Phase 0 | 15 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.75 (0.40), margin>=q0.25 (0.49) | all_three | options excl. Phase 0 | 11 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.75 (0.40), margin>=q0.50 (0.56) | all_three | options excl. Phase 0 | 9 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.75 (0.40), margin>=q0.50 (0.56) | all_three | options excl. Phase 0 | 9 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.75 (0.40), margin>=q0.50 (0.56) | all_three | options excl. Phase 0 | 7 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.75 (0.40), margin>=q0.75 (0.67) | all_three | options excl. Phase 0 | 4 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.75 (0.40), margin>=q0.75 (0.67) | all_three | options excl. Phase 0 | 3 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.75 (0.40), margin>=q0.75 (0.67) | all_three | options excl. Phase 0 | 4 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.75 (0.40), margin>=q0.25 (0.53) | all_three | options incl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.75 (0.40), margin>=q0.25 (0.53) | all_three | options incl. Phase 0 | 3 | 0 |
| neighbour/discovery | main | n_inf=500, self>=q0.75 (0.40), margin>=q0.25 (0.53) | all_three | options incl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.75 (0.40), margin>=q0.50 (0.62) | all_three | options incl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.75 (0.40), margin>=q0.50 (0.62) | all_three | options incl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=500, self>=q0.75 (0.40), margin>=q0.50 (0.62) | all_three | options incl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.75 (0.40), margin>=q0.75 (0.73) | all_three | options incl. Phase 0 | 0 | 1 |
| neighbour/hard | main | n_inf=500, self>=q0.75 (0.40), margin>=q0.75 (0.73) | all_three | options incl. Phase 0 | 0 | 1 |
| neighbour/discovery | main | n_inf=500, self>=q0.75 (0.40), margin>=q0.75 (0.73) | all_three | options incl. Phase 0 | 0 | 1 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.75 (0.40), margin>=q0.25 (0.52) | all_three | options incl. Phase 0 | 17 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.75 (0.40), margin>=q0.25 (0.52) | all_three | options incl. Phase 0 | 14 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.75 (0.40), margin>=q0.25 (0.52) | all_three | options incl. Phase 0 | 12 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.75 (0.40), margin>=q0.50 (0.61) | all_three | options incl. Phase 0 | 11 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.75 (0.40), margin>=q0.50 (0.61) | all_three | options incl. Phase 0 | 8 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.75 (0.40), margin>=q0.50 (0.61) | all_three | options incl. Phase 0 | 8 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.75 (0.40), margin>=q0.75 (0.73) | all_three | options incl. Phase 0 | 4 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.75 (0.40), margin>=q0.75 (0.73) | all_three | options incl. Phase 0 | 1 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.75 (0.40), margin>=q0.75 (0.73) | all_three | options incl. Phase 0 | 3 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.90 (0.54), margin>=q0.25 (0.51) | all_three | options excl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.90 (0.54), margin>=q0.25 (0.51) | all_three | options excl. Phase 0 | 1 | 0 |
| neighbour/discovery | main | n_inf=500, self>=q0.90 (0.54), margin>=q0.25 (0.51) | all_three | options excl. Phase 0 | 1 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.90 (0.54), margin>=q0.50 (0.58) | all_three | options excl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.90 (0.54), margin>=q0.50 (0.58) | all_three | options excl. Phase 0 | 0 | 1 |
| neighbour/discovery | main | n_inf=500, self>=q0.90 (0.54), margin>=q0.50 (0.58) | all_three | options excl. Phase 0 | 0 | 1 |
| neighbour/easy | main | n_inf=500, self>=q0.90 (0.54), margin>=q0.75 (0.68) | all_three | options excl. Phase 0 | 0 | 2 |
| neighbour/hard | main | n_inf=500, self>=q0.90 (0.54), margin>=q0.75 (0.68) | all_three | options excl. Phase 0 | 0 | 2 |
| neighbour/discovery | main | n_inf=500, self>=q0.90 (0.54), margin>=q0.75 (0.68) | all_three | options excl. Phase 0 | 0 | 2 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.90 (0.54), margin>=q0.25 (0.43) | all_three | options excl. Phase 0 | 8 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.90 (0.54), margin>=q0.25 (0.43) | all_three | options excl. Phase 0 | 7 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.90 (0.54), margin>=q0.25 (0.43) | all_three | options excl. Phase 0 | 9 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.90 (0.54), margin>=q0.50 (0.54) | all_three | options excl. Phase 0 | 6 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.90 (0.54), margin>=q0.50 (0.54) | all_three | options excl. Phase 0 | 5 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.90 (0.54), margin>=q0.50 (0.54) | all_three | options excl. Phase 0 | 7 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.90 (0.54), margin>=q0.75 (0.63) | all_three | options excl. Phase 0 | 4 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.90 (0.54), margin>=q0.75 (0.63) | all_three | options excl. Phase 0 | 3 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.90 (0.54), margin>=q0.75 (0.63) | all_three | options excl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.90 (0.54), margin>=q0.25 (0.54) | all_three | options incl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.90 (0.54), margin>=q0.25 (0.54) | all_three | options incl. Phase 0 | 0 | 1 |
| neighbour/discovery | main | n_inf=500, self>=q0.90 (0.54), margin>=q0.25 (0.54) | all_three | options incl. Phase 0 | 1 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.90 (0.54), margin>=q0.50 (0.62) | all_three | options incl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.90 (0.54), margin>=q0.50 (0.62) | all_three | options incl. Phase 0 | 0 | 3 |
| neighbour/discovery | main | n_inf=500, self>=q0.90 (0.54), margin>=q0.50 (0.62) | all_three | options incl. Phase 0 | 0 | 1 |
| neighbour/easy | main | n_inf=500, self>=q0.90 (0.54), margin>=q0.75 (0.70) | all_three | options incl. Phase 0 | 0 | 1 |
| neighbour/hard | main | n_inf=500, self>=q0.90 (0.54), margin>=q0.75 (0.70) | all_three | options incl. Phase 0 | 0 | 3 |
| neighbour/discovery | main | n_inf=500, self>=q0.90 (0.54), margin>=q0.75 (0.70) | all_three | options incl. Phase 0 | 0 | 2 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.90 (0.54), margin>=q0.25 (0.49) | all_three | options incl. Phase 0 | 11 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.90 (0.54), margin>=q0.25 (0.49) | all_three | options incl. Phase 0 | 9 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.90 (0.54), margin>=q0.25 (0.49) | all_three | options incl. Phase 0 | 8 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.90 (0.54), margin>=q0.50 (0.59) | all_three | options incl. Phase 0 | 8 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.90 (0.54), margin>=q0.50 (0.59) | all_three | options incl. Phase 0 | 6 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.90 (0.54), margin>=q0.50 (0.59) | all_three | options incl. Phase 0 | 3 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.90 (0.54), margin>=q0.75 (0.72) | all_three | options incl. Phase 0 | 0 | 1 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.90 (0.54), margin>=q0.75 (0.72) | all_three | options incl. Phase 0 | 2 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.90 (0.54), margin>=q0.75 (0.72) | all_three | options incl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.50 (0.32), margin>=q0.25 (0.50) | d12_d34 | options excl. Phase 0 | 5 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.50 (0.32), margin>=q0.25 (0.50) | d12_d34 | options excl. Phase 0 | 3 | 0 |
| neighbour/discovery | main | n_inf=500, self>=q0.50 (0.32), margin>=q0.25 (0.50) | d12_d34 | options excl. Phase 0 | 3 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.50 (0.32), margin>=q0.50 (0.57) | d12_d34 | options excl. Phase 0 | 3 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.50 (0.32), margin>=q0.50 (0.57) | d12_d34 | options excl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=500, self>=q0.50 (0.32), margin>=q0.50 (0.57) | d12_d34 | options excl. Phase 0 | 3 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.50 (0.32), margin>=q0.75 (0.69) | d12_d34 | options excl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.50 (0.32), margin>=q0.75 (0.69) | d12_d34 | options excl. Phase 0 | 1 | 0 |
| neighbour/discovery | main | n_inf=500, self>=q0.50 (0.32), margin>=q0.75 (0.69) | d12_d34 | options excl. Phase 0 | 1 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.50 (0.32), margin>=q0.25 (0.47) | d12_d34 | options excl. Phase 0 | 24 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.50 (0.32), margin>=q0.25 (0.47) | d12_d34 | options excl. Phase 0 | 20 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.50 (0.32), margin>=q0.25 (0.47) | d12_d34 | options excl. Phase 0 | 20 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.50 (0.32), margin>=q0.50 (0.56) | d12_d34 | options excl. Phase 0 | 13 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.50 (0.32), margin>=q0.50 (0.56) | d12_d34 | options excl. Phase 0 | 14 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.50 (0.32), margin>=q0.50 (0.56) | d12_d34 | options excl. Phase 0 | 11 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.50 (0.32), margin>=q0.75 (0.68) | d12_d34 | options excl. Phase 0 | 6 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.50 (0.32), margin>=q0.75 (0.68) | d12_d34 | options excl. Phase 0 | 5 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.50 (0.32), margin>=q0.75 (0.68) | d12_d34 | options excl. Phase 0 | 3 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.50 (0.32), margin>=q0.25 (0.52) | d12_d34 | options incl. Phase 0 | 7 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.50 (0.32), margin>=q0.25 (0.52) | d12_d34 | options incl. Phase 0 | 4 | 0 |
| neighbour/discovery | main | n_inf=500, self>=q0.50 (0.32), margin>=q0.25 (0.52) | d12_d34 | options incl. Phase 0 | 3 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.50 (0.32), margin>=q0.50 (0.60) | d12_d34 | options incl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.50 (0.32), margin>=q0.50 (0.60) | d12_d34 | options incl. Phase 0 | 3 | 0 |
| neighbour/discovery | main | n_inf=500, self>=q0.50 (0.32), margin>=q0.50 (0.60) | d12_d34 | options incl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.50 (0.32), margin>=q0.75 (0.71) | d12_d34 | options incl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.50 (0.32), margin>=q0.75 (0.71) | d12_d34 | options incl. Phase 0 | 1 | 0 |
| neighbour/discovery | main | n_inf=500, self>=q0.50 (0.32), margin>=q0.75 (0.71) | d12_d34 | options incl. Phase 0 | 0 | 1 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.50 (0.32), margin>=q0.25 (0.52) | d12_d34 | options incl. Phase 0 | 25 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.50 (0.32), margin>=q0.25 (0.52) | d12_d34 | options incl. Phase 0 | 20 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.50 (0.32), margin>=q0.25 (0.52) | d12_d34 | options incl. Phase 0 | 14 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.50 (0.32), margin>=q0.50 (0.60) | d12_d34 | options incl. Phase 0 | 13 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.50 (0.32), margin>=q0.50 (0.60) | d12_d34 | options incl. Phase 0 | 9 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.50 (0.32), margin>=q0.50 (0.60) | d12_d34 | options incl. Phase 0 | 12 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.50 (0.32), margin>=q0.75 (0.72) | d12_d34 | options incl. Phase 0 | 3 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.50 (0.32), margin>=q0.75 (0.72) | d12_d34 | options incl. Phase 0 | 3 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.50 (0.32), margin>=q0.75 (0.72) | d12_d34 | options incl. Phase 0 | 3 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.75 (0.47), margin>=q0.25 (0.50) | d12_d34 | options excl. Phase 0 | 4 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.75 (0.47), margin>=q0.25 (0.50) | d12_d34 | options excl. Phase 0 | 3 | 0 |
| neighbour/discovery | main | n_inf=500, self>=q0.75 (0.47), margin>=q0.25 (0.50) | d12_d34 | options excl. Phase 0 | 3 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.75 (0.47), margin>=q0.50 (0.58) | d12_d34 | options excl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.75 (0.47), margin>=q0.50 (0.58) | d12_d34 | options excl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=500, self>=q0.75 (0.47), margin>=q0.50 (0.58) | d12_d34 | options excl. Phase 0 | 1 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.75 (0.47), margin>=q0.75 (0.70) | d12_d34 | options excl. Phase 0 | 0 | 1 |
| neighbour/hard | main | n_inf=500, self>=q0.75 (0.47), margin>=q0.75 (0.70) | d12_d34 | options excl. Phase 0 | 0 | 1 |
| neighbour/discovery | main | n_inf=500, self>=q0.75 (0.47), margin>=q0.75 (0.70) | d12_d34 | options excl. Phase 0 | 0 | 1 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.75 (0.47), margin>=q0.25 (0.46) | d12_d34 | options excl. Phase 0 | 19 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.75 (0.47), margin>=q0.25 (0.46) | d12_d34 | options excl. Phase 0 | 17 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.75 (0.47), margin>=q0.25 (0.46) | d12_d34 | options excl. Phase 0 | 14 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.75 (0.47), margin>=q0.50 (0.57) | d12_d34 | options excl. Phase 0 | 14 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.75 (0.47), margin>=q0.50 (0.57) | d12_d34 | options excl. Phase 0 | 13 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.75 (0.47), margin>=q0.50 (0.57) | d12_d34 | options excl. Phase 0 | 7 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.75 (0.47), margin>=q0.75 (0.66) | d12_d34 | options excl. Phase 0 | 6 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.75 (0.47), margin>=q0.75 (0.66) | d12_d34 | options excl. Phase 0 | 7 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.75 (0.47), margin>=q0.75 (0.66) | d12_d34 | options excl. Phase 0 | 1 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.75 (0.47), margin>=q0.25 (0.53) | d12_d34 | options incl. Phase 0 | 4 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.75 (0.47), margin>=q0.25 (0.53) | d12_d34 | options incl. Phase 0 | 3 | 0 |
| neighbour/discovery | main | n_inf=500, self>=q0.75 (0.47), margin>=q0.25 (0.53) | d12_d34 | options incl. Phase 0 | 3 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.75 (0.47), margin>=q0.50 (0.62) | d12_d34 | options incl. Phase 0 | 3 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.75 (0.47), margin>=q0.50 (0.62) | d12_d34 | options incl. Phase 0 | 3 | 0 |
| neighbour/discovery | main | n_inf=500, self>=q0.75 (0.47), margin>=q0.50 (0.62) | d12_d34 | options incl. Phase 0 | 3 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.75 (0.47), margin>=q0.75 (0.73) | d12_d34 | options incl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.75 (0.47), margin>=q0.75 (0.73) | d12_d34 | options incl. Phase 0 | 0 | 1 |
| neighbour/discovery | main | n_inf=500, self>=q0.75 (0.47), margin>=q0.75 (0.73) | d12_d34 | options incl. Phase 0 | 0 | 1 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.75 (0.47), margin>=q0.25 (0.50) | d12_d34 | options incl. Phase 0 | 19 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.75 (0.47), margin>=q0.25 (0.50) | d12_d34 | options incl. Phase 0 | 14 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.75 (0.47), margin>=q0.25 (0.50) | d12_d34 | options incl. Phase 0 | 15 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.75 (0.47), margin>=q0.50 (0.59) | d12_d34 | options incl. Phase 0 | 14 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.75 (0.47), margin>=q0.50 (0.59) | d12_d34 | options incl. Phase 0 | 8 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.75 (0.47), margin>=q0.50 (0.59) | d12_d34 | options incl. Phase 0 | 9 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.75 (0.47), margin>=q0.75 (0.73) | d12_d34 | options incl. Phase 0 | 5 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.75 (0.47), margin>=q0.75 (0.73) | d12_d34 | options incl. Phase 0 | 1 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.75 (0.47), margin>=q0.75 (0.73) | d12_d34 | options incl. Phase 0 | 1 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.90 (0.60), margin>=q0.25 (0.49) | d12_d34 | options excl. Phase 0 | 0 | 1 |
| neighbour/hard | main | n_inf=500, self>=q0.90 (0.60), margin>=q0.25 (0.49) | d12_d34 | options excl. Phase 0 | 0 | 1 |
| neighbour/discovery | main | n_inf=500, self>=q0.90 (0.60), margin>=q0.25 (0.49) | d12_d34 | options excl. Phase 0 | 0 | 1 |
| neighbour/easy | main | n_inf=500, self>=q0.90 (0.60), margin>=q0.50 (0.59) | d12_d34 | options excl. Phase 0 | 0 | 1 |
| neighbour/hard | main | n_inf=500, self>=q0.90 (0.60), margin>=q0.50 (0.59) | d12_d34 | options excl. Phase 0 | 0 | 2 |
| neighbour/discovery | main | n_inf=500, self>=q0.90 (0.60), margin>=q0.50 (0.59) | d12_d34 | options excl. Phase 0 | 0 | 2 |
| neighbour/easy | main | n_inf=500, self>=q0.90 (0.60), margin>=q0.75 (0.70) | d12_d34 | options excl. Phase 0 | 0 | 1 |
| neighbour/hard | main | n_inf=500, self>=q0.90 (0.60), margin>=q0.75 (0.70) | d12_d34 | options excl. Phase 0 | 0 | 2 |
| neighbour/discovery | main | n_inf=500, self>=q0.90 (0.60), margin>=q0.75 (0.70) | d12_d34 | options excl. Phase 0 | 0 | 2 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.90 (0.60), margin>=q0.25 (0.43) | d12_d34 | options excl. Phase 0 | 7 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.90 (0.60), margin>=q0.25 (0.43) | d12_d34 | options excl. Phase 0 | 6 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.90 (0.60), margin>=q0.25 (0.43) | d12_d34 | options excl. Phase 0 | 7 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.90 (0.60), margin>=q0.50 (0.51) | d12_d34 | options excl. Phase 0 | 5 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.90 (0.60), margin>=q0.50 (0.51) | d12_d34 | options excl. Phase 0 | 5 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.90 (0.60), margin>=q0.50 (0.51) | d12_d34 | options excl. Phase 0 | 5 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.90 (0.60), margin>=q0.75 (0.62) | d12_d34 | options excl. Phase 0 | 3 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.90 (0.60), margin>=q0.75 (0.62) | d12_d34 | options excl. Phase 0 | 3 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.90 (0.60), margin>=q0.75 (0.62) | d12_d34 | options excl. Phase 0 | 3 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.90 (0.60), margin>=q0.25 (0.51) | d12_d34 | options incl. Phase 0 | 0 | 1 |
| neighbour/hard | main | n_inf=500, self>=q0.90 (0.60), margin>=q0.25 (0.51) | d12_d34 | options incl. Phase 0 | 0 | 1 |
| neighbour/discovery | main | n_inf=500, self>=q0.90 (0.60), margin>=q0.25 (0.51) | d12_d34 | options incl. Phase 0 | 0 | 1 |
| neighbour/easy | main | n_inf=500, self>=q0.90 (0.60), margin>=q0.50 (0.60) | d12_d34 | options incl. Phase 0 | 0 | 1 |
| neighbour/hard | main | n_inf=500, self>=q0.90 (0.60), margin>=q0.50 (0.60) | d12_d34 | options incl. Phase 0 | 0 | 1 |
| neighbour/discovery | main | n_inf=500, self>=q0.90 (0.60), margin>=q0.50 (0.60) | d12_d34 | options incl. Phase 0 | 0 | 1 |
| neighbour/easy | main | n_inf=500, self>=q0.90 (0.60), margin>=q0.75 (0.70) | d12_d34 | options incl. Phase 0 | 0 | 2 |
| neighbour/hard | main | n_inf=500, self>=q0.90 (0.60), margin>=q0.75 (0.70) | d12_d34 | options incl. Phase 0 | 0 | 2 |
| neighbour/discovery | main | n_inf=500, self>=q0.90 (0.60), margin>=q0.75 (0.70) | d12_d34 | options incl. Phase 0 | 0 | 2 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.90 (0.60), margin>=q0.25 (0.47) | d12_d34 | options incl. Phase 0 | 13 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.90 (0.60), margin>=q0.25 (0.47) | d12_d34 | options incl. Phase 0 | 8 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.90 (0.60), margin>=q0.25 (0.47) | d12_d34 | options incl. Phase 0 | 7 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.90 (0.60), margin>=q0.50 (0.57) | d12_d34 | options incl. Phase 0 | 8 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.90 (0.60), margin>=q0.50 (0.57) | d12_d34 | options incl. Phase 0 | 4 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.90 (0.60), margin>=q0.50 (0.57) | d12_d34 | options incl. Phase 0 | 4 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.90 (0.60), margin>=q0.75 (0.71) | d12_d34 | options incl. Phase 0 | 2 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.90 (0.60), margin>=q0.75 (0.71) | d12_d34 | options incl. Phase 0 | 2 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.90 (0.60), margin>=q0.75 (0.71) | d12_d34 | options incl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.50 (0.34), margin>=q0.25 (0.49) | d14_d23 | options excl. Phase 0 | 10 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.50 (0.34), margin>=q0.25 (0.49) | d14_d23 | options excl. Phase 0 | 4 | 0 |
| neighbour/discovery | main | n_inf=500, self>=q0.50 (0.34), margin>=q0.25 (0.49) | d14_d23 | options excl. Phase 0 | 3 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.50 (0.34), margin>=q0.50 (0.58) | d14_d23 | options excl. Phase 0 | 5 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.50 (0.34), margin>=q0.50 (0.58) | d14_d23 | options excl. Phase 0 | 1 | 0 |
| neighbour/discovery | main | n_inf=500, self>=q0.50 (0.34), margin>=q0.50 (0.58) | d14_d23 | options excl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.50 (0.34), margin>=q0.75 (0.71) | d14_d23 | options excl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.50 (0.34), margin>=q0.75 (0.71) | d14_d23 | options excl. Phase 0 | 0 | 2 |
| neighbour/discovery | main | n_inf=500, self>=q0.50 (0.34), margin>=q0.75 (0.71) | d14_d23 | options excl. Phase 0 | 0 | 2 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.50 (0.34), margin>=q0.25 (0.46) | d14_d23 | options excl. Phase 0 | 24 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.50 (0.34), margin>=q0.25 (0.46) | d14_d23 | options excl. Phase 0 | 17 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.50 (0.34), margin>=q0.25 (0.46) | d14_d23 | options excl. Phase 0 | 17 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.50 (0.34), margin>=q0.50 (0.57) | d14_d23 | options excl. Phase 0 | 18 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.50 (0.34), margin>=q0.50 (0.57) | d14_d23 | options excl. Phase 0 | 14 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.50 (0.34), margin>=q0.50 (0.57) | d14_d23 | options excl. Phase 0 | 11 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.50 (0.34), margin>=q0.75 (0.66) | d14_d23 | options excl. Phase 0 | 8 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.50 (0.34), margin>=q0.75 (0.66) | d14_d23 | options excl. Phase 0 | 4 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.50 (0.34), margin>=q0.75 (0.66) | d14_d23 | options excl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.50 (0.34), margin>=q0.25 (0.51) | d14_d23 | options incl. Phase 0 | 8 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.50 (0.34), margin>=q0.25 (0.51) | d14_d23 | options incl. Phase 0 | 4 | 0 |
| neighbour/discovery | main | n_inf=500, self>=q0.50 (0.34), margin>=q0.25 (0.51) | d14_d23 | options incl. Phase 0 | 5 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.50 (0.34), margin>=q0.50 (0.61) | d14_d23 | options incl. Phase 0 | 4 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.50 (0.34), margin>=q0.50 (0.61) | d14_d23 | options incl. Phase 0 | 3 | 0 |
| neighbour/discovery | main | n_inf=500, self>=q0.50 (0.34), margin>=q0.50 (0.61) | d14_d23 | options incl. Phase 0 | 3 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.50 (0.34), margin>=q0.75 (0.72) | d14_d23 | options incl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.50 (0.34), margin>=q0.75 (0.72) | d14_d23 | options incl. Phase 0 | 1 | 0 |
| neighbour/discovery | main | n_inf=500, self>=q0.50 (0.34), margin>=q0.75 (0.72) | d14_d23 | options incl. Phase 0 | 1 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.50 (0.34), margin>=q0.25 (0.52) | d14_d23 | options incl. Phase 0 | 22 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.50 (0.34), margin>=q0.25 (0.52) | d14_d23 | options incl. Phase 0 | 18 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.50 (0.34), margin>=q0.25 (0.52) | d14_d23 | options incl. Phase 0 | 15 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.50 (0.34), margin>=q0.50 (0.61) | d14_d23 | options incl. Phase 0 | 18 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.50 (0.34), margin>=q0.50 (0.61) | d14_d23 | options incl. Phase 0 | 11 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.50 (0.34), margin>=q0.50 (0.61) | d14_d23 | options incl. Phase 0 | 8 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.50 (0.34), margin>=q0.75 (0.72) | d14_d23 | options incl. Phase 0 | 5 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.50 (0.34), margin>=q0.75 (0.72) | d14_d23 | options incl. Phase 0 | 1 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.50 (0.34), margin>=q0.75 (0.72) | d14_d23 | options incl. Phase 0 | 5 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.75 (0.49), margin>=q0.25 (0.49) | d14_d23 | options excl. Phase 0 | 4 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.75 (0.49), margin>=q0.25 (0.49) | d14_d23 | options excl. Phase 0 | 4 | 0 |
| neighbour/discovery | main | n_inf=500, self>=q0.75 (0.49), margin>=q0.25 (0.49) | d14_d23 | options excl. Phase 0 | 4 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.75 (0.49), margin>=q0.50 (0.58) | d14_d23 | options excl. Phase 0 | 3 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.75 (0.49), margin>=q0.50 (0.58) | d14_d23 | options excl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=500, self>=q0.75 (0.49), margin>=q0.50 (0.58) | d14_d23 | options excl. Phase 0 | 1 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.75 (0.49), margin>=q0.75 (0.69) | d14_d23 | options excl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.75 (0.49), margin>=q0.75 (0.69) | d14_d23 | options excl. Phase 0 | 0 | 1 |
| neighbour/discovery | main | n_inf=500, self>=q0.75 (0.49), margin>=q0.75 (0.69) | d14_d23 | options excl. Phase 0 | 0 | 1 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.75 (0.49), margin>=q0.25 (0.47) | d14_d23 | options excl. Phase 0 | 17 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.75 (0.49), margin>=q0.25 (0.47) | d14_d23 | options excl. Phase 0 | 16 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.75 (0.49), margin>=q0.25 (0.47) | d14_d23 | options excl. Phase 0 | 15 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.75 (0.49), margin>=q0.50 (0.55) | d14_d23 | options excl. Phase 0 | 14 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.75 (0.49), margin>=q0.50 (0.55) | d14_d23 | options excl. Phase 0 | 13 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.75 (0.49), margin>=q0.50 (0.55) | d14_d23 | options excl. Phase 0 | 8 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.75 (0.49), margin>=q0.75 (0.64) | d14_d23 | options excl. Phase 0 | 8 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.75 (0.49), margin>=q0.75 (0.64) | d14_d23 | options excl. Phase 0 | 5 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.75 (0.49), margin>=q0.75 (0.64) | d14_d23 | options excl. Phase 0 | 3 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.75 (0.49), margin>=q0.25 (0.52) | d14_d23 | options incl. Phase 0 | 4 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.75 (0.49), margin>=q0.25 (0.52) | d14_d23 | options incl. Phase 0 | 4 | 0 |
| neighbour/discovery | main | n_inf=500, self>=q0.75 (0.49), margin>=q0.25 (0.52) | d14_d23 | options incl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.75 (0.49), margin>=q0.50 (0.60) | d14_d23 | options incl. Phase 0 | 3 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.75 (0.49), margin>=q0.50 (0.60) | d14_d23 | options incl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=500, self>=q0.75 (0.49), margin>=q0.50 (0.60) | d14_d23 | options incl. Phase 0 | 0 | 1 |
| neighbour/easy | main | n_inf=500, self>=q0.75 (0.49), margin>=q0.75 (0.71) | d14_d23 | options incl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.75 (0.49), margin>=q0.75 (0.71) | d14_d23 | options incl. Phase 0 | 0 | 2 |
| neighbour/discovery | main | n_inf=500, self>=q0.75 (0.49), margin>=q0.75 (0.71) | d14_d23 | options incl. Phase 0 | 0 | 2 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.75 (0.49), margin>=q0.25 (0.52) | d14_d23 | options incl. Phase 0 | 20 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.75 (0.49), margin>=q0.25 (0.52) | d14_d23 | options incl. Phase 0 | 15 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.75 (0.49), margin>=q0.25 (0.52) | d14_d23 | options incl. Phase 0 | 15 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.75 (0.49), margin>=q0.50 (0.60) | d14_d23 | options incl. Phase 0 | 16 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.75 (0.49), margin>=q0.50 (0.60) | d14_d23 | options incl. Phase 0 | 10 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.75 (0.49), margin>=q0.50 (0.60) | d14_d23 | options incl. Phase 0 | 9 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.75 (0.49), margin>=q0.75 (0.72) | d14_d23 | options incl. Phase 0 | 6 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.75 (0.49), margin>=q0.75 (0.72) | d14_d23 | options incl. Phase 0 | 3 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.75 (0.49), margin>=q0.75 (0.72) | d14_d23 | options incl. Phase 0 | 3 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.90 (0.61), margin>=q0.25 (0.47) | d14_d23 | options excl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.90 (0.61), margin>=q0.25 (0.47) | d14_d23 | options excl. Phase 0 | 0 | 1 |
| neighbour/discovery | main | n_inf=500, self>=q0.90 (0.61), margin>=q0.25 (0.47) | d14_d23 | options excl. Phase 0 | 0 | 1 |
| neighbour/easy | main | n_inf=500, self>=q0.90 (0.61), margin>=q0.50 (0.57) | d14_d23 | options excl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.90 (0.61), margin>=q0.50 (0.57) | d14_d23 | options excl. Phase 0 | 0 | 2 |
| neighbour/discovery | main | n_inf=500, self>=q0.90 (0.61), margin>=q0.50 (0.57) | d14_d23 | options excl. Phase 0 | 0 | 2 |
| neighbour/easy | main | n_inf=500, self>=q0.90 (0.61), margin>=q0.75 (0.66) | d14_d23 | options excl. Phase 0 | 0 | 2 |
| neighbour/hard | main | n_inf=500, self>=q0.90 (0.61), margin>=q0.75 (0.66) | d14_d23 | options excl. Phase 0 | 0 | 2 |
| neighbour/discovery | main | n_inf=500, self>=q0.90 (0.61), margin>=q0.75 (0.66) | d14_d23 | options excl. Phase 0 | 0 | 2 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.90 (0.61), margin>=q0.25 (0.42) | d14_d23 | options excl. Phase 0 | 14 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.90 (0.61), margin>=q0.25 (0.42) | d14_d23 | options excl. Phase 0 | 10 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.90 (0.61), margin>=q0.25 (0.42) | d14_d23 | options excl. Phase 0 | 8 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.90 (0.61), margin>=q0.50 (0.50) | d14_d23 | options excl. Phase 0 | 10 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.90 (0.61), margin>=q0.50 (0.50) | d14_d23 | options excl. Phase 0 | 8 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.90 (0.61), margin>=q0.50 (0.50) | d14_d23 | options excl. Phase 0 | 6 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.90 (0.61), margin>=q0.75 (0.59) | d14_d23 | options excl. Phase 0 | 6 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.90 (0.61), margin>=q0.75 (0.59) | d14_d23 | options excl. Phase 0 | 4 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.90 (0.61), margin>=q0.75 (0.59) | d14_d23 | options excl. Phase 0 | 3 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.90 (0.61), margin>=q0.25 (0.50) | d14_d23 | options incl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.90 (0.61), margin>=q0.25 (0.50) | d14_d23 | options incl. Phase 0 | 1 | 0 |
| neighbour/discovery | main | n_inf=500, self>=q0.90 (0.61), margin>=q0.25 (0.50) | d14_d23 | options incl. Phase 0 | 1 | 0 |
| neighbour/easy | main | n_inf=500, self>=q0.90 (0.61), margin>=q0.50 (0.59) | d14_d23 | options incl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.90 (0.61), margin>=q0.50 (0.59) | d14_d23 | options incl. Phase 0 | 0 | 2 |
| neighbour/discovery | main | n_inf=500, self>=q0.90 (0.61), margin>=q0.50 (0.59) | d14_d23 | options incl. Phase 0 | 0 | 1 |
| neighbour/easy | main | n_inf=500, self>=q0.90 (0.61), margin>=q0.75 (0.69) | d14_d23 | options incl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=500, self>=q0.90 (0.61), margin>=q0.75 (0.69) | d14_d23 | options incl. Phase 0 | 0 | 2 |
| neighbour/discovery | main | n_inf=500, self>=q0.90 (0.61), margin>=q0.75 (0.69) | d14_d23 | options incl. Phase 0 | 0 | 2 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.90 (0.61), margin>=q0.25 (0.49) | d14_d23 | options incl. Phase 0 | 13 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.90 (0.61), margin>=q0.25 (0.49) | d14_d23 | options incl. Phase 0 | 10 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.90 (0.61), margin>=q0.25 (0.49) | d14_d23 | options incl. Phase 0 | 9 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.90 (0.61), margin>=q0.50 (0.58) | d14_d23 | options incl. Phase 0 | 11 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.90 (0.61), margin>=q0.50 (0.58) | d14_d23 | options incl. Phase 0 | 5 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.90 (0.61), margin>=q0.50 (0.58) | d14_d23 | options incl. Phase 0 | 5 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=500, self>=q0.90 (0.61), margin>=q0.75 (0.71) | d14_d23 | options incl. Phase 0 | 2 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=500, self>=q0.90 (0.61), margin>=q0.75 (0.71) | d14_d23 | options incl. Phase 0 | 1 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=500, self>=q0.90 (0.61), margin>=q0.75 (0.71) | d14_d23 | options incl. Phase 0 | 1 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.50 (0.22), margin>=q0.25 (0.45) | all_three | options excl. Phase 0 | 7 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.50 (0.22), margin>=q0.25 (0.45) | all_three | options excl. Phase 0 | 5 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.50 (0.22), margin>=q0.25 (0.45) | all_three | options excl. Phase 0 | 7 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.50 (0.22), margin>=q0.50 (0.55) | all_three | options excl. Phase 0 | 3 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.50 (0.22), margin>=q0.50 (0.55) | all_three | options excl. Phase 0 | 3 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.50 (0.22), margin>=q0.50 (0.55) | all_three | options excl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.50 (0.22), margin>=q0.75 (0.65) | all_three | options excl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.50 (0.22), margin>=q0.75 (0.65) | all_three | options excl. Phase 0 | 1 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.50 (0.22), margin>=q0.75 (0.65) | all_three | options excl. Phase 0 | 1 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.50 (0.22), margin>=q0.25 (0.44) | all_three | options excl. Phase 0 | 23 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.50 (0.22), margin>=q0.25 (0.44) | all_three | options excl. Phase 0 | 16 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.50 (0.22), margin>=q0.25 (0.44) | all_three | options excl. Phase 0 | 13 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.50 (0.22), margin>=q0.50 (0.52) | all_three | options excl. Phase 0 | 16 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.50 (0.22), margin>=q0.50 (0.52) | all_three | options excl. Phase 0 | 13 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.50 (0.22), margin>=q0.50 (0.52) | all_three | options excl. Phase 0 | 9 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.50 (0.22), margin>=q0.75 (0.63) | all_three | options excl. Phase 0 | 6 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.50 (0.22), margin>=q0.75 (0.63) | all_three | options excl. Phase 0 | 6 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.50 (0.22), margin>=q0.75 (0.63) | all_three | options excl. Phase 0 | 5 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.50 (0.22), margin>=q0.25 (0.48) | all_three | options incl. Phase 0 | 6 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.50 (0.22), margin>=q0.25 (0.48) | all_three | options incl. Phase 0 | 4 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.50 (0.22), margin>=q0.25 (0.48) | all_three | options incl. Phase 0 | 4 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.50 (0.22), margin>=q0.50 (0.57) | all_three | options incl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.50 (0.22), margin>=q0.50 (0.57) | all_three | options incl. Phase 0 | 3 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.50 (0.22), margin>=q0.50 (0.57) | all_three | options incl. Phase 0 | 3 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.50 (0.22), margin>=q0.75 (0.67) | all_three | options incl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.50 (0.22), margin>=q0.75 (0.67) | all_three | options incl. Phase 0 | 1 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.50 (0.22), margin>=q0.75 (0.67) | all_three | options incl. Phase 0 | 1 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.50 (0.22), margin>=q0.25 (0.49) | all_three | options incl. Phase 0 | 23 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.50 (0.22), margin>=q0.25 (0.49) | all_three | options incl. Phase 0 | 18 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.50 (0.22), margin>=q0.25 (0.49) | all_three | options incl. Phase 0 | 13 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.50 (0.22), margin>=q0.50 (0.57) | all_three | options incl. Phase 0 | 18 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.50 (0.22), margin>=q0.50 (0.57) | all_three | options incl. Phase 0 | 14 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.50 (0.22), margin>=q0.50 (0.57) | all_three | options incl. Phase 0 | 10 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.50 (0.22), margin>=q0.75 (0.69) | all_three | options incl. Phase 0 | 4 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.50 (0.22), margin>=q0.75 (0.69) | all_three | options incl. Phase 0 | 5 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.50 (0.22), margin>=q0.75 (0.69) | all_three | options incl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.75 (0.36), margin>=q0.25 (0.45) | all_three | options excl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.75 (0.36), margin>=q0.25 (0.45) | all_three | options excl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.75 (0.36), margin>=q0.25 (0.45) | all_three | options excl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.75 (0.36), margin>=q0.50 (0.56) | all_three | options excl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.75 (0.36), margin>=q0.50 (0.56) | all_three | options excl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.75 (0.36), margin>=q0.50 (0.56) | all_three | options excl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.75 (0.36), margin>=q0.75 (0.66) | all_three | options excl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.75 (0.36), margin>=q0.75 (0.66) | all_three | options excl. Phase 0 | 0 | 1 |
| neighbour/discovery | main | n_inf=1000, self>=q0.75 (0.36), margin>=q0.75 (0.66) | all_three | options excl. Phase 0 | 0 | 2 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.75 (0.36), margin>=q0.25 (0.44) | all_three | options excl. Phase 0 | 18 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.75 (0.36), margin>=q0.25 (0.44) | all_three | options excl. Phase 0 | 14 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.75 (0.36), margin>=q0.25 (0.44) | all_three | options excl. Phase 0 | 10 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.75 (0.36), margin>=q0.50 (0.51) | all_three | options excl. Phase 0 | 13 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.75 (0.36), margin>=q0.50 (0.51) | all_three | options excl. Phase 0 | 8 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.75 (0.36), margin>=q0.50 (0.51) | all_three | options excl. Phase 0 | 6 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.75 (0.36), margin>=q0.75 (0.62) | all_three | options excl. Phase 0 | 5 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.75 (0.36), margin>=q0.75 (0.62) | all_three | options excl. Phase 0 | 2 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.75 (0.36), margin>=q0.75 (0.62) | all_three | options excl. Phase 0 | 4 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.75 (0.36), margin>=q0.25 (0.48) | all_three | options incl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.75 (0.36), margin>=q0.25 (0.48) | all_three | options incl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.75 (0.36), margin>=q0.25 (0.48) | all_three | options incl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.75 (0.36), margin>=q0.50 (0.57) | all_three | options incl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.75 (0.36), margin>=q0.50 (0.57) | all_three | options incl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.75 (0.36), margin>=q0.50 (0.57) | all_three | options incl. Phase 0 | 1 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.75 (0.36), margin>=q0.75 (0.68) | all_three | options incl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.75 (0.36), margin>=q0.75 (0.68) | all_three | options incl. Phase 0 | 1 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.75 (0.36), margin>=q0.75 (0.68) | all_three | options incl. Phase 0 | 1 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.75 (0.36), margin>=q0.25 (0.46) | all_three | options incl. Phase 0 | 19 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.75 (0.36), margin>=q0.25 (0.46) | all_three | options incl. Phase 0 | 15 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.75 (0.36), margin>=q0.25 (0.46) | all_three | options incl. Phase 0 | 11 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.75 (0.36), margin>=q0.50 (0.55) | all_three | options incl. Phase 0 | 15 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.75 (0.36), margin>=q0.50 (0.55) | all_three | options incl. Phase 0 | 11 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.75 (0.36), margin>=q0.50 (0.55) | all_three | options incl. Phase 0 | 8 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.75 (0.36), margin>=q0.75 (0.67) | all_three | options incl. Phase 0 | 6 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.75 (0.36), margin>=q0.75 (0.67) | all_three | options incl. Phase 0 | 2 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.75 (0.36), margin>=q0.75 (0.67) | all_three | options incl. Phase 0 | 1 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.90 (0.49), margin>=q0.25 (0.45) | all_three | options excl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.90 (0.49), margin>=q0.25 (0.45) | all_three | options excl. Phase 0 | 0 | 1 |
| neighbour/discovery | main | n_inf=1000, self>=q0.90 (0.49), margin>=q0.25 (0.45) | all_three | options excl. Phase 0 | 0 | 1 |
| neighbour/easy | main | n_inf=1000, self>=q0.90 (0.49), margin>=q0.50 (0.55) | all_three | options excl. Phase 0 | 0 | 1 |
| neighbour/hard | main | n_inf=1000, self>=q0.90 (0.49), margin>=q0.50 (0.55) | all_three | options excl. Phase 0 | 0 | 2 |
| neighbour/discovery | main | n_inf=1000, self>=q0.90 (0.49), margin>=q0.50 (0.55) | all_three | options excl. Phase 0 | 0 | 3 |
| neighbour/easy | main | n_inf=1000, self>=q0.90 (0.49), margin>=q0.75 (0.66) | all_three | options excl. Phase 0 | 0 | 1 |
| neighbour/hard | main | n_inf=1000, self>=q0.90 (0.49), margin>=q0.75 (0.66) | all_three | options excl. Phase 0 | 0 | 3 |
| neighbour/discovery | main | n_inf=1000, self>=q0.90 (0.49), margin>=q0.75 (0.66) | all_three | options excl. Phase 0 | 0 | 3 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.90 (0.49), margin>=q0.25 (0.37) | all_three | options excl. Phase 0 | 9 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.90 (0.49), margin>=q0.25 (0.37) | all_three | options excl. Phase 0 | 8 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.90 (0.49), margin>=q0.25 (0.37) | all_three | options excl. Phase 0 | 8 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.90 (0.49), margin>=q0.50 (0.49) | all_three | options excl. Phase 0 | 3 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.90 (0.49), margin>=q0.50 (0.49) | all_three | options excl. Phase 0 | 4 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.90 (0.49), margin>=q0.50 (0.49) | all_three | options excl. Phase 0 | 3 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.90 (0.49), margin>=q0.75 (0.60) | all_three | options excl. Phase 0 | 2 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.90 (0.49), margin>=q0.75 (0.60) | all_three | options excl. Phase 0 | 2 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.90 (0.49), margin>=q0.75 (0.60) | all_three | options excl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.90 (0.49), margin>=q0.25 (0.47) | all_three | options incl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.90 (0.49), margin>=q0.25 (0.47) | all_three | options incl. Phase 0 | 1 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.90 (0.49), margin>=q0.25 (0.47) | all_three | options incl. Phase 0 | 1 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.90 (0.49), margin>=q0.50 (0.55) | all_three | options incl. Phase 0 | 0 | 1 |
| neighbour/hard | main | n_inf=1000, self>=q0.90 (0.49), margin>=q0.50 (0.55) | all_three | options incl. Phase 0 | 0 | 2 |
| neighbour/discovery | main | n_inf=1000, self>=q0.90 (0.49), margin>=q0.50 (0.55) | all_three | options incl. Phase 0 | 0 | 1 |
| neighbour/easy | main | n_inf=1000, self>=q0.90 (0.49), margin>=q0.75 (0.66) | all_three | options incl. Phase 0 | 0 | 1 |
| neighbour/hard | main | n_inf=1000, self>=q0.90 (0.49), margin>=q0.75 (0.66) | all_three | options incl. Phase 0 | 0 | 2 |
| neighbour/discovery | main | n_inf=1000, self>=q0.90 (0.49), margin>=q0.75 (0.66) | all_three | options incl. Phase 0 | 0 | 3 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.90 (0.49), margin>=q0.25 (0.45) | all_three | options incl. Phase 0 | 12 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.90 (0.49), margin>=q0.25 (0.45) | all_three | options incl. Phase 0 | 10 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.90 (0.49), margin>=q0.25 (0.45) | all_three | options incl. Phase 0 | 9 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.90 (0.49), margin>=q0.50 (0.55) | all_three | options incl. Phase 0 | 8 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.90 (0.49), margin>=q0.50 (0.55) | all_three | options incl. Phase 0 | 6 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.90 (0.49), margin>=q0.50 (0.55) | all_three | options incl. Phase 0 | 3 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.90 (0.49), margin>=q0.75 (0.68) | all_three | options incl. Phase 0 | 4 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.90 (0.49), margin>=q0.75 (0.68) | all_three | options incl. Phase 0 | 1 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.90 (0.49), margin>=q0.75 (0.68) | all_three | options incl. Phase 0 | 0 | 1 |
| neighbour/easy | main | n_inf=1000, self>=q0.50 (0.28), margin>=q0.25 (0.44) | d12_d34 | options excl. Phase 0 | 8 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.50 (0.28), margin>=q0.25 (0.44) | d12_d34 | options excl. Phase 0 | 6 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.50 (0.28), margin>=q0.25 (0.44) | d12_d34 | options excl. Phase 0 | 5 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.50 (0.28), margin>=q0.50 (0.54) | d12_d34 | options excl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.50 (0.28), margin>=q0.50 (0.54) | d12_d34 | options excl. Phase 0 | 3 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.50 (0.28), margin>=q0.50 (0.54) | d12_d34 | options excl. Phase 0 | 3 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.50 (0.28), margin>=q0.75 (0.64) | d12_d34 | options excl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.50 (0.28), margin>=q0.75 (0.64) | d12_d34 | options excl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.50 (0.28), margin>=q0.75 (0.64) | d12_d34 | options excl. Phase 0 | 1 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.50 (0.28), margin>=q0.25 (0.45) | d12_d34 | options excl. Phase 0 | 29 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.50 (0.28), margin>=q0.25 (0.45) | d12_d34 | options excl. Phase 0 | 20 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.50 (0.28), margin>=q0.25 (0.45) | d12_d34 | options excl. Phase 0 | 18 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.50 (0.28), margin>=q0.50 (0.53) | d12_d34 | options excl. Phase 0 | 20 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.50 (0.28), margin>=q0.50 (0.53) | d12_d34 | options excl. Phase 0 | 15 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.50 (0.28), margin>=q0.50 (0.53) | d12_d34 | options excl. Phase 0 | 9 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.50 (0.28), margin>=q0.75 (0.62) | d12_d34 | options excl. Phase 0 | 7 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.50 (0.28), margin>=q0.75 (0.62) | d12_d34 | options excl. Phase 0 | 6 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.50 (0.28), margin>=q0.75 (0.62) | d12_d34 | options excl. Phase 0 | 6 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.50 (0.28), margin>=q0.25 (0.47) | d12_d34 | options incl. Phase 0 | 6 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.50 (0.28), margin>=q0.25 (0.47) | d12_d34 | options incl. Phase 0 | 3 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.50 (0.28), margin>=q0.25 (0.47) | d12_d34 | options incl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.50 (0.28), margin>=q0.50 (0.57) | d12_d34 | options incl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.50 (0.28), margin>=q0.50 (0.57) | d12_d34 | options incl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.50 (0.28), margin>=q0.50 (0.57) | d12_d34 | options incl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.50 (0.28), margin>=q0.75 (0.67) | d12_d34 | options incl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.50 (0.28), margin>=q0.75 (0.67) | d12_d34 | options incl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.50 (0.28), margin>=q0.75 (0.67) | d12_d34 | options incl. Phase 0 | 1 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.50 (0.28), margin>=q0.25 (0.47) | d12_d34 | options incl. Phase 0 | 30 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.50 (0.28), margin>=q0.25 (0.47) | d12_d34 | options incl. Phase 0 | 22 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.50 (0.28), margin>=q0.25 (0.47) | d12_d34 | options incl. Phase 0 | 16 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.50 (0.28), margin>=q0.50 (0.55) | d12_d34 | options incl. Phase 0 | 22 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.50 (0.28), margin>=q0.50 (0.55) | d12_d34 | options incl. Phase 0 | 15 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.50 (0.28), margin>=q0.50 (0.55) | d12_d34 | options incl. Phase 0 | 10 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.50 (0.28), margin>=q0.75 (0.66) | d12_d34 | options incl. Phase 0 | 5 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.50 (0.28), margin>=q0.75 (0.66) | d12_d34 | options incl. Phase 0 | 7 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.50 (0.28), margin>=q0.75 (0.66) | d12_d34 | options incl. Phase 0 | 3 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.75 (0.42), margin>=q0.25 (0.44) | d12_d34 | options excl. Phase 0 | 3 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.75 (0.42), margin>=q0.25 (0.44) | d12_d34 | options excl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.75 (0.42), margin>=q0.25 (0.44) | d12_d34 | options excl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.75 (0.42), margin>=q0.50 (0.55) | d12_d34 | options excl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.75 (0.42), margin>=q0.50 (0.55) | d12_d34 | options excl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.75 (0.42), margin>=q0.50 (0.55) | d12_d34 | options excl. Phase 0 | 1 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.75 (0.42), margin>=q0.75 (0.66) | d12_d34 | options excl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.75 (0.42), margin>=q0.75 (0.66) | d12_d34 | options excl. Phase 0 | 1 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.75 (0.42), margin>=q0.75 (0.66) | d12_d34 | options excl. Phase 0 | 1 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.75 (0.42), margin>=q0.25 (0.43) | d12_d34 | options excl. Phase 0 | 20 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.75 (0.42), margin>=q0.25 (0.43) | d12_d34 | options excl. Phase 0 | 16 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.75 (0.42), margin>=q0.25 (0.43) | d12_d34 | options excl. Phase 0 | 12 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.75 (0.42), margin>=q0.50 (0.50) | d12_d34 | options excl. Phase 0 | 13 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.75 (0.42), margin>=q0.50 (0.50) | d12_d34 | options excl. Phase 0 | 11 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.75 (0.42), margin>=q0.50 (0.50) | d12_d34 | options excl. Phase 0 | 7 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.75 (0.42), margin>=q0.75 (0.61) | d12_d34 | options excl. Phase 0 | 7 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.75 (0.42), margin>=q0.75 (0.61) | d12_d34 | options excl. Phase 0 | 2 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.75 (0.42), margin>=q0.75 (0.61) | d12_d34 | options excl. Phase 0 | 5 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.75 (0.42), margin>=q0.25 (0.47) | d12_d34 | options incl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.75 (0.42), margin>=q0.25 (0.47) | d12_d34 | options incl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.75 (0.42), margin>=q0.25 (0.47) | d12_d34 | options incl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.75 (0.42), margin>=q0.50 (0.57) | d12_d34 | options incl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.75 (0.42), margin>=q0.50 (0.57) | d12_d34 | options incl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.75 (0.42), margin>=q0.50 (0.57) | d12_d34 | options incl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.75 (0.42), margin>=q0.75 (0.68) | d12_d34 | options incl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.75 (0.42), margin>=q0.75 (0.68) | d12_d34 | options incl. Phase 0 | 1 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.75 (0.42), margin>=q0.75 (0.68) | d12_d34 | options incl. Phase 0 | 1 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.75 (0.42), margin>=q0.25 (0.45) | d12_d34 | options incl. Phase 0 | 20 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.75 (0.42), margin>=q0.25 (0.45) | d12_d34 | options incl. Phase 0 | 17 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.75 (0.42), margin>=q0.25 (0.45) | d12_d34 | options incl. Phase 0 | 15 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.75 (0.42), margin>=q0.50 (0.53) | d12_d34 | options incl. Phase 0 | 14 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.75 (0.42), margin>=q0.50 (0.53) | d12_d34 | options incl. Phase 0 | 13 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.75 (0.42), margin>=q0.50 (0.53) | d12_d34 | options incl. Phase 0 | 7 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.75 (0.42), margin>=q0.75 (0.65) | d12_d34 | options incl. Phase 0 | 5 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.75 (0.42), margin>=q0.75 (0.65) | d12_d34 | options incl. Phase 0 | 5 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.75 (0.42), margin>=q0.75 (0.65) | d12_d34 | options incl. Phase 0 | 0 | 1 |
| neighbour/easy | main | n_inf=1000, self>=q0.90 (0.55), margin>=q0.25 (0.42) | d12_d34 | options excl. Phase 0 | 0 | 1 |
| neighbour/hard | main | n_inf=1000, self>=q0.90 (0.55), margin>=q0.25 (0.42) | d12_d34 | options excl. Phase 0 | 0 | 2 |
| neighbour/discovery | main | n_inf=1000, self>=q0.90 (0.55), margin>=q0.25 (0.42) | d12_d34 | options excl. Phase 0 | 0 | 1 |
| neighbour/easy | main | n_inf=1000, self>=q0.90 (0.55), margin>=q0.50 (0.54) | d12_d34 | options excl. Phase 0 | 0 | 1 |
| neighbour/hard | main | n_inf=1000, self>=q0.90 (0.55), margin>=q0.50 (0.54) | d12_d34 | options excl. Phase 0 | 0 | 3 |
| neighbour/discovery | main | n_inf=1000, self>=q0.90 (0.55), margin>=q0.50 (0.54) | d12_d34 | options excl. Phase 0 | 0 | 3 |
| neighbour/easy | main | n_inf=1000, self>=q0.90 (0.55), margin>=q0.75 (0.65) | d12_d34 | options excl. Phase 0 | 0 | 3 |
| neighbour/hard | main | n_inf=1000, self>=q0.90 (0.55), margin>=q0.75 (0.65) | d12_d34 | options excl. Phase 0 | 0 | 3 |
| neighbour/discovery | main | n_inf=1000, self>=q0.90 (0.55), margin>=q0.75 (0.65) | d12_d34 | options excl. Phase 0 | 0 | 3 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.90 (0.55), margin>=q0.25 (0.38) | d12_d34 | options excl. Phase 0 | 13 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.90 (0.55), margin>=q0.25 (0.38) | d12_d34 | options excl. Phase 0 | 10 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.90 (0.55), margin>=q0.25 (0.38) | d12_d34 | options excl. Phase 0 | 7 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.90 (0.55), margin>=q0.50 (0.47) | d12_d34 | options excl. Phase 0 | 7 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.90 (0.55), margin>=q0.50 (0.47) | d12_d34 | options excl. Phase 0 | 4 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.90 (0.55), margin>=q0.50 (0.47) | d12_d34 | options excl. Phase 0 | 3 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.90 (0.55), margin>=q0.75 (0.60) | d12_d34 | options excl. Phase 0 | 4 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.90 (0.55), margin>=q0.75 (0.60) | d12_d34 | options excl. Phase 0 | 2 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.90 (0.55), margin>=q0.75 (0.60) | d12_d34 | options excl. Phase 0 | 1 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.90 (0.55), margin>=q0.25 (0.45) | d12_d34 | options incl. Phase 0 | 0 | 1 |
| neighbour/hard | main | n_inf=1000, self>=q0.90 (0.55), margin>=q0.25 (0.45) | d12_d34 | options incl. Phase 0 | 0 | 1 |
| neighbour/discovery | main | n_inf=1000, self>=q0.90 (0.55), margin>=q0.25 (0.45) | d12_d34 | options incl. Phase 0 | 0 | 1 |
| neighbour/easy | main | n_inf=1000, self>=q0.90 (0.55), margin>=q0.50 (0.57) | d12_d34 | options incl. Phase 0 | 0 | 1 |
| neighbour/hard | main | n_inf=1000, self>=q0.90 (0.55), margin>=q0.50 (0.57) | d12_d34 | options incl. Phase 0 | 0 | 1 |
| neighbour/discovery | main | n_inf=1000, self>=q0.90 (0.55), margin>=q0.50 (0.57) | d12_d34 | options incl. Phase 0 | 0 | 1 |
| neighbour/easy | main | n_inf=1000, self>=q0.90 (0.55), margin>=q0.75 (0.66) | d12_d34 | options incl. Phase 0 | 0 | 3 |
| neighbour/hard | main | n_inf=1000, self>=q0.90 (0.55), margin>=q0.75 (0.66) | d12_d34 | options incl. Phase 0 | 0 | 3 |
| neighbour/discovery | main | n_inf=1000, self>=q0.90 (0.55), margin>=q0.75 (0.66) | d12_d34 | options incl. Phase 0 | 0 | 3 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.90 (0.55), margin>=q0.25 (0.43) | d12_d34 | options incl. Phase 0 | 14 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.90 (0.55), margin>=q0.25 (0.43) | d12_d34 | options incl. Phase 0 | 11 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.90 (0.55), margin>=q0.25 (0.43) | d12_d34 | options incl. Phase 0 | 10 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.90 (0.55), margin>=q0.50 (0.53) | d12_d34 | options incl. Phase 0 | 7 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.90 (0.55), margin>=q0.50 (0.53) | d12_d34 | options incl. Phase 0 | 5 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.90 (0.55), margin>=q0.50 (0.53) | d12_d34 | options incl. Phase 0 | 4 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.90 (0.55), margin>=q0.75 (0.68) | d12_d34 | options incl. Phase 0 | 3 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.90 (0.55), margin>=q0.75 (0.68) | d12_d34 | options incl. Phase 0 | 2 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.90 (0.55), margin>=q0.75 (0.68) | d12_d34 | options incl. Phase 0 | 0 | 1 |
| neighbour/easy | main | n_inf=1000, self>=q0.50 (0.30), margin>=q0.25 (0.44) | d14_d23 | options excl. Phase 0 | 7 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.50 (0.30), margin>=q0.25 (0.44) | d14_d23 | options excl. Phase 0 | 7 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.50 (0.30), margin>=q0.25 (0.44) | d14_d23 | options excl. Phase 0 | 5 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.50 (0.30), margin>=q0.50 (0.54) | d14_d23 | options excl. Phase 0 | 3 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.50 (0.30), margin>=q0.50 (0.54) | d14_d23 | options excl. Phase 0 | 3 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.50 (0.30), margin>=q0.50 (0.54) | d14_d23 | options excl. Phase 0 | 3 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.50 (0.30), margin>=q0.75 (0.66) | d14_d23 | options excl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.50 (0.30), margin>=q0.75 (0.66) | d14_d23 | options excl. Phase 0 | 0 | 1 |
| neighbour/discovery | main | n_inf=1000, self>=q0.50 (0.30), margin>=q0.75 (0.66) | d14_d23 | options excl. Phase 0 | 1 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.50 (0.30), margin>=q0.25 (0.43) | d14_d23 | options excl. Phase 0 | 25 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.50 (0.30), margin>=q0.25 (0.43) | d14_d23 | options excl. Phase 0 | 19 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.50 (0.30), margin>=q0.25 (0.43) | d14_d23 | options excl. Phase 0 | 16 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.50 (0.30), margin>=q0.50 (0.51) | d14_d23 | options excl. Phase 0 | 16 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.50 (0.30), margin>=q0.50 (0.51) | d14_d23 | options excl. Phase 0 | 14 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.50 (0.30), margin>=q0.50 (0.51) | d14_d23 | options excl. Phase 0 | 13 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.50 (0.30), margin>=q0.75 (0.61) | d14_d23 | options excl. Phase 0 | 9 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.50 (0.30), margin>=q0.75 (0.61) | d14_d23 | options excl. Phase 0 | 6 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.50 (0.30), margin>=q0.75 (0.61) | d14_d23 | options excl. Phase 0 | 6 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.50 (0.30), margin>=q0.25 (0.46) | d14_d23 | options incl. Phase 0 | 6 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.50 (0.30), margin>=q0.25 (0.46) | d14_d23 | options incl. Phase 0 | 5 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.50 (0.30), margin>=q0.25 (0.46) | d14_d23 | options incl. Phase 0 | 6 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.50 (0.30), margin>=q0.50 (0.56) | d14_d23 | options incl. Phase 0 | 3 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.50 (0.30), margin>=q0.50 (0.56) | d14_d23 | options incl. Phase 0 | 3 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.50 (0.30), margin>=q0.50 (0.56) | d14_d23 | options incl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.50 (0.30), margin>=q0.75 (0.68) | d14_d23 | options incl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.50 (0.30), margin>=q0.75 (0.68) | d14_d23 | options incl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.50 (0.30), margin>=q0.75 (0.68) | d14_d23 | options incl. Phase 0 | 1 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.50 (0.30), margin>=q0.25 (0.47) | d14_d23 | options incl. Phase 0 | 26 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.50 (0.30), margin>=q0.25 (0.47) | d14_d23 | options incl. Phase 0 | 20 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.50 (0.30), margin>=q0.25 (0.47) | d14_d23 | options incl. Phase 0 | 15 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.50 (0.30), margin>=q0.50 (0.55) | d14_d23 | options incl. Phase 0 | 19 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.50 (0.30), margin>=q0.50 (0.55) | d14_d23 | options incl. Phase 0 | 16 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.50 (0.30), margin>=q0.50 (0.55) | d14_d23 | options incl. Phase 0 | 11 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.50 (0.30), margin>=q0.75 (0.65) | d14_d23 | options incl. Phase 0 | 6 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.50 (0.30), margin>=q0.75 (0.65) | d14_d23 | options incl. Phase 0 | 4 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.50 (0.30), margin>=q0.75 (0.65) | d14_d23 | options incl. Phase 0 | 5 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.75 (0.44), margin>=q0.25 (0.42) | d14_d23 | options excl. Phase 0 | 3 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.75 (0.44), margin>=q0.25 (0.42) | d14_d23 | options excl. Phase 0 | 3 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.75 (0.44), margin>=q0.25 (0.42) | d14_d23 | options excl. Phase 0 | 3 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.75 (0.44), margin>=q0.50 (0.53) | d14_d23 | options excl. Phase 0 | 3 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.75 (0.44), margin>=q0.50 (0.53) | d14_d23 | options excl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.75 (0.44), margin>=q0.50 (0.53) | d14_d23 | options excl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.75 (0.44), margin>=q0.75 (0.65) | d14_d23 | options excl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.75 (0.44), margin>=q0.75 (0.65) | d14_d23 | options excl. Phase 0 | 0 | 2 |
| neighbour/discovery | main | n_inf=1000, self>=q0.75 (0.44), margin>=q0.75 (0.65) | d14_d23 | options excl. Phase 0 | 0 | 1 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.75 (0.44), margin>=q0.25 (0.42) | d14_d23 | options excl. Phase 0 | 22 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.75 (0.44), margin>=q0.25 (0.42) | d14_d23 | options excl. Phase 0 | 17 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.75 (0.44), margin>=q0.25 (0.42) | d14_d23 | options excl. Phase 0 | 15 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.75 (0.44), margin>=q0.50 (0.52) | d14_d23 | options excl. Phase 0 | 16 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.75 (0.44), margin>=q0.50 (0.52) | d14_d23 | options excl. Phase 0 | 13 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.75 (0.44), margin>=q0.50 (0.52) | d14_d23 | options excl. Phase 0 | 8 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.75 (0.44), margin>=q0.75 (0.61) | d14_d23 | options excl. Phase 0 | 10 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.75 (0.44), margin>=q0.75 (0.61) | d14_d23 | options excl. Phase 0 | 8 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.75 (0.44), margin>=q0.75 (0.61) | d14_d23 | options excl. Phase 0 | 3 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.75 (0.44), margin>=q0.25 (0.47) | d14_d23 | options incl. Phase 0 | 3 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.75 (0.44), margin>=q0.25 (0.47) | d14_d23 | options incl. Phase 0 | 3 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.75 (0.44), margin>=q0.25 (0.47) | d14_d23 | options incl. Phase 0 | 3 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.75 (0.44), margin>=q0.50 (0.56) | d14_d23 | options incl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.75 (0.44), margin>=q0.50 (0.56) | d14_d23 | options incl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.75 (0.44), margin>=q0.50 (0.56) | d14_d23 | options incl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.75 (0.44), margin>=q0.75 (0.68) | d14_d23 | options incl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.75 (0.44), margin>=q0.75 (0.68) | d14_d23 | options incl. Phase 0 | 1 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.75 (0.44), margin>=q0.75 (0.68) | d14_d23 | options incl. Phase 0 | 0 | 1 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.75 (0.44), margin>=q0.25 (0.46) | d14_d23 | options incl. Phase 0 | 23 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.75 (0.44), margin>=q0.25 (0.46) | d14_d23 | options incl. Phase 0 | 16 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.75 (0.44), margin>=q0.25 (0.46) | d14_d23 | options incl. Phase 0 | 16 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.75 (0.44), margin>=q0.50 (0.56) | d14_d23 | options incl. Phase 0 | 16 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.75 (0.44), margin>=q0.50 (0.56) | d14_d23 | options incl. Phase 0 | 12 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.75 (0.44), margin>=q0.50 (0.56) | d14_d23 | options incl. Phase 0 | 10 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.75 (0.44), margin>=q0.75 (0.70) | d14_d23 | options incl. Phase 0 | 5 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.75 (0.44), margin>=q0.75 (0.70) | d14_d23 | options incl. Phase 0 | 3 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.75 (0.44), margin>=q0.75 (0.70) | d14_d23 | options incl. Phase 0 | 5 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.90 (0.56), margin>=q0.25 (0.42) | d14_d23 | options excl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.90 (0.56), margin>=q0.25 (0.42) | d14_d23 | options excl. Phase 0 | 1 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.90 (0.56), margin>=q0.25 (0.42) | d14_d23 | options excl. Phase 0 | 0 | 1 |
| neighbour/easy | main | n_inf=1000, self>=q0.90 (0.56), margin>=q0.50 (0.55) | d14_d23 | options excl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.90 (0.56), margin>=q0.50 (0.55) | d14_d23 | options excl. Phase 0 | 0 | 2 |
| neighbour/discovery | main | n_inf=1000, self>=q0.90 (0.56), margin>=q0.50 (0.55) | d14_d23 | options excl. Phase 0 | 0 | 2 |
| neighbour/easy | main | n_inf=1000, self>=q0.90 (0.56), margin>=q0.75 (0.64) | d14_d23 | options excl. Phase 0 | 0 | 1 |
| neighbour/hard | main | n_inf=1000, self>=q0.90 (0.56), margin>=q0.75 (0.64) | d14_d23 | options excl. Phase 0 | 0 | 3 |
| neighbour/discovery | main | n_inf=1000, self>=q0.90 (0.56), margin>=q0.75 (0.64) | d14_d23 | options excl. Phase 0 | 0 | 3 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.90 (0.56), margin>=q0.25 (0.39) | d14_d23 | options excl. Phase 0 | 16 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.90 (0.56), margin>=q0.25 (0.39) | d14_d23 | options excl. Phase 0 | 9 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.90 (0.56), margin>=q0.25 (0.39) | d14_d23 | options excl. Phase 0 | 8 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.90 (0.56), margin>=q0.50 (0.50) | d14_d23 | options excl. Phase 0 | 9 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.90 (0.56), margin>=q0.50 (0.50) | d14_d23 | options excl. Phase 0 | 6 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.90 (0.56), margin>=q0.50 (0.50) | d14_d23 | options excl. Phase 0 | 3 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.90 (0.56), margin>=q0.75 (0.60) | d14_d23 | options excl. Phase 0 | 6 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.90 (0.56), margin>=q0.75 (0.60) | d14_d23 | options excl. Phase 0 | 2 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.90 (0.56), margin>=q0.75 (0.60) | d14_d23 | options excl. Phase 0 | 1 | 0 |
| neighbour/easy | main | n_inf=1000, self>=q0.90 (0.56), margin>=q0.25 (0.46) | d14_d23 | options incl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.90 (0.56), margin>=q0.25 (0.46) | d14_d23 | options incl. Phase 0 | 1 | 0 |
| neighbour/discovery | main | n_inf=1000, self>=q0.90 (0.56), margin>=q0.25 (0.46) | d14_d23 | options incl. Phase 0 | 0 | 1 |
| neighbour/easy | main | n_inf=1000, self>=q0.90 (0.56), margin>=q0.50 (0.58) | d14_d23 | options incl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=1000, self>=q0.90 (0.56), margin>=q0.50 (0.58) | d14_d23 | options incl. Phase 0 | 0 | 2 |
| neighbour/discovery | main | n_inf=1000, self>=q0.90 (0.56), margin>=q0.50 (0.58) | d14_d23 | options incl. Phase 0 | 0 | 1 |
| neighbour/easy | main | n_inf=1000, self>=q0.90 (0.56), margin>=q0.75 (0.70) | d14_d23 | options incl. Phase 0 | 0 | 1 |
| neighbour/hard | main | n_inf=1000, self>=q0.90 (0.56), margin>=q0.75 (0.70) | d14_d23 | options incl. Phase 0 | 0 | 2 |
| neighbour/discovery | main | n_inf=1000, self>=q0.90 (0.56), margin>=q0.75 (0.70) | d14_d23 | options incl. Phase 0 | 0 | 2 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.90 (0.56), margin>=q0.25 (0.46) | d14_d23 | options incl. Phase 0 | 17 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.90 (0.56), margin>=q0.25 (0.46) | d14_d23 | options incl. Phase 0 | 11 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.90 (0.56), margin>=q0.25 (0.46) | d14_d23 | options incl. Phase 0 | 8 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.90 (0.56), margin>=q0.50 (0.55) | d14_d23 | options incl. Phase 0 | 11 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.90 (0.56), margin>=q0.50 (0.55) | d14_d23 | options incl. Phase 0 | 7 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.90 (0.56), margin>=q0.50 (0.55) | d14_d23 | options incl. Phase 0 | 3 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=1000, self>=q0.90 (0.56), margin>=q0.75 (0.69) | d14_d23 | options incl. Phase 0 | 3 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=1000, self>=q0.90 (0.56), margin>=q0.75 (0.69) | d14_d23 | options incl. Phase 0 | 3 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=1000, self>=q0.90 (0.56), margin>=q0.75 (0.69) | d14_d23 | options incl. Phase 0 | 0 | 1 |
| neighbour/easy | main | n_inf=2000, self>=q0.50 (0.19), margin>=q0.25 (0.39) | all_three | options excl. Phase 0 | 6 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.50 (0.19), margin>=q0.25 (0.39) | all_three | options excl. Phase 0 | 4 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.50 (0.19), margin>=q0.25 (0.39) | all_three | options excl. Phase 0 | 4 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.50 (0.19), margin>=q0.50 (0.47) | all_three | options excl. Phase 0 | 3 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.50 (0.19), margin>=q0.50 (0.47) | all_three | options excl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.50 (0.19), margin>=q0.50 (0.47) | all_three | options excl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.50 (0.19), margin>=q0.75 (0.58) | all_three | options excl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.50 (0.19), margin>=q0.75 (0.58) | all_three | options excl. Phase 0 | 1 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.50 (0.19), margin>=q0.75 (0.58) | all_three | options excl. Phase 0 | 1 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.50 (0.19), margin>=q0.25 (0.40) | all_three | options excl. Phase 0 | 25 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.50 (0.19), margin>=q0.25 (0.40) | all_three | options excl. Phase 0 | 18 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.50 (0.19), margin>=q0.25 (0.40) | all_three | options excl. Phase 0 | 16 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.50 (0.19), margin>=q0.50 (0.49) | all_three | options excl. Phase 0 | 20 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.50 (0.19), margin>=q0.50 (0.49) | all_three | options excl. Phase 0 | 14 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.50 (0.19), margin>=q0.50 (0.49) | all_three | options excl. Phase 0 | 9 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.50 (0.19), margin>=q0.75 (0.58) | all_three | options excl. Phase 0 | 10 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.50 (0.19), margin>=q0.75 (0.58) | all_three | options excl. Phase 0 | 4 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.50 (0.19), margin>=q0.75 (0.58) | all_three | options excl. Phase 0 | 4 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.50 (0.19), margin>=q0.25 (0.41) | all_three | options incl. Phase 0 | 7 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.50 (0.19), margin>=q0.25 (0.41) | all_three | options incl. Phase 0 | 3 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.50 (0.19), margin>=q0.25 (0.41) | all_three | options incl. Phase 0 | 4 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.50 (0.19), margin>=q0.50 (0.50) | all_three | options incl. Phase 0 | 5 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.50 (0.19), margin>=q0.50 (0.50) | all_three | options incl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.50 (0.19), margin>=q0.50 (0.50) | all_three | options incl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.50 (0.19), margin>=q0.75 (0.60) | all_three | options incl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.50 (0.19), margin>=q0.75 (0.60) | all_three | options incl. Phase 0 | 1 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.50 (0.19), margin>=q0.75 (0.60) | all_three | options incl. Phase 0 | 1 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.50 (0.19), margin>=q0.25 (0.43) | all_three | options incl. Phase 0 | 26 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.50 (0.19), margin>=q0.25 (0.43) | all_three | options incl. Phase 0 | 20 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.50 (0.19), margin>=q0.25 (0.43) | all_three | options incl. Phase 0 | 15 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.50 (0.19), margin>=q0.50 (0.54) | all_three | options incl. Phase 0 | 18 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.50 (0.19), margin>=q0.50 (0.54) | all_three | options incl. Phase 0 | 13 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.50 (0.19), margin>=q0.50 (0.54) | all_three | options incl. Phase 0 | 11 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.50 (0.19), margin>=q0.75 (0.65) | all_three | options incl. Phase 0 | 5 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.50 (0.19), margin>=q0.75 (0.65) | all_three | options incl. Phase 0 | 4 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.50 (0.19), margin>=q0.75 (0.65) | all_three | options incl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.75 (0.32), margin>=q0.25 (0.38) | all_three | options excl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.75 (0.32), margin>=q0.25 (0.38) | all_three | options excl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.75 (0.32), margin>=q0.25 (0.38) | all_three | options excl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.75 (0.32), margin>=q0.50 (0.48) | all_three | options excl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.75 (0.32), margin>=q0.50 (0.48) | all_three | options excl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.75 (0.32), margin>=q0.50 (0.48) | all_three | options excl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.75 (0.32), margin>=q0.75 (0.57) | all_three | options excl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.75 (0.32), margin>=q0.75 (0.57) | all_three | options excl. Phase 0 | 0 | 1 |
| neighbour/discovery | main | n_inf=2000, self>=q0.75 (0.32), margin>=q0.75 (0.57) | all_three | options excl. Phase 0 | 0 | 1 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.75 (0.32), margin>=q0.25 (0.38) | all_three | options excl. Phase 0 | 18 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.75 (0.32), margin>=q0.25 (0.38) | all_three | options excl. Phase 0 | 17 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.75 (0.32), margin>=q0.25 (0.38) | all_three | options excl. Phase 0 | 12 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.75 (0.32), margin>=q0.50 (0.47) | all_three | options excl. Phase 0 | 12 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.75 (0.32), margin>=q0.50 (0.47) | all_three | options excl. Phase 0 | 11 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.75 (0.32), margin>=q0.50 (0.47) | all_three | options excl. Phase 0 | 8 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.75 (0.32), margin>=q0.75 (0.58) | all_three | options excl. Phase 0 | 8 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.75 (0.32), margin>=q0.75 (0.58) | all_three | options excl. Phase 0 | 5 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.75 (0.32), margin>=q0.75 (0.58) | all_three | options excl. Phase 0 | 0 | 1 |
| neighbour/easy | main | n_inf=2000, self>=q0.75 (0.32), margin>=q0.25 (0.41) | all_three | options incl. Phase 0 | 3 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.75 (0.32), margin>=q0.25 (0.41) | all_three | options incl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.75 (0.32), margin>=q0.25 (0.41) | all_three | options incl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.75 (0.32), margin>=q0.50 (0.50) | all_three | options incl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.75 (0.32), margin>=q0.50 (0.50) | all_three | options incl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.75 (0.32), margin>=q0.50 (0.50) | all_three | options incl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.75 (0.32), margin>=q0.75 (0.60) | all_three | options incl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.75 (0.32), margin>=q0.75 (0.60) | all_three | options incl. Phase 0 | 1 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.75 (0.32), margin>=q0.75 (0.60) | all_three | options incl. Phase 0 | 1 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.75 (0.32), margin>=q0.25 (0.42) | all_three | options incl. Phase 0 | 22 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.75 (0.32), margin>=q0.25 (0.42) | all_three | options incl. Phase 0 | 15 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.75 (0.32), margin>=q0.25 (0.42) | all_three | options incl. Phase 0 | 13 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.75 (0.32), margin>=q0.50 (0.51) | all_three | options incl. Phase 0 | 14 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.75 (0.32), margin>=q0.50 (0.51) | all_three | options incl. Phase 0 | 11 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.75 (0.32), margin>=q0.50 (0.51) | all_three | options incl. Phase 0 | 8 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.75 (0.32), margin>=q0.75 (0.63) | all_three | options incl. Phase 0 | 5 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.75 (0.32), margin>=q0.75 (0.63) | all_three | options incl. Phase 0 | 1 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.75 (0.32), margin>=q0.75 (0.63) | all_three | options incl. Phase 0 | 1 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.90 (0.45), margin>=q0.25 (0.34) | all_three | options excl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.90 (0.45), margin>=q0.25 (0.34) | all_three | options excl. Phase 0 | 1 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.90 (0.45), margin>=q0.25 (0.34) | all_three | options excl. Phase 0 | 1 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.90 (0.45), margin>=q0.50 (0.45) | all_three | options excl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.90 (0.45), margin>=q0.50 (0.45) | all_three | options excl. Phase 0 | 1 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.90 (0.45), margin>=q0.50 (0.45) | all_three | options excl. Phase 0 | 0 | 1 |
| neighbour/easy | main | n_inf=2000, self>=q0.90 (0.45), margin>=q0.75 (0.57) | all_three | options excl. Phase 0 | 0 | 3 |
| neighbour/hard | main | n_inf=2000, self>=q0.90 (0.45), margin>=q0.75 (0.57) | all_three | options excl. Phase 0 | 0 | 3 |
| neighbour/discovery | main | n_inf=2000, self>=q0.90 (0.45), margin>=q0.75 (0.57) | all_three | options excl. Phase 0 | 0 | 3 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.90 (0.45), margin>=q0.25 (0.35) | all_three | options excl. Phase 0 | 14 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.90 (0.45), margin>=q0.25 (0.35) | all_three | options excl. Phase 0 | 11 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.90 (0.45), margin>=q0.25 (0.35) | all_three | options excl. Phase 0 | 8 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.90 (0.45), margin>=q0.50 (0.45) | all_three | options excl. Phase 0 | 9 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.90 (0.45), margin>=q0.50 (0.45) | all_three | options excl. Phase 0 | 6 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.90 (0.45), margin>=q0.50 (0.45) | all_three | options excl. Phase 0 | 4 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.90 (0.45), margin>=q0.75 (0.58) | all_three | options excl. Phase 0 | 2 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.90 (0.45), margin>=q0.75 (0.58) | all_three | options excl. Phase 0 | 3 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.90 (0.45), margin>=q0.75 (0.58) | all_three | options excl. Phase 0 | 1 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.90 (0.45), margin>=q0.25 (0.39) | all_three | options incl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.90 (0.45), margin>=q0.25 (0.39) | all_three | options incl. Phase 0 | 1 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.90 (0.45), margin>=q0.25 (0.39) | all_three | options incl. Phase 0 | 1 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.90 (0.45), margin>=q0.50 (0.50) | all_three | options incl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.90 (0.45), margin>=q0.50 (0.50) | all_three | options incl. Phase 0 | 0 | 1 |
| neighbour/discovery | main | n_inf=2000, self>=q0.90 (0.45), margin>=q0.50 (0.50) | all_three | options incl. Phase 0 | 0 | 1 |
| neighbour/easy | main | n_inf=2000, self>=q0.90 (0.45), margin>=q0.75 (0.62) | all_three | options incl. Phase 0 | 0 | 2 |
| neighbour/hard | main | n_inf=2000, self>=q0.90 (0.45), margin>=q0.75 (0.62) | all_three | options incl. Phase 0 | 0 | 3 |
| neighbour/discovery | main | n_inf=2000, self>=q0.90 (0.45), margin>=q0.75 (0.62) | all_three | options incl. Phase 0 | 0 | 3 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.90 (0.45), margin>=q0.25 (0.38) | all_three | options incl. Phase 0 | 13 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.90 (0.45), margin>=q0.25 (0.38) | all_three | options incl. Phase 0 | 10 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.90 (0.45), margin>=q0.25 (0.38) | all_three | options incl. Phase 0 | 8 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.90 (0.45), margin>=q0.50 (0.51) | all_three | options incl. Phase 0 | 9 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.90 (0.45), margin>=q0.50 (0.51) | all_three | options incl. Phase 0 | 5 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.90 (0.45), margin>=q0.50 (0.51) | all_three | options incl. Phase 0 | 5 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.90 (0.45), margin>=q0.75 (0.64) | all_three | options incl. Phase 0 | 3 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.90 (0.45), margin>=q0.75 (0.64) | all_three | options incl. Phase 0 | 1 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.90 (0.45), margin>=q0.75 (0.64) | all_three | options incl. Phase 0 | 0 | 2 |
| neighbour/easy | main | n_inf=2000, self>=q0.50 (0.24), margin>=q0.25 (0.37) | d12_d34 | options excl. Phase 0 | 5 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.50 (0.24), margin>=q0.25 (0.37) | d12_d34 | options excl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.50 (0.24), margin>=q0.25 (0.37) | d12_d34 | options excl. Phase 0 | 4 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.50 (0.24), margin>=q0.50 (0.47) | d12_d34 | options excl. Phase 0 | 3 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.50 (0.24), margin>=q0.50 (0.47) | d12_d34 | options excl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.50 (0.24), margin>=q0.50 (0.47) | d12_d34 | options excl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.50 (0.24), margin>=q0.75 (0.58) | d12_d34 | options excl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.50 (0.24), margin>=q0.75 (0.58) | d12_d34 | options excl. Phase 0 | 0 | 1 |
| neighbour/discovery | main | n_inf=2000, self>=q0.50 (0.24), margin>=q0.75 (0.58) | d12_d34 | options excl. Phase 0 | 1 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.50 (0.24), margin>=q0.25 (0.39) | d12_d34 | options excl. Phase 0 | 23 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.50 (0.24), margin>=q0.25 (0.39) | d12_d34 | options excl. Phase 0 | 20 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.50 (0.24), margin>=q0.25 (0.39) | d12_d34 | options excl. Phase 0 | 16 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.50 (0.24), margin>=q0.50 (0.49) | d12_d34 | options excl. Phase 0 | 20 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.50 (0.24), margin>=q0.50 (0.49) | d12_d34 | options excl. Phase 0 | 14 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.50 (0.24), margin>=q0.50 (0.49) | d12_d34 | options excl. Phase 0 | 11 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.50 (0.24), margin>=q0.75 (0.58) | d12_d34 | options excl. Phase 0 | 10 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.50 (0.24), margin>=q0.75 (0.58) | d12_d34 | options excl. Phase 0 | 6 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.50 (0.24), margin>=q0.75 (0.58) | d12_d34 | options excl. Phase 0 | 5 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.50 (0.24), margin>=q0.25 (0.40) | d12_d34 | options incl. Phase 0 | 8 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.50 (0.24), margin>=q0.25 (0.40) | d12_d34 | options incl. Phase 0 | 4 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.50 (0.24), margin>=q0.25 (0.40) | d12_d34 | options incl. Phase 0 | 3 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.50 (0.24), margin>=q0.50 (0.50) | d12_d34 | options incl. Phase 0 | 4 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.50 (0.24), margin>=q0.50 (0.50) | d12_d34 | options incl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.50 (0.24), margin>=q0.50 (0.50) | d12_d34 | options incl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.50 (0.24), margin>=q0.75 (0.60) | d12_d34 | options incl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.50 (0.24), margin>=q0.75 (0.60) | d12_d34 | options incl. Phase 0 | 1 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.50 (0.24), margin>=q0.75 (0.60) | d12_d34 | options incl. Phase 0 | 2 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.50 (0.24), margin>=q0.25 (0.43) | d12_d34 | options incl. Phase 0 | 29 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.50 (0.24), margin>=q0.25 (0.43) | d12_d34 | options incl. Phase 0 | 22 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.50 (0.24), margin>=q0.25 (0.43) | d12_d34 | options incl. Phase 0 | 16 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.50 (0.24), margin>=q0.50 (0.51) | d12_d34 | options incl. Phase 0 | 21 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.50 (0.24), margin>=q0.50 (0.51) | d12_d34 | options incl. Phase 0 | 14 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.50 (0.24), margin>=q0.50 (0.51) | d12_d34 | options incl. Phase 0 | 10 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.50 (0.24), margin>=q0.75 (0.64) | d12_d34 | options incl. Phase 0 | 4 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.50 (0.24), margin>=q0.75 (0.64) | d12_d34 | options incl. Phase 0 | 5 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.50 (0.24), margin>=q0.75 (0.64) | d12_d34 | options incl. Phase 0 | 4 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.75 (0.37), margin>=q0.25 (0.36) | d12_d34 | options excl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.75 (0.37), margin>=q0.25 (0.36) | d12_d34 | options excl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.75 (0.37), margin>=q0.25 (0.36) | d12_d34 | options excl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.75 (0.37), margin>=q0.50 (0.48) | d12_d34 | options excl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.75 (0.37), margin>=q0.50 (0.48) | d12_d34 | options excl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.75 (0.37), margin>=q0.50 (0.48) | d12_d34 | options excl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.75 (0.37), margin>=q0.75 (0.57) | d12_d34 | options excl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.75 (0.37), margin>=q0.75 (0.57) | d12_d34 | options excl. Phase 0 | 0 | 1 |
| neighbour/discovery | main | n_inf=2000, self>=q0.75 (0.37), margin>=q0.75 (0.57) | d12_d34 | options excl. Phase 0 | 0 | 1 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.75 (0.37), margin>=q0.25 (0.37) | d12_d34 | options excl. Phase 0 | 21 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.75 (0.37), margin>=q0.25 (0.37) | d12_d34 | options excl. Phase 0 | 19 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.75 (0.37), margin>=q0.25 (0.37) | d12_d34 | options excl. Phase 0 | 14 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.75 (0.37), margin>=q0.50 (0.45) | d12_d34 | options excl. Phase 0 | 14 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.75 (0.37), margin>=q0.50 (0.45) | d12_d34 | options excl. Phase 0 | 10 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.75 (0.37), margin>=q0.50 (0.45) | d12_d34 | options excl. Phase 0 | 8 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.75 (0.37), margin>=q0.75 (0.56) | d12_d34 | options excl. Phase 0 | 5 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.75 (0.37), margin>=q0.75 (0.56) | d12_d34 | options excl. Phase 0 | 7 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.75 (0.37), margin>=q0.75 (0.56) | d12_d34 | options excl. Phase 0 | 3 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.75 (0.37), margin>=q0.25 (0.40) | d12_d34 | options incl. Phase 0 | 3 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.75 (0.37), margin>=q0.25 (0.40) | d12_d34 | options incl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.75 (0.37), margin>=q0.25 (0.40) | d12_d34 | options incl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.75 (0.37), margin>=q0.50 (0.50) | d12_d34 | options incl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.75 (0.37), margin>=q0.50 (0.50) | d12_d34 | options incl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.75 (0.37), margin>=q0.50 (0.50) | d12_d34 | options incl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.75 (0.37), margin>=q0.75 (0.60) | d12_d34 | options incl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.75 (0.37), margin>=q0.75 (0.60) | d12_d34 | options incl. Phase 0 | 0 | 1 |
| neighbour/discovery | main | n_inf=2000, self>=q0.75 (0.37), margin>=q0.75 (0.60) | d12_d34 | options incl. Phase 0 | 2 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.75 (0.37), margin>=q0.25 (0.40) | d12_d34 | options incl. Phase 0 | 23 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.75 (0.37), margin>=q0.25 (0.40) | d12_d34 | options incl. Phase 0 | 17 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.75 (0.37), margin>=q0.25 (0.40) | d12_d34 | options incl. Phase 0 | 13 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.75 (0.37), margin>=q0.50 (0.50) | d12_d34 | options incl. Phase 0 | 16 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.75 (0.37), margin>=q0.50 (0.50) | d12_d34 | options incl. Phase 0 | 12 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.75 (0.37), margin>=q0.50 (0.50) | d12_d34 | options incl. Phase 0 | 4 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.75 (0.37), margin>=q0.75 (0.62) | d12_d34 | options incl. Phase 0 | 4 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.75 (0.37), margin>=q0.75 (0.62) | d12_d34 | options incl. Phase 0 | 0 | 1 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.75 (0.37), margin>=q0.75 (0.62) | d12_d34 | options incl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.90 (0.49), margin>=q0.25 (0.34) | d12_d34 | options excl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.90 (0.49), margin>=q0.25 (0.34) | d12_d34 | options excl. Phase 0 | 0 | 1 |
| neighbour/discovery | main | n_inf=2000, self>=q0.90 (0.49), margin>=q0.25 (0.34) | d12_d34 | options excl. Phase 0 | 0 | 1 |
| neighbour/easy | main | n_inf=2000, self>=q0.90 (0.49), margin>=q0.50 (0.43) | d12_d34 | options excl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.90 (0.49), margin>=q0.50 (0.43) | d12_d34 | options excl. Phase 0 | 0 | 1 |
| neighbour/discovery | main | n_inf=2000, self>=q0.90 (0.49), margin>=q0.50 (0.43) | d12_d34 | options excl. Phase 0 | 0 | 2 |
| neighbour/easy | main | n_inf=2000, self>=q0.90 (0.49), margin>=q0.75 (0.56) | d12_d34 | options excl. Phase 0 | 0 | 1 |
| neighbour/hard | main | n_inf=2000, self>=q0.90 (0.49), margin>=q0.75 (0.56) | d12_d34 | options excl. Phase 0 | 0 | 3 |
| neighbour/discovery | main | n_inf=2000, self>=q0.90 (0.49), margin>=q0.75 (0.56) | d12_d34 | options excl. Phase 0 | 0 | 3 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.90 (0.49), margin>=q0.25 (0.35) | d12_d34 | options excl. Phase 0 | 13 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.90 (0.49), margin>=q0.25 (0.35) | d12_d34 | options excl. Phase 0 | 8 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.90 (0.49), margin>=q0.25 (0.35) | d12_d34 | options excl. Phase 0 | 12 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.90 (0.49), margin>=q0.50 (0.42) | d12_d34 | options excl. Phase 0 | 6 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.90 (0.49), margin>=q0.50 (0.42) | d12_d34 | options excl. Phase 0 | 4 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.90 (0.49), margin>=q0.50 (0.42) | d12_d34 | options excl. Phase 0 | 5 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.90 (0.49), margin>=q0.75 (0.56) | d12_d34 | options excl. Phase 0 | 2 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.90 (0.49), margin>=q0.75 (0.56) | d12_d34 | options excl. Phase 0 | 2 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.90 (0.49), margin>=q0.75 (0.56) | d12_d34 | options excl. Phase 0 | 1 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.90 (0.49), margin>=q0.25 (0.38) | d12_d34 | options incl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.90 (0.49), margin>=q0.25 (0.38) | d12_d34 | options incl. Phase 0 | 0 | 1 |
| neighbour/discovery | main | n_inf=2000, self>=q0.90 (0.49), margin>=q0.25 (0.38) | d12_d34 | options incl. Phase 0 | 0 | 1 |
| neighbour/easy | main | n_inf=2000, self>=q0.90 (0.49), margin>=q0.50 (0.47) | d12_d34 | options incl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.90 (0.49), margin>=q0.50 (0.47) | d12_d34 | options incl. Phase 0 | 0 | 1 |
| neighbour/discovery | main | n_inf=2000, self>=q0.90 (0.49), margin>=q0.50 (0.47) | d12_d34 | options incl. Phase 0 | 0 | 1 |
| neighbour/easy | main | n_inf=2000, self>=q0.90 (0.49), margin>=q0.75 (0.60) | d12_d34 | options incl. Phase 0 | 0 | 2 |
| neighbour/hard | main | n_inf=2000, self>=q0.90 (0.49), margin>=q0.75 (0.60) | d12_d34 | options incl. Phase 0 | 0 | 3 |
| neighbour/discovery | main | n_inf=2000, self>=q0.90 (0.49), margin>=q0.75 (0.60) | d12_d34 | options incl. Phase 0 | 0 | 3 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.90 (0.49), margin>=q0.25 (0.41) | d12_d34 | options incl. Phase 0 | 16 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.90 (0.49), margin>=q0.25 (0.41) | d12_d34 | options incl. Phase 0 | 11 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.90 (0.49), margin>=q0.25 (0.41) | d12_d34 | options incl. Phase 0 | 10 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.90 (0.49), margin>=q0.50 (0.50) | d12_d34 | options incl. Phase 0 | 10 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.90 (0.49), margin>=q0.50 (0.50) | d12_d34 | options incl. Phase 0 | 6 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.90 (0.49), margin>=q0.50 (0.50) | d12_d34 | options incl. Phase 0 | 3 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.90 (0.49), margin>=q0.75 (0.63) | d12_d34 | options incl. Phase 0 | 4 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.90 (0.49), margin>=q0.75 (0.63) | d12_d34 | options incl. Phase 0 | 2 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.90 (0.49), margin>=q0.75 (0.63) | d12_d34 | options incl. Phase 0 | 0 | 1 |
| neighbour/easy | main | n_inf=2000, self>=q0.50 (0.26), margin>=q0.25 (0.38) | d14_d23 | options excl. Phase 0 | 7 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.50 (0.26), margin>=q0.25 (0.38) | d14_d23 | options excl. Phase 0 | 3 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.50 (0.26), margin>=q0.25 (0.38) | d14_d23 | options excl. Phase 0 | 3 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.50 (0.26), margin>=q0.50 (0.47) | d14_d23 | options excl. Phase 0 | 4 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.50 (0.26), margin>=q0.50 (0.47) | d14_d23 | options excl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.50 (0.26), margin>=q0.50 (0.47) | d14_d23 | options excl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.50 (0.26), margin>=q0.75 (0.59) | d14_d23 | options excl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.50 (0.26), margin>=q0.75 (0.59) | d14_d23 | options excl. Phase 0 | 1 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.50 (0.26), margin>=q0.75 (0.59) | d14_d23 | options excl. Phase 0 | 0 | 1 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.50 (0.26), margin>=q0.25 (0.39) | d14_d23 | options excl. Phase 0 | 28 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.50 (0.26), margin>=q0.25 (0.39) | d14_d23 | options excl. Phase 0 | 23 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.50 (0.26), margin>=q0.25 (0.39) | d14_d23 | options excl. Phase 0 | 18 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.50 (0.26), margin>=q0.50 (0.48) | d14_d23 | options excl. Phase 0 | 20 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.50 (0.26), margin>=q0.50 (0.48) | d14_d23 | options excl. Phase 0 | 16 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.50 (0.26), margin>=q0.50 (0.48) | d14_d23 | options excl. Phase 0 | 9 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.50 (0.26), margin>=q0.75 (0.59) | d14_d23 | options excl. Phase 0 | 11 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.50 (0.26), margin>=q0.75 (0.59) | d14_d23 | options excl. Phase 0 | 6 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.50 (0.26), margin>=q0.75 (0.59) | d14_d23 | options excl. Phase 0 | 3 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.50 (0.26), margin>=q0.25 (0.40) | d14_d23 | options incl. Phase 0 | 7 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.50 (0.26), margin>=q0.25 (0.40) | d14_d23 | options incl. Phase 0 | 3 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.50 (0.26), margin>=q0.25 (0.40) | d14_d23 | options incl. Phase 0 | 3 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.50 (0.26), margin>=q0.50 (0.50) | d14_d23 | options incl. Phase 0 | 4 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.50 (0.26), margin>=q0.50 (0.50) | d14_d23 | options incl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.50 (0.26), margin>=q0.50 (0.50) | d14_d23 | options incl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.50 (0.26), margin>=q0.75 (0.60) | d14_d23 | options incl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.50 (0.26), margin>=q0.75 (0.60) | d14_d23 | options incl. Phase 0 | 1 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.50 (0.26), margin>=q0.75 (0.60) | d14_d23 | options incl. Phase 0 | 1 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.50 (0.26), margin>=q0.25 (0.42) | d14_d23 | options incl. Phase 0 | 26 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.50 (0.26), margin>=q0.25 (0.42) | d14_d23 | options incl. Phase 0 | 22 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.50 (0.26), margin>=q0.25 (0.42) | d14_d23 | options incl. Phase 0 | 19 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.50 (0.26), margin>=q0.50 (0.51) | d14_d23 | options incl. Phase 0 | 21 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.50 (0.26), margin>=q0.50 (0.51) | d14_d23 | options incl. Phase 0 | 16 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.50 (0.26), margin>=q0.50 (0.51) | d14_d23 | options incl. Phase 0 | 8 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.50 (0.26), margin>=q0.75 (0.62) | d14_d23 | options incl. Phase 0 | 5 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.50 (0.26), margin>=q0.75 (0.62) | d14_d23 | options incl. Phase 0 | 4 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.50 (0.26), margin>=q0.75 (0.62) | d14_d23 | options incl. Phase 0 | 1 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.75 (0.38), margin>=q0.25 (0.35) | d14_d23 | options excl. Phase 0 | 3 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.75 (0.38), margin>=q0.25 (0.35) | d14_d23 | options excl. Phase 0 | 3 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.75 (0.38), margin>=q0.25 (0.35) | d14_d23 | options excl. Phase 0 | 3 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.75 (0.38), margin>=q0.50 (0.46) | d14_d23 | options excl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.75 (0.38), margin>=q0.50 (0.46) | d14_d23 | options excl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.75 (0.38), margin>=q0.50 (0.46) | d14_d23 | options excl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.75 (0.38), margin>=q0.75 (0.57) | d14_d23 | options excl. Phase 0 | 2 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.75 (0.38), margin>=q0.75 (0.57) | d14_d23 | options excl. Phase 0 | 0 | 1 |
| neighbour/discovery | main | n_inf=2000, self>=q0.75 (0.38), margin>=q0.75 (0.57) | d14_d23 | options excl. Phase 0 | 0 | 2 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.75 (0.38), margin>=q0.25 (0.39) | d14_d23 | options excl. Phase 0 | 21 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.75 (0.38), margin>=q0.25 (0.39) | d14_d23 | options excl. Phase 0 | 18 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.75 (0.38), margin>=q0.25 (0.39) | d14_d23 | options excl. Phase 0 | 15 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.75 (0.38), margin>=q0.50 (0.47) | d14_d23 | options excl. Phase 0 | 16 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.75 (0.38), margin>=q0.50 (0.47) | d14_d23 | options excl. Phase 0 | 12 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.75 (0.38), margin>=q0.50 (0.47) | d14_d23 | options excl. Phase 0 | 10 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.75 (0.38), margin>=q0.75 (0.58) | d14_d23 | options excl. Phase 0 | 8 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.75 (0.38), margin>=q0.75 (0.58) | d14_d23 | options excl. Phase 0 | 4 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.75 (0.38), margin>=q0.75 (0.58) | d14_d23 | options excl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.75 (0.38), margin>=q0.25 (0.38) | d14_d23 | options incl. Phase 0 | 5 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.75 (0.38), margin>=q0.25 (0.38) | d14_d23 | options incl. Phase 0 | 3 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.75 (0.38), margin>=q0.25 (0.38) | d14_d23 | options incl. Phase 0 | 3 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.75 (0.38), margin>=q0.50 (0.49) | d14_d23 | options incl. Phase 0 | 3 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.75 (0.38), margin>=q0.50 (0.49) | d14_d23 | options incl. Phase 0 | 2 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.75 (0.38), margin>=q0.50 (0.49) | d14_d23 | options incl. Phase 0 | 2 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.75 (0.38), margin>=q0.75 (0.60) | d14_d23 | options incl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.75 (0.38), margin>=q0.75 (0.60) | d14_d23 | options incl. Phase 0 | 1 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.75 (0.38), margin>=q0.75 (0.60) | d14_d23 | options incl. Phase 0 | 0 | 1 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.75 (0.38), margin>=q0.25 (0.42) | d14_d23 | options incl. Phase 0 | 24 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.75 (0.38), margin>=q0.25 (0.42) | d14_d23 | options incl. Phase 0 | 20 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.75 (0.38), margin>=q0.25 (0.42) | d14_d23 | options incl. Phase 0 | 15 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.75 (0.38), margin>=q0.50 (0.52) | d14_d23 | options incl. Phase 0 | 17 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.75 (0.38), margin>=q0.50 (0.52) | d14_d23 | options incl. Phase 0 | 13 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.75 (0.38), margin>=q0.50 (0.52) | d14_d23 | options incl. Phase 0 | 8 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.75 (0.38), margin>=q0.75 (0.65) | d14_d23 | options incl. Phase 0 | 6 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.75 (0.38), margin>=q0.75 (0.65) | d14_d23 | options incl. Phase 0 | 2 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.75 (0.38), margin>=q0.75 (0.65) | d14_d23 | options incl. Phase 0 | 3 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.90 (0.50), margin>=q0.25 (0.31) | d14_d23 | options excl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.90 (0.50), margin>=q0.25 (0.31) | d14_d23 | options excl. Phase 0 | 1 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.90 (0.50), margin>=q0.25 (0.31) | d14_d23 | options excl. Phase 0 | 1 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.90 (0.50), margin>=q0.50 (0.44) | d14_d23 | options excl. Phase 0 | 0 | 1 |
| neighbour/hard | main | n_inf=2000, self>=q0.90 (0.50), margin>=q0.50 (0.44) | d14_d23 | options excl. Phase 0 | 0 | 1 |
| neighbour/discovery | main | n_inf=2000, self>=q0.90 (0.50), margin>=q0.50 (0.44) | d14_d23 | options excl. Phase 0 | 0 | 2 |
| neighbour/easy | main | n_inf=2000, self>=q0.90 (0.50), margin>=q0.75 (0.58) | d14_d23 | options excl. Phase 0 | 0 | 2 |
| neighbour/hard | main | n_inf=2000, self>=q0.90 (0.50), margin>=q0.75 (0.58) | d14_d23 | options excl. Phase 0 | 0 | 3 |
| neighbour/discovery | main | n_inf=2000, self>=q0.90 (0.50), margin>=q0.75 (0.58) | d14_d23 | options excl. Phase 0 | 0 | 3 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.90 (0.50), margin>=q0.25 (0.33) | d14_d23 | options excl. Phase 0 | 13 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.90 (0.50), margin>=q0.25 (0.33) | d14_d23 | options excl. Phase 0 | 13 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.90 (0.50), margin>=q0.25 (0.33) | d14_d23 | options excl. Phase 0 | 10 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.90 (0.50), margin>=q0.50 (0.42) | d14_d23 | options excl. Phase 0 | 5 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.90 (0.50), margin>=q0.50 (0.42) | d14_d23 | options excl. Phase 0 | 6 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.90 (0.50), margin>=q0.50 (0.42) | d14_d23 | options excl. Phase 0 | 6 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.90 (0.50), margin>=q0.75 (0.56) | d14_d23 | options excl. Phase 0 | 3 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.90 (0.50), margin>=q0.75 (0.56) | d14_d23 | options excl. Phase 0 | 1 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.90 (0.50), margin>=q0.75 (0.56) | d14_d23 | options excl. Phase 0 | 1 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.90 (0.50), margin>=q0.25 (0.37) | d14_d23 | options incl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.90 (0.50), margin>=q0.25 (0.37) | d14_d23 | options incl. Phase 0 | 1 | 0 |
| neighbour/discovery | main | n_inf=2000, self>=q0.90 (0.50), margin>=q0.25 (0.37) | d14_d23 | options incl. Phase 0 | 1 | 0 |
| neighbour/easy | main | n_inf=2000, self>=q0.90 (0.50), margin>=q0.50 (0.46) | d14_d23 | options incl. Phase 0 | 1 | 0 |
| neighbour/hard | main | n_inf=2000, self>=q0.90 (0.50), margin>=q0.50 (0.46) | d14_d23 | options incl. Phase 0 | 0 | 1 |
| neighbour/discovery | main | n_inf=2000, self>=q0.90 (0.50), margin>=q0.50 (0.46) | d14_d23 | options incl. Phase 0 | 0 | 1 |
| neighbour/easy | main | n_inf=2000, self>=q0.90 (0.50), margin>=q0.75 (0.61) | d14_d23 | options incl. Phase 0 | 0 | 3 |
| neighbour/hard | main | n_inf=2000, self>=q0.90 (0.50), margin>=q0.75 (0.61) | d14_d23 | options incl. Phase 0 | 0 | 3 |
| neighbour/discovery | main | n_inf=2000, self>=q0.90 (0.50), margin>=q0.75 (0.61) | d14_d23 | options incl. Phase 0 | 0 | 3 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.90 (0.50), margin>=q0.25 (0.42) | d14_d23 | options incl. Phase 0 | 14 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.90 (0.50), margin>=q0.25 (0.42) | d14_d23 | options incl. Phase 0 | 9 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.90 (0.50), margin>=q0.25 (0.42) | d14_d23 | options incl. Phase 0 | 8 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.90 (0.50), margin>=q0.50 (0.51) | d14_d23 | options incl. Phase 0 | 8 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.90 (0.50), margin>=q0.50 (0.51) | d14_d23 | options incl. Phase 0 | 6 | 0 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.90 (0.50), margin>=q0.50 (0.51) | d14_d23 | options incl. Phase 0 | 3 | 0 |
| neighbour/easy | flagged (pooled) | n_inf=2000, self>=q0.90 (0.50), margin>=q0.75 (0.66) | d14_d23 | options incl. Phase 0 | 3 | 0 |
| neighbour/hard | flagged (pooled) | n_inf=2000, self>=q0.90 (0.50), margin>=q0.75 (0.66) | d14_d23 | options incl. Phase 0 | 0 | 1 |
| neighbour/discovery | flagged (pooled) | n_inf=2000, self>=q0.90 (0.50), margin>=q0.75 (0.66) | d14_d23 | options incl. Phase 0 | 1 | 0 |

## F-readout filter and strata picked by the D-023 order, by per-cell count

Order: all_three with effect tercile, then d12_d34 with effect tercile, then d14_d23 with effect tercile, then all_three with no tercile, then d12_d34 with no tercile, then d14_d23 with no tercile.

| parameters | per_cell | picked |
|---|---|---|
| R=20, top_k=50 | 1 | d12_d34 + effect tercile |
| R=20, top_k=50 | 2 | d12_d34 + effect tercile |
| R=20, top_k=50 | 3 | d12_d34 + effect tercile |
| R=20, top_k=50 | 4 | d12_d34 + effect tercile |
| R=20, top_k=50 | 5 | all_three + no tercile |
| R=20, top_k=50 | 8 | all_three + no tercile |
| R=20, top_k=50 | 10 | d12_d34 + no tercile |
| R=20, top_k=50 | 15 | d12_d34 + no tercile |
| R=20, top_k=50 | 19 | d12_d34 + no tercile |
| R=20, top_k=50 | 20 | none fills |
| R=20, top_k=all | 1 | d12_d34 + effect tercile |
| R=20, top_k=all | 2 | d12_d34 + effect tercile |
| R=20, top_k=all | 3 | d12_d34 + effect tercile |
| R=20, top_k=all | 4 | d12_d34 + effect tercile |
| R=20, top_k=all | 5 | d12_d34 + effect tercile |
| R=20, top_k=all | 8 | all_three + no tercile |
| R=20, top_k=all | 10 | d12_d34 + no tercile |
| R=20, top_k=all | 15 | d12_d34 + no tercile |
| R=20, top_k=all | 19 | d12_d34 + no tercile |
| R=20, top_k=all | 20 | none fills |
| R=5, top_k=50 | 1 | d12_d34 + effect tercile |
| R=5, top_k=50 | 2 | d12_d34 + effect tercile |
| R=5, top_k=50 | 3 | d12_d34 + effect tercile |
| R=5, top_k=50 | 4 | d12_d34 + effect tercile |
| R=5, top_k=50 | 5 | all_three + no tercile |
| R=5, top_k=50 | 8 | all_three + no tercile |
| R=5, top_k=50 | 10 | d12_d34 + no tercile |
| R=5, top_k=50 | 15 | d12_d34 + no tercile |
| R=5, top_k=50 | 19 | d12_d34 + no tercile |
| R=5, top_k=50 | 20 | none fills |
| R=5, top_k=all | 1 | d12_d34 + effect tercile |
| R=5, top_k=all | 2 | d12_d34 + effect tercile |
| R=5, top_k=all | 3 | d12_d34 + effect tercile |
| R=5, top_k=all | 4 | d12_d34 + effect tercile |
| R=5, top_k=all | 5 | d12_d34 + effect tercile |
| R=5, top_k=all | 8 | all_three + no tercile |
| R=5, top_k=all | 10 | d12_d34 + no tercile |
| R=5, top_k=all | 15 | d12_d34 + no tercile |
| R=5, top_k=all | 19 | d12_d34 + no tercile |
| R=5, top_k=all | 20 | none fills |
| R=50, top_k=50 | 1 | d12_d34 + effect tercile |
| R=50, top_k=50 | 2 | d12_d34 + effect tercile |
| R=50, top_k=50 | 3 | d12_d34 + effect tercile |
| R=50, top_k=50 | 4 | d12_d34 + effect tercile |
| R=50, top_k=50 | 5 | all_three + no tercile |
| R=50, top_k=50 | 8 | all_three + no tercile |
| R=50, top_k=50 | 10 | d12_d34 + no tercile |
| R=50, top_k=50 | 15 | d12_d34 + no tercile |
| R=50, top_k=50 | 19 | d12_d34 + no tercile |
| R=50, top_k=50 | 20 | none fills |
| R=50, top_k=all | 1 | d12_d34 + effect tercile |
| R=50, top_k=all | 2 | d12_d34 + effect tercile |
| R=50, top_k=all | 3 | d12_d34 + effect tercile |
| R=50, top_k=all | 4 | d12_d34 + effect tercile |
| R=50, top_k=all | 5 | d12_d34 + effect tercile |
| R=50, top_k=all | 8 | all_three + no tercile |
| R=50, top_k=all | 10 | d12_d34 + no tercile |
| R=50, top_k=all | 15 | d12_d34 + no tercile |
| R=50, top_k=all | 19 | d12_d34 + no tercile |
| R=50, top_k=all | 20 | none fills |

## Baseline rungs: cross-fitted Brier skill vs uniform (descriptive)

Candidate pools at reference settings (agreement d12_d34; readout: R=20, cells condition x label x effect tercile; gene: ratio=2, tol=1.0, cells condition x label; neighbour: n_inf=1000, self>=q0.5, margin any, options excl. Phase 0, cells tier x condition), with an equal count in every cell (as in the batch; total up to probe2.baseline_train_max), forecasts out-of-fold with folds split by gene. Skill = 1 - Brier / Brier(uniform).

| cutoff | family | rung | questions | brier | brier_uniform | skill_vs_uniform |
|---|---|---|---|---|---|---|
| 2026-05-01 | readout | fame_only | 2538 | 0.667 | 0.6667 | -0.0005 |
| 2026-05-01 | readout | annotation_only | 2538 | 0.6639 | 0.6667 | 0.0041 |
| 2026-05-01 | gene | fame_only | 19998 | 0.5013 | 0.5 | -0.0025 |
| 2026-05-01 | gene | annotation_only | 19998 | 0.4967 | 0.5 | 0.0067 |
| 2026-05-01 | neighbour | fame_only | 900 | 0.7518 | 0.75 | -0.0024 |
| 2026-05-01 | neighbour | annotation_only | 900 | 0.7001 | 0.75 | 0.0666 |
| 2026-05-01 | readout | annotation_only_noIEA | 2538 | 0.6635 | 0.6667 | 0.0047 |
| 2026-05-01 | gene | annotation_only_noIEA | 19998 | 0.4961 | 0.5 | 0.0079 |
| 2026-05-01 | neighbour | annotation_only_noIEA | 900 | 0.7308 | 0.75 | 0.0256 |
| 2026-07-01 | readout | fame_only | 2538 | 0.667 | 0.6667 | -0.0005 |
| 2026-07-01 | readout | annotation_only | 2538 | 0.6632 | 0.6667 | 0.0052 |
| 2026-07-01 | gene | fame_only | 19998 | 0.5013 | 0.5 | -0.0025 |
| 2026-07-01 | gene | annotation_only | 19998 | 0.4961 | 0.5 | 0.0079 |
| 2026-07-01 | neighbour | fame_only | 900 | 0.7518 | 0.75 | -0.0024 |
| 2026-07-01 | neighbour | annotation_only | 900 | 0.7227 | 0.75 | 0.0364 |
| 2026-07-01 | readout | annotation_only_noIEA | 2538 | 0.6626 | 0.6667 | 0.0062 |
| 2026-07-01 | gene | annotation_only_noIEA | 19998 | 0.4958 | 0.5 | 0.0084 |
| 2026-07-01 | neighbour | annotation_only_noIEA | 900 | 0.7416 | 0.75 | 0.0112 |

## Model calls and wall time

Median seconds per call in Phase 0: {"sol-6.1-cli": 23.1, "opus-5.5-cli": 12.1}; workers per model: {"opus-5.5-cli": 2, "sol-6.1-cli": 4}. Calls = questions x versions x k (opus-5.5-cli) plus sol_fraction of the questions (sol-6.1-cli); versions = 2 (named, hidden) or 3 with the optional wrong-name control; the two models run concurrently.

| questions | k | sol_fraction | versions | opus_calls | sol_calls | total_calls | opus_hours | sol_hours | wall_hours |
|---|---|---|---|---|---|---|---|---|---|
| 600 | 1 | 0.5 | 2 | 1200 | 600 | 1800 | 2.0 | 1.0 | 2.0 |
| 600 | 1 | 0.5 | 3 | 1800 | 900 | 2700 | 3.0 | 1.4 | 3.0 |
| 600 | 1 | 1.0 | 2 | 1200 | 1200 | 2400 | 2.0 | 1.9 | 2.0 |
| 600 | 1 | 1.0 | 3 | 1800 | 1800 | 3600 | 3.0 | 2.9 | 3.0 |
| 600 | 2 | 0.5 | 2 | 2400 | 1200 | 3600 | 4.0 | 1.9 | 4.0 |
| 600 | 2 | 0.5 | 3 | 3600 | 1800 | 5400 | 6.0 | 2.9 | 6.0 |
| 600 | 2 | 1.0 | 2 | 2400 | 2400 | 4800 | 4.0 | 3.8 | 4.0 |
| 600 | 2 | 1.0 | 3 | 3600 | 3600 | 7200 | 6.0 | 5.8 | 6.0 |
| 600 | 3 | 0.5 | 2 | 3600 | 1800 | 5400 | 6.0 | 2.9 | 6.0 |
| 600 | 3 | 0.5 | 3 | 5400 | 2700 | 8100 | 9.0 | 4.3 | 9.0 |
| 600 | 3 | 1.0 | 2 | 3600 | 3600 | 7200 | 6.0 | 5.8 | 6.0 |
| 600 | 3 | 1.0 | 3 | 5400 | 5400 | 10800 | 9.0 | 8.7 | 9.0 |
| 1290 | 1 | 0.5 | 2 | 2580 | 1290 | 3870 | 4.3 | 2.1 | 4.3 |
| 1290 | 1 | 0.5 | 3 | 3870 | 1935 | 5805 | 6.5 | 3.1 | 6.5 |
| 1290 | 1 | 1.0 | 2 | 2580 | 2580 | 5160 | 4.3 | 4.1 | 4.3 |
| 1290 | 1 | 1.0 | 3 | 3870 | 3870 | 7740 | 6.5 | 6.2 | 6.5 |
| 1290 | 2 | 0.5 | 2 | 5160 | 2580 | 7740 | 8.6 | 4.1 | 8.6 |
| 1290 | 2 | 0.5 | 3 | 7740 | 3870 | 11610 | 13.0 | 6.2 | 13.0 |
| 1290 | 2 | 1.0 | 2 | 5160 | 5160 | 10320 | 8.6 | 8.3 | 8.6 |
| 1290 | 2 | 1.0 | 3 | 7740 | 7740 | 15480 | 13.0 | 12.4 | 13.0 |
| 1290 | 3 | 0.5 | 2 | 7740 | 3870 | 11610 | 13.0 | 6.2 | 13.0 |
| 1290 | 3 | 0.5 | 3 | 11610 | 5805 | 17415 | 19.4 | 9.3 | 19.4 |
| 1290 | 3 | 1.0 | 2 | 7740 | 7740 | 15480 | 13.0 | 12.4 | 13.0 |
| 1290 | 3 | 1.0 | 3 | 11610 | 11610 | 23220 | 19.4 | 18.6 | 19.4 |

## Pre-registered configuration: selection as generation would make it

Questions per family and stratum (opus-5.5-cli runs all; sol-6.1-cli the sol subset):

| family | stratum | opus | sol |
|---|---|---|---|
| gene | flagged | 120 | 68 |
| gene | main | 300 | 150 |
| neighbour | flagged | 30 | 18 |
| neighbour | main | 135 | 75 |
| readout | flagged | 180 | 101 |
| readout | main | 675 | 405 |

Agreement filter per family: {"readout": "d12_d34", "gene": "all_three", "neighbour": "all_three"}.
F-neighbour thresholds per condition: {"neighbour": {"min_self_corr": {"Rest": 0.21299463510513306, "Stim8hr": 0.24391533434391022, "Stim48hr": 0.2623332738876343}, "margin": {"Rest": 0.5830048620700836, "Stim8hr": 0.5130419135093689, "Stim48hr": 0.505396381020546}}}.
Dropped cells: {"readout/main": [], "readout/flagged": [], "gene/main": [], "gene/flagged": [], "neighbour/main": [], "neighbour/flagged": []}.

| model | questions | versions | k | calls | hours |
|---|---|---|---|---|---|
| opus-5.5-cli | 1440 | 2 | 2 | 5760 | 9.6 |
| sol-6.1-cli | 817 | 2 | 2 | 3268 | 5.2 |
