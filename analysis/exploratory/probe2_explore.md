# Probe v2 exploratory aggregates: batch p2-20261023-232739-c559

**Exploratory, not pre-registered.** Written after the final report and D-025; nothing here changes the checks or the branch. Aggregates only; produced by `analysis/exploratory/probe2_explore.py`.

## a. Bin-0 flagged cells

Questions: 21 ({'gene': 7, 'neighbour': 4, 'readout': 10}); distinct genes: 11 (flagged by the paper: 4). Reference: 40 random genes from main-stratum bin-0 questions. Identities are in data_root only.

| set | n | NCBI type protein-coding | symbol changed (HGNC) | has alias/prev symbol | median gene2pubmed papers | median PubMed [tiab] symbol hits | median hits/papers (symbol) | median hits/papers (symbol or alias) |
|---|---|---|---|---|---|---|---|---|
| bin0_flagged | 11 | 11 | 8 | 11 | 4.0 | 9 | 1.5 | 2.4 |
| bin0_main_reference | 40 | 40 | 20 | 37 | 4.0 | 8 | 2.1 | 4.0 |

PubMed counts are title/abstract hits before 2026-05-01 (Sol's cutoff); symbol searches over-count short or word-like symbols, and alias searches over-count more, so compare the two sets rather than reading the ratios as rates.

Positive-control gain (flagged stratum, F-readout and F-gene, mean of the two family means, mean_brier), with and without bin 0:

- opus-5.5-cli: all bins 0.206 [0.134, 0.272] (n=300); bin 0 excluded 0.192 [0.120, 0.263] (n=283)
- sol-6.1-cli: all bins 0.195 [0.084, 0.297] (n=169); bin 0 excluded 0.177 [0.063, 0.281] (n=158)

## b. Name-similarity rung for F-neighbour

Conditional logit over the four options on (shared symbol prefix length, same alphabetic symbol root, shared HGNC gene group), fitted on the 630 outside-batch neighbour training items like the other rungs; coefficients [-0.069, 1.463, 0.417]. HGNC groups are from the current HGNC file, not a release dated before each cutoff.

Feature means, correct option vs mean of distractors (all batch neighbour items): prefix 0.176 vs 0.131; same root 0.012 vs 0.016; same group 0.067 vs 0.022

| model | stratum | bin | n | rung Brier skill vs uniform | model named Brier skill | model gain (named vs hidden) | model named gain beyond rung |
|---|---|---|---|---|---|---|---|
| opus-5.5-cli | flagged | all | 30 | 0.019 | 0.160 | 0.199 | 0.141 [0.000, 0.282] |
| opus-5.5-cli | flagged | 0 | 4 | 0.000 | 0.711 | 0.541 | 0.711 [0.635, 0.765] |
| opus-5.5-cli | flagged | 1 | 1 | 0.000 | 0.553 | 0.588 | 0.553 [0.553, 0.553] |
| opus-5.5-cli | flagged | 2 | 2 | 0.000 | 0.295 | 0.144 | 0.295 [-0.036, 0.627] |
| opus-5.5-cli | flagged | 3 | 5 | 0.004 | 0.034 | 0.128 | 0.029 [-0.296, 0.438] |
| opus-5.5-cli | flagged | 4 | 18 | 0.030 | 0.036 | 0.127 | 0.006 [-0.103, 0.114] |
| opus-5.5-cli | main | all | 135 | -0.003 | 0.142 | 0.137 | 0.145 [0.074, 0.209] |
| opus-5.5-cli | main | 0 | 27 | -0.022 | 0.227 | 0.262 | 0.249 [0.061, 0.462] |
| opus-5.5-cli | main | 1 | 27 | 0.005 | 0.229 | 0.214 | 0.224 [0.074, 0.389] |
| opus-5.5-cli | main | 2 | 27 | -0.004 | 0.119 | 0.051 | 0.124 [-0.004, 0.265] |
| opus-5.5-cli | main | 3 | 27 | 0.001 | 0.040 | 0.068 | 0.038 [-0.113, 0.179] |
| opus-5.5-cli | main | 4 | 27 | 0.004 | 0.094 | 0.091 | 0.090 [-0.044, 0.248] |
| sol-6.1-cli | flagged | all | 18 | -0.013 | 0.168 | 0.183 | 0.180 [-0.098, 0.462] |
| sol-6.1-cli | flagged | 0 | 2 | 0.000 | 0.788 | 0.788 | 0.788 [0.788, 0.788] |
| sol-6.1-cli | flagged | 1 | 1 | 0.000 | 0.719 | 0.719 | 0.719 [0.719, 0.719] |
| sol-6.1-cli | flagged | 2 | 2 | 0.000 | 0.430 | 0.430 | 0.430 [0.091, 0.769] |
| sol-6.1-cli | flagged | 3 | 3 | 0.004 | -0.279 | -0.279 | -0.282 [-0.570, 0.281] |
| sol-6.1-cli | flagged | 4 | 10 | -0.024 | 0.070 | 0.097 | 0.094 [-0.287, 0.445] |
| sol-6.1-cli | main | all | 75 | 0.004 | 0.001 | 0.001 | -0.003 [-0.124, 0.118] |
| sol-6.1-cli | main | 0 | 15 | -0.009 | 0.050 | 0.050 | 0.059 [-0.222, 0.322] |
| sol-6.1-cli | main | 1 | 15 | 0.027 | 0.227 | 0.227 | 0.200 [-0.101, 0.517] |
| sol-6.1-cli | main | 2 | 15 | -0.002 | 0.003 | 0.003 | 0.006 [-0.196, 0.249] |
| sol-6.1-cli | main | 3 | 15 | -0.003 | -0.054 | -0.054 | -0.051 [-0.308, 0.242] |
| sol-6.1-cli | main | 4 | 15 | 0.006 | -0.223 | -0.223 | -0.229 [-0.429, 0.024] |

## c. Essentiality rung for F-gene

Multinomial logistic on the pair differences in DepMap 24Q4 mean Chronos gene effect (mean over screened lines) and Replogle 2022 K562 genome-wide knockdown strength (−pct_expr, the fractional drop in target expression; mean over guides), each with a missing indicator, fitted on the 1374 outside-batch F-gene training pairs like the other rungs. Both genes covered: DepMap 98%, Replogle 85% of batch pairs.

| model | stratum | ratio band | n | rung Brier skill vs uniform | model named Brier skill | model named gain beyond rung |
|---|---|---|---|---|---|---|
| opus-5.5-cli | flagged | all | 120 | 0.084 | 0.325 | 0.241 [0.091, 0.393] |
| opus-5.5-cli | flagged | 2-4 | 18 | 0.173 | 0.309 | 0.136 [-0.169, 0.483] |
| opus-5.5-cli | flagged | 4-10 | 26 | 0.056 | 0.129 | 0.073 [-0.223, 0.335] |
| opus-5.5-cli | flagged | >10 | 76 | 0.073 | 0.396 | 0.323 [0.152, 0.509] |
| opus-5.5-cli | main | all | 300 | 0.074 | 0.173 | 0.099 [0.021, 0.172] |
| opus-5.5-cli | main | 2-4 | 59 | 0.140 | 0.240 | 0.101 [-0.063, 0.245] |
| opus-5.5-cli | main | 4-10 | 113 | 0.045 | 0.160 | 0.115 [0.000, 0.226] |
| opus-5.5-cli | main | >10 | 128 | 0.070 | 0.153 | 0.083 [-0.025, 0.198] |
| sol-6.1-cli | flagged | all | 68 | 0.048 | 0.353 | 0.305 [0.068, 0.524] |
| sol-6.1-cli | flagged | 2-4 | 11 | 0.121 | -0.063 | -0.184 [-0.911, 0.536] |
| sol-6.1-cli | flagged | 4-10 | 11 | 0.070 | 0.001 | -0.069 [-0.818, 0.577] |
| sol-6.1-cli | flagged | >10 | 46 | 0.025 | 0.537 | 0.512 [0.261, 0.718] |
| sol-6.1-cli | main | all | 150 | 0.116 | 0.099 | -0.016 [-0.162, 0.134] |
| sol-6.1-cli | main | 2-4 | 33 | 0.100 | 0.278 | 0.178 [-0.082, 0.426] |
| sol-6.1-cli | main | 4-10 | 53 | 0.154 | 0.101 | -0.053 [-0.283, 0.173] |
| sol-6.1-cli | main | >10 | 64 | 0.092 | 0.006 | -0.086 [-0.316, 0.147] |

## d. Discrimination vs calibration on shared questions

817 questions answered by both models (all strata). Murphy terms over 10 forecast bins, summed one-vs-rest (resolution: higher is better discrimination; reliability: lower is better calibration). AUC: F-readout P(changed); F-gene P(A) for A; F-neighbour correct option vs distractors, pooled.

| family | version | model | resolution | reliability | ECE | AUC | Brier skill vs uniform |
|---|---|---|---|---|---|---|---|
| readout | named | opus-5.5-cli | 0.076 | 0.026 | 0.028 | 0.645 | 0.085 |
| readout | named | sol-6.1-cli | 0.061 | 0.017 | 0.073 | 0.584 | 0.068 |
| readout | hidden | opus-5.5-cli | 0.010 | 0.013 | 0.051 | 0.430 | -0.005 |
| readout | hidden | sol-6.1-cli | 0.003 | 0.003 | 0.002 | 0.480 | -0.001 |
| gene | named | opus-5.5-cli | 0.151 | 0.024 | 0.096 | 0.819 | 0.270 |
| gene | named | sol-6.1-cli | 0.121 | 0.026 | 0.079 | 0.748 | 0.189 |
| gene | hidden | opus-5.5-cli | 0.000 | 0.000 | 0.000 | 0.500 | 0.000 |
| gene | hidden | sol-6.1-cli | 0.000 | 0.000 | 0.000 | 0.500 | 0.000 |
| neighbour | named | opus-5.5-cli | 0.132 | 0.049 | 0.164 | 0.637 | 0.104 |
| neighbour | named | sol-6.1-cli | 0.114 | 0.097 | 0.177 | 0.653 | 0.038 |
| neighbour | hidden | opus-5.5-cli | 0.056 | 0.071 | 0.072 | 0.540 | -0.009 |
| neighbour | hidden | sol-6.1-cli | 0.009 | 0.015 | 0.015 | 0.493 | -0.002 |

Named version, Opus − Sol, gene-clustered bootstrap on shared questions:

- readout: resolution 0.015 [-0.007, 0.034]; reliability 0.009 [-0.007, 0.021]; AUC 0.061 [0.016, 0.112]
- gene: resolution 0.031 [-0.019, 0.066]; reliability -0.002 [-0.044, 0.025]; AUC 0.071 [0.029, 0.115]
- neighbour: resolution 0.018 [-0.049, 0.046]; reliability -0.048 [-0.124, -0.013]; AUC -0.016 [-0.064, 0.022]
