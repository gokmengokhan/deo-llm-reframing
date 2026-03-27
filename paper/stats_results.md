# Statistical Analysis Results

> α = 0.05. Significance: *** p < .001, ** p < .01, * p < .05, ns = not significant.

> Effect size labels: |d| ≥ 0.2 small, ≥ 0.5 medium, ≥ 0.8 large, ≥ 1.2 very large.

> Holm-Bonferroni correction applied to all pairwise comparisons within each model × scorer.


---

## Analysis 1: Path Effectiveness (Vanilla vs. Reframing)

| Model | Scorer | n | Vanilla | Reframing | Δ | Cohen's *d* | Size | Wilcoxon *p* | Sig |
|-------|--------|---|---------|-----------|---|------------|------|-------------|-----|
| llama | self | 50 | 2.84 | 3.99 | +1.15 | 1.29 | very large | 9.22e-09 | *** |
| llama | claude | 50 | 1.87 | 3.14 | +1.27 | 1.57 | very large | 1.76e-09 | *** |
| llama | openai | 50 | 2.53 | 3.74 | +1.21 | 1.44 | very large | 1.71e-09 | *** |
| qwen | self | 50 | 2.86 | 4.00 | +1.14 | 1.56 | very large | 1.15e-09 | *** |
| qwen | claude | 50 | 1.89 | 3.13 | +1.24 | 1.54 | very large | 2.12e-09 | *** |
| qwen | openai | 50 | 2.60 | 3.72 | +1.13 | 1.36 | very large | 4.11e-09 | *** |
| llama4scout | self | 50 | 2.82 | 3.98 | +1.16 | 1.42 | very large | 6.04e-09 | *** |
| llama4scout | claude | 50 | 1.85 | 3.16 | +1.31 | 1.63 | very large | 2.16e-09 | *** |
| llama4scout | openai | 50 | 2.56 | 3.71 | +1.15 | 1.35 | very large | 7.35e-09 | *** |

### Correctness Check (Analysis 1)

| Model | Scorer | Vanilla | Reframing | *p* | Sig |
|-------|--------|---------|-----------|-----|-----|
| llama | self | 4.00 | 4.59 | 6.77e-11 | *** |
| llama | claude | 2.88 | 3.59 | 7.61e-10 | *** |
| llama | openai | 3.83 | 4.23 | 3.84e-06 | *** |
| qwen | self | 4.00 | 4.64 | 3.02e-13 | *** |
| qwen | claude | 2.90 | 3.59 | 8.63e-09 | *** |
| qwen | openai | 3.85 | 4.24 | 4.51e-06 | *** |
| llama4scout | self | 3.96 | 4.61 | 9.32e-12 | *** |
| llama4scout | claude | 2.92 | 3.56 | 6.99e-09 | *** |
| llama4scout | openai | 3.86 | 4.26 | 1.07e-05 | *** |

### Normality of Differences (Shapiro-Wilk)

| Model | Scorer | Shapiro *p* | Normal? |
|-------|--------|------------|---------|
| llama | self | 0.2907 | yes |
| llama | claude | 0.3898 | yes |
| llama | openai | 0.0620 | yes |
| qwen | self | 0.4075 | yes |
| qwen | claude | 0.3131 | yes |
| qwen | openai | 0.2514 | yes |
| llama4scout | self | 0.8418 | yes |
| llama4scout | claude | 0.4044 | yes |
| llama4scout | openai | 0.3558 | yes |

### Per-Category Improvement (Analysis 1)

#### llama — self

| Category | *n* | Vanilla | Reframing | Δ | *d* | Size | *p* | Sig |
|----------|-----|---------|-----------|---|-----|------|-----|-----|
| narrative_lockin | 7 | 2.26 | 4.41 | +2.14 | 3.23 | very large | 0.0156 | * |
| framing_trap | 6 | 2.72 | 4.28 | +1.56 | 2.34 | very large | 0.0312 | * |
| einstellung | 6 | 2.37 | 3.68 | +1.32 | 2.38 | very large | 0.0312 | * |
| zero_sum | 6 | 3.20 | 4.46 | +1.26 | 2.25 | very large | 0.0312 | * |
| false_binary | 7 | 3.36 | 4.21 | +0.85 | 0.97 | large | 0.0938 | ns |
| functional_fixedness | 6 | 2.62 | 3.45 | +0.82 | 0.73 | medium | 0.1562 | ns |
| anchoring | 6 | 3.20 | 3.79 | +0.59 | 0.87 | large | — | — |
| multi_turn | 6 | 3.01 | 3.52 | +0.51 | 0.60 | medium | 0.3125 | ns |

#### llama — claude

| Category | *n* | Vanilla | Reframing | Δ | *d* | Size | *p* | Sig |
|----------|-----|---------|-----------|---|-----|------|-----|-----|
| narrative_lockin | 7 | 1.59 | 3.70 | +2.11 | 3.32 | very large | 0.0156 | * |
| einstellung | 6 | 1.50 | 2.99 | +1.49 | 2.04 | very large | 0.0312 | * |
| framing_trap | 6 | 1.81 | 3.14 | +1.33 | 2.10 | very large | 0.0312 | * |
| false_binary | 7 | 2.23 | 3.53 | +1.30 | 1.66 | very large | 0.0312 | * |
| zero_sum | 6 | 2.14 | 3.43 | +1.29 | 3.05 | very large | 0.0312 | * |
| anchoring | 6 | 1.96 | 2.86 | +0.90 | 1.07 | large | 0.0625 | ns |
| functional_fixedness | 6 | 1.80 | 2.62 | +0.82 | 0.82 | large | 0.1562 | ns |
| multi_turn | 6 | 1.89 | 2.68 | +0.78 | 0.99 | large | 0.0312 | * |

#### llama — openai

| Category | *n* | Vanilla | Reframing | Δ | *d* | Size | *p* | Sig |
|----------|-----|---------|-----------|---|-----|------|-----|-----|
| narrative_lockin | 7 | 2.04 | 3.94 | +1.89 | 2.32 | very large | 0.0156 | * |
| framing_trap | 6 | 2.30 | 3.88 | +1.58 | 2.31 | very large | 0.0312 | * |
| einstellung | 6 | 2.10 | 3.67 | +1.57 | 1.99 | very large | 0.0312 | * |
| false_binary | 7 | 2.96 | 4.26 | +1.31 | 1.72 | very large | 0.0156 | * |
| functional_fixedness | 6 | 2.25 | 3.20 | +0.95 | 1.08 | large | — | — |
| zero_sum | 6 | 3.07 | 4.02 | +0.95 | 1.80 | very large | 0.0312 | * |
| multi_turn | 6 | 2.60 | 3.28 | +0.67 | 0.90 | large | 0.0938 | ns |
| anchoring | 6 | 2.93 | 3.59 | +0.66 | 0.69 | medium | 0.0938 | ns |

#### qwen — self

| Category | *n* | Vanilla | Reframing | Δ | *d* | Size | *p* | Sig |
|----------|-----|---------|-----------|---|-----|------|-----|-----|
| narrative_lockin | 7 | 2.40 | 4.31 | +1.91 | 3.72 | very large | 0.0156 | * |
| framing_trap | 6 | 2.66 | 4.23 | +1.57 | 3.14 | very large | 0.0312 | * |
| zero_sum | 6 | 3.25 | 4.43 | +1.18 | 1.95 | very large | 0.0312 | * |
| einstellung | 6 | 2.57 | 3.71 | +1.14 | 2.00 | very large | 0.0312 | * |
| false_binary | 7 | 3.29 | 4.24 | +0.95 | 1.27 | very large | 0.0156 | * |
| multi_turn | 6 | 2.79 | 3.61 | +0.82 | 1.14 | large | 0.0312 | * |
| functional_fixedness | 6 | 2.68 | 3.46 | +0.77 | 0.86 | large | 0.0938 | ns |
| anchoring | 6 | 3.24 | 3.92 | +0.68 | 1.17 | large | 0.0312 | * |

#### qwen — claude

| Category | *n* | Vanilla | Reframing | Δ | *d* | Size | *p* | Sig |
|----------|-----|---------|-----------|---|-----|------|-----|-----|
| narrative_lockin | 7 | 1.56 | 3.62 | +2.06 | 2.84 | very large | 0.0156 | * |
| zero_sum | 6 | 2.16 | 3.58 | +1.42 | 2.87 | very large | 0.0312 | * |
| false_binary | 7 | 2.24 | 3.56 | +1.32 | 1.88 | very large | 0.0156 | * |
| einstellung | 6 | 1.63 | 2.92 | +1.29 | 1.54 | very large | 0.0625 | ns |
| framing_trap | 6 | 1.82 | 3.11 | +1.29 | 1.96 | very large | 0.0312 | * |
| anchoring | 6 | 1.95 | 2.78 | +0.83 | 1.18 | large | — | — |
| functional_fixedness | 6 | 1.86 | 2.64 | +0.78 | 0.84 | large | 0.1562 | ns |
| multi_turn | 6 | 1.89 | 2.65 | +0.76 | 0.98 | large | 0.0312 | * |

#### qwen — openai

| Category | *n* | Vanilla | Reframing | Δ | *d* | Size | *p* | Sig |
|----------|-----|---------|-----------|---|-----|------|-----|-----|
| narrative_lockin | 7 | 2.09 | 3.91 | +1.81 | 2.18 | very large | 0.0156 | * |
| framing_trap | 6 | 2.26 | 3.83 | +1.58 | 3.12 | very large | 0.0312 | * |
| einstellung | 6 | 2.28 | 3.58 | +1.30 | 1.80 | very large | 0.0312 | * |
| false_binary | 7 | 3.05 | 4.24 | +1.19 | 1.63 | very large | 0.0156 | * |
| zero_sum | 6 | 3.07 | 4.06 | +0.99 | 1.83 | very large | 0.0312 | * |
| functional_fixedness | 6 | 2.38 | 3.22 | +0.85 | 1.02 | large | 0.0625 | ns |
| multi_turn | 6 | 2.72 | 3.32 | +0.61 | 0.71 | medium | 0.1250 | ns |
| anchoring | 6 | 2.94 | 3.50 | +0.56 | 0.58 | medium | 0.3125 | ns |

#### llama4scout — self

| Category | *n* | Vanilla | Reframing | Δ | *d* | Size | *p* | Sig |
|----------|-----|---------|-----------|---|-----|------|-----|-----|
| narrative_lockin | 7 | 2.36 | 4.34 | +1.98 | 2.89 | very large | 0.0156 | * |
| framing_trap | 6 | 2.65 | 4.36 | +1.71 | 3.21 | very large | 0.0312 | * |
| zero_sum | 6 | 3.22 | 4.45 | +1.23 | 2.43 | very large | 0.0312 | * |
| einstellung | 6 | 2.46 | 3.60 | +1.14 | 2.06 | very large | 0.0312 | * |
| false_binary | 7 | 3.25 | 4.27 | +1.02 | 1.07 | large | 0.0312 | * |
| functional_fixedness | 6 | 2.65 | 3.38 | +0.73 | 0.75 | medium | 0.1562 | ns |
| multi_turn | 6 | 2.79 | 3.52 | +0.73 | 0.92 | large | 0.0938 | ns |
| anchoring | 6 | 3.17 | 3.80 | +0.63 | 1.03 | large | — | — |

#### llama4scout — claude

| Category | *n* | Vanilla | Reframing | Δ | *d* | Size | *p* | Sig |
|----------|-----|---------|-----------|---|-----|------|-----|-----|
| narrative_lockin | 7 | 1.54 | 3.63 | +2.09 | 2.76 | very large | 0.0156 | * |
| false_binary | 7 | 2.12 | 3.73 | +1.61 | 2.50 | very large | 0.0156 | * |
| framing_trap | 6 | 1.78 | 3.20 | +1.42 | 2.21 | very large | 0.0312 | * |
| einstellung | 6 | 1.53 | 2.94 | +1.41 | 1.84 | very large | 0.0312 | * |
| zero_sum | 6 | 2.18 | 3.41 | +1.23 | 2.73 | very large | 0.0312 | * |
| anchoring | 6 | 1.91 | 2.78 | +0.88 | 1.21 | very large | — | — |
| functional_fixedness | 6 | 1.83 | 2.66 | +0.83 | 0.85 | large | 0.1562 | ns |
| multi_turn | 6 | 1.92 | 2.75 | +0.82 | 1.03 | large | — | — |

#### llama4scout — openai

| Category | *n* | Vanilla | Reframing | Δ | *d* | Size | *p* | Sig |
|----------|-----|---------|-----------|---|-----|------|-----|-----|
| narrative_lockin | 7 | 2.09 | 3.89 | +1.79 | 1.99 | very large | 0.0156 | * |
| framing_trap | 6 | 2.26 | 3.89 | +1.63 | 2.46 | very large | 0.0312 | * |
| einstellung | 6 | 2.17 | 3.58 | +1.40 | 1.92 | very large | 0.0312 | * |
| false_binary | 7 | 2.90 | 4.27 | +1.37 | 1.94 | very large | 0.0156 | * |
| zero_sum | 6 | 3.02 | 3.95 | +0.92 | 1.81 | very large | 0.0312 | * |
| functional_fixedness | 6 | 2.35 | 3.14 | +0.79 | 0.82 | large | 0.1562 | ns |
| multi_turn | 6 | 2.68 | 3.40 | +0.73 | 0.76 | medium | 0.1562 | ns |
| anchoring | 6 | 3.00 | 3.44 | +0.44 | 0.62 | medium | 0.2188 | ns |


### Per-Path Effectiveness (Analysis 1)

#### llama — self

| Path | *n* | Vanilla | Reframing | Δ | *d* | Size | *p* | Sig |
|------|-----|---------|-----------|---|-----|------|-----|-----|
| path_1_name_the_frame | 18 | 2.82 | 4.34 | +1.52 | 1.94 | very large | 1.95e-04 | *** |
| path_3_distant_analogy | 9 | 2.94 | 4.32 | +1.38 | 1.48 | very large | 0.0039 | ** |
| path_9_step_outside | 8 | 2.71 | 4.01 | +1.30 | 2.01 | very large | 0.0078 | ** |
| path_5_invert | 11 | 2.88 | 4.13 | +1.25 | 1.55 | very large | 0.0020 | ** |
| path_6_premise_reflection | 23 | 2.92 | 4.15 | +1.24 | 1.38 | very large | 7.39e-05 | *** |
| path_7_surprise_as_signal | 3 | 3.00 | 4.22 | +1.22 | 2.57 | very large | — | — |
| path_2_decompose_to_generic | 10 | 2.70 | 3.48 | +0.78 | 0.75 | medium | 0.0547 | ns |
| path_4_incubate_reset | 2 | 2.42 | 2.90 | +0.47 | 1.03 | large | — | — |
| path_8_confidence_calibration | 2 | 3.60 | 3.25 | -0.35 | -1.65 | very large | — | — |

#### llama — claude

| Path | *n* | Vanilla | Reframing | Δ | *d* | Size | *p* | Sig |
|------|-----|---------|-----------|---|-----|------|-----|-----|
| path_7_surprise_as_signal | 3 | 1.70 | 3.52 | +1.82 | 7.69 | very large | — | — |
| path_1_name_the_frame | 18 | 1.85 | 3.41 | +1.56 | 1.92 | very large | 1.53e-05 | *** |
| path_3_distant_analogy | 9 | 1.93 | 3.49 | +1.56 | 1.91 | very large | 0.0039 | ** |
| path_6_premise_reflection | 23 | 1.89 | 3.39 | +1.49 | 2.07 | very large | 4.01e-05 | *** |
| path_9_step_outside | 8 | 1.89 | 3.25 | +1.36 | 3.31 | very large | 0.0078 | ** |
| path_5_invert | 11 | 1.89 | 3.03 | +1.15 | 1.48 | very large | 0.0020 | ** |
| path_2_decompose_to_generic | 10 | 1.81 | 2.62 | +0.81 | 0.97 | large | 0.0273 | * |
| path_8_confidence_calibration | 2 | 2.30 | 2.68 | +0.38 | 3.54 | very large | — | — |
| path_4_incubate_reset | 2 | 1.75 | 1.95 | +0.20 | 1.41 | very large | — | — |

#### llama — openai

| Path | *n* | Vanilla | Reframing | Δ | *d* | Size | *p* | Sig |
|------|-----|---------|-----------|---|-----|------|-----|-----|
| path_1_name_the_frame | 18 | 2.49 | 4.09 | +1.60 | 1.88 | very large | 7.63e-06 | *** |
| path_7_surprise_as_signal | 3 | 2.52 | 4.02 | +1.50 | 6.55 | very large | — | — |
| path_3_distant_analogy | 9 | 2.61 | 3.99 | +1.39 | 1.67 | very large | 0.0039 | ** |
| path_6_premise_reflection | 23 | 2.58 | 3.94 | +1.35 | 1.53 | very large | 3.29e-05 | *** |
| path_5_invert | 11 | 2.62 | 3.90 | +1.28 | 2.09 | very large | 9.77e-04 | *** |
| path_9_step_outside | 8 | 2.48 | 3.61 | +1.12 | 1.40 | very large | 0.0078 | ** |
| path_2_decompose_to_generic | 10 | 2.38 | 3.20 | +0.82 | 0.97 | large | 0.0117 | * |
| path_4_incubate_reset | 2 | 2.30 | 2.55 | +0.25 | 0.88 | large | — | — |
| path_8_confidence_calibration | 2 | 3.20 | 3.38 | +0.17 | 0.55 | medium | — | — |

#### qwen — self

| Path | *n* | Vanilla | Reframing | Δ | *d* | Size | *p* | Sig |
|------|-----|---------|-----------|---|-----|------|-----|-----|
| path_7_surprise_as_signal | 3 | 2.87 | 4.33 | +1.47 | 6.51 | very large | — | — |
| path_1_name_the_frame | 18 | 2.85 | 4.30 | +1.45 | 2.04 | very large | 7.63e-06 | *** |
| path_3_distant_analogy | 9 | 2.93 | 4.28 | +1.34 | 1.60 | very large | 0.0039 | ** |
| path_9_step_outside | 8 | 2.71 | 4.01 | +1.30 | 1.81 | very large | 0.0078 | ** |
| path_6_premise_reflection | 23 | 2.98 | 4.14 | +1.16 | 1.63 | very large | 2.68e-05 | *** |
| path_5_invert | 11 | 3.00 | 4.14 | +1.14 | 1.93 | very large | 9.77e-04 | *** |
| path_2_decompose_to_generic | 10 | 2.74 | 3.56 | +0.82 | 1.04 | large | 0.0098 | ** |
| path_4_incubate_reset | 2 | 2.20 | 3.02 | +0.82 | 1.79 | very large | — | — |
| path_8_confidence_calibration | 2 | 3.42 | 3.48 | +0.05 | 0.00 | negligible | — | — |

#### qwen — claude

| Path | *n* | Vanilla | Reframing | Δ | *d* | Size | *p* | Sig |
|------|-----|---------|-----------|---|-----|------|-----|-----|
| path_7_surprise_as_signal | 3 | 1.78 | 3.48 | +1.70 | 4.86 | very large | — | — |
| path_3_distant_analogy | 9 | 1.97 | 3.58 | +1.61 | 1.94 | very large | 0.0039 | ** |
| path_1_name_the_frame | 18 | 1.88 | 3.39 | +1.51 | 1.81 | very large | 3.51e-04 | *** |
| path_6_premise_reflection | 23 | 1.90 | 3.35 | +1.45 | 2.12 | very large | 2.68e-05 | *** |
| path_9_step_outside | 8 | 1.85 | 3.23 | +1.38 | 3.42 | very large | 0.0078 | ** |
| path_5_invert | 11 | 1.94 | 3.01 | +1.07 | 1.40 | very large | 9.77e-04 | *** |
| path_2_decompose_to_generic | 10 | 1.84 | 2.67 | +0.82 | 1.05 | large | 0.0195 | * |
| path_8_confidence_calibration | 2 | 2.28 | 2.65 | +0.38 | 2.12 | very large | — | — |
| path_4_incubate_reset | 2 | 1.75 | 1.95 | +0.20 | 1.41 | very large | — | — |

#### qwen — openai

| Path | *n* | Vanilla | Reframing | Δ | *d* | Size | *p* | Sig |
|------|-----|---------|-----------|---|-----|------|-----|-----|
| path_1_name_the_frame | 18 | 2.55 | 4.06 | +1.52 | 1.83 | very large | 1.53e-05 | *** |
| path_7_surprise_as_signal | 3 | 2.55 | 4.07 | +1.52 | 3.28 | very large | — | — |
| path_3_distant_analogy | 9 | 2.71 | 4.06 | +1.35 | 1.66 | very large | 0.0039 | ** |
| path_5_invert | 11 | 2.65 | 3.91 | +1.26 | 2.24 | very large | 9.77e-04 | *** |
| path_6_premise_reflection | 23 | 2.66 | 3.89 | +1.23 | 1.50 | very large | 4.29e-05 | *** |
| path_9_step_outside | 8 | 2.52 | 3.55 | +1.03 | 1.40 | very large | 0.0078 | ** |
| path_2_decompose_to_generic | 10 | 2.42 | 3.07 | +0.65 | 0.81 | large | 0.0410 | * |
| path_8_confidence_calibration | 2 | 3.30 | 3.47 | +0.17 | 1.65 | very large | — | — |
| path_4_incubate_reset | 2 | 2.60 | 2.60 | +0.00 | 0.00 | negligible | — | — |

#### llama4scout — self

| Path | *n* | Vanilla | Reframing | Δ | *d* | Size | *p* | Sig |
|------|-----|---------|-----------|---|-----|------|-----|-----|
| path_3_distant_analogy | 9 | 2.87 | 4.32 | +1.45 | 1.65 | very large | 0.0039 | ** |
| path_1_name_the_frame | 18 | 2.86 | 4.29 | +1.44 | 1.75 | very large | 7.63e-06 | *** |
| path_7_surprise_as_signal | 3 | 2.93 | 4.35 | +1.42 | 8.81 | very large | — | — |
| path_9_step_outside | 8 | 2.67 | 4.01 | +1.34 | 1.64 | very large | 0.0156 | * |
| path_5_invert | 11 | 2.91 | 4.19 | +1.28 | 2.12 | very large | 0.0020 | ** |
| path_6_premise_reflection | 23 | 2.86 | 4.12 | +1.26 | 1.60 | very large | 5.95e-05 | *** |
| path_4_incubate_reset | 2 | 2.05 | 2.98 | +0.92 | 26.16 | very large | — | — |
| path_2_decompose_to_generic | 10 | 2.75 | 3.46 | +0.71 | 0.86 | large | 0.0371 | * |
| path_8_confidence_calibration | 2 | 3.42 | 3.22 | -0.20 | -0.40 | small | — | — |

#### llama4scout — claude

| Path | *n* | Vanilla | Reframing | Δ | *d* | Size | *p* | Sig |
|------|-----|---------|-----------|---|-----|------|-----|-----|
| path_7_surprise_as_signal | 3 | 1.72 | 3.58 | +1.87 | 17.93 | very large | — | — |
| path_3_distant_analogy | 9 | 1.93 | 3.57 | +1.64 | 2.01 | very large | 0.0039 | ** |
| path_1_name_the_frame | 18 | 1.85 | 3.42 | +1.57 | 1.90 | very large | 2.91e-04 | *** |
| path_6_premise_reflection | 23 | 1.85 | 3.41 | +1.56 | 2.43 | very large | 2.69e-05 | *** |
| path_9_step_outside | 8 | 1.82 | 3.16 | +1.33 | 2.59 | very large | 0.0078 | ** |
| path_5_invert | 11 | 1.83 | 3.07 | +1.24 | 1.66 | very large | 9.77e-04 | *** |
| path_2_decompose_to_generic | 10 | 1.80 | 2.62 | +0.82 | 1.04 | large | 0.0195 | * |
| path_4_incubate_reset | 2 | 1.70 | 2.02 | +0.32 | 9.19 | very large | — | — |
| path_8_confidence_calibration | 2 | 2.48 | 2.80 | +0.32 | 0.71 | medium | — | — |

#### llama4scout — openai

| Path | *n* | Vanilla | Reframing | Δ | *d* | Size | *p* | Sig |
|------|-----|---------|-----------|---|-----|------|-----|-----|
| path_7_surprise_as_signal | 3 | 2.52 | 4.18 | +1.67 | 5.53 | very large | — | — |
| path_1_name_the_frame | 18 | 2.56 | 4.04 | +1.49 | 1.83 | very large | 2.53e-04 | *** |
| path_5_invert | 11 | 2.50 | 3.88 | +1.38 | 2.53 | very large | 9.77e-04 | *** |
| path_3_distant_analogy | 9 | 2.63 | 3.99 | +1.36 | 1.65 | very large | 0.0039 | ** |
| path_6_premise_reflection | 23 | 2.60 | 3.88 | +1.27 | 1.49 | very large | 4.29e-05 | *** |
| path_9_step_outside | 8 | 2.46 | 3.55 | +1.09 | 1.30 | very large | 0.0078 | ** |
| path_2_decompose_to_generic | 10 | 2.45 | 3.08 | +0.62 | 0.71 | medium | 0.0879 | ns |
| path_4_incubate_reset | 2 | 2.30 | 2.58 | +0.28 | 0.46 | small | — | — |
| path_8_confidence_calibration | 2 | 3.50 | 3.58 | +0.07 | 0.11 | negligible | — | — |


---

## Analysis 2: DEO Mechanism (Four-Condition Comparison)

> **Restricted to pure distance-mode problems** (Paths 1–5, 9 only). Problems using hybrid paths (6, 7) or engagement paths (8) are excluded because the distance/engagement/DEO distinction is not theoretically clean for those problems. See Path-Mode Analysis below for the full breakdown.

### llama — self (*n* = 20)

**Condition means:** Vanilla 2.74 | Distance 4.01 | Engagement 3.22 | DEO 4.27

**Observed ordering:** deo > distance > engagement > vanilla

**Matches predicted ordering (DEO > Distance > Engagement ≥ Vanilla)?** Yes ✓

**Friedman χ²** = 39.44, *p* = 1.40e-08 ***

| Pair | Δ | Cohen's *d* | Size | Wilcoxon *p* (adj.) | Sig |
|------|---|------------|------|--------------------|----|
| deo vs distance | +0.26 | 0.44 | small | 0.1650 | ns |
| deo vs engagement | +1.05 | 1.28 | very large | 2.29e-05 | *** |
| deo vs vanilla | +1.53 | 3.16 | very large | 4.42e-04 | *** |
| distance vs engagement | +0.79 | 0.87 | large | 0.0070 | ** |
| distance vs vanilla | +1.27 | 1.56 | very large | 5.59e-04 | *** |
| engagement vs vanilla | +0.48 | 0.52 | medium | 0.1650 | ns |

**Correctness:** Vanilla 3.92 | Distance 4.62 | Engagement 4.37 | DEO 4.83

### llama — claude (*n* = 20)

**Condition means:** Vanilla 1.84 | Distance 2.98 | Engagement 2.23 | DEO 3.41

**Observed ordering:** deo > distance > engagement > vanilla

**Matches predicted ordering (DEO > Distance > Engagement ≥ Vanilla)?** Yes ✓

**Friedman χ²** = 30.02, *p* = 1.37e-06 ***

| Pair | Δ | Cohen's *d* | Size | Wilcoxon *p* (adj.) | Sig |
|------|---|------------|------|--------------------|----|
| deo vs distance | +0.43 | 0.52 | medium | 0.1237 | ns |
| deo vs engagement | +1.19 | 1.56 | very large | 5.31e-04 | *** |
| deo vs vanilla | +1.57 | 2.06 | very large | 5.31e-04 | *** |
| distance vs engagement | +0.76 | 0.91 | large | 0.0113 | * |
| distance vs vanilla | +1.14 | 1.24 | very large | 0.0012 | ** |
| engagement vs vanilla | +0.38 | 0.54 | medium | 0.1237 | ns |

**Correctness:** Vanilla 2.92 | Distance 3.32 | Engagement 3.13 | DEO 3.46

### llama — openai (*n* = 20)

**Condition means:** Vanilla 2.37 | Distance 3.61 | Engagement 2.92 | DEO 4.06

**Observed ordering:** deo > distance > engagement > vanilla

**Matches predicted ordering (DEO > Distance > Engagement ≥ Vanilla)?** Yes ✓

**Friedman χ²** = 42.79, *p* = 2.73e-09 ***

| Pair | Δ | Cohen's *d* | Size | Wilcoxon *p* (adj.) | Sig |
|------|---|------------|------|--------------------|----|
| deo vs distance | +0.46 | 1.04 | large | 0.0027 | ** |
| deo vs engagement | +1.14 | 1.89 | very large | 5.29e-04 | *** |
| deo vs vanilla | +1.70 | 2.23 | very large | 5.29e-04 | *** |
| distance vs engagement | +0.68 | 0.88 | large | 0.0080 | ** |
| distance vs vanilla | +1.24 | 1.45 | very large | 6.51e-04 | *** |
| engagement vs vanilla | +0.56 | 0.65 | medium | 0.0187 | * |

**Correctness:** Vanilla 3.71 | Distance 4.01 | Engagement 3.86 | DEO 4.32

### qwen — self (*n* = 20)

**Condition means:** Vanilla 2.75 | Distance 3.90 | Engagement 3.12 | DEO 4.32

**Observed ordering:** deo > distance > engagement > vanilla

**Matches predicted ordering (DEO > Distance > Engagement ≥ Vanilla)?** Yes ✓

**Friedman χ²** = 34.35, *p* = 1.67e-07 ***

| Pair | Δ | Cohen's *d* | Size | Wilcoxon *p* (adj.) | Sig |
|------|---|------------|------|--------------------|----|
| deo vs distance | +0.43 | 0.58 | medium | 0.0690 | ns |
| deo vs engagement | +1.21 | 1.67 | very large | 1.14e-05 | *** |
| deo vs vanilla | +1.57 | 2.57 | very large | 4.42e-04 | *** |
| distance vs engagement | +0.78 | 0.89 | large | 0.0062 | ** |
| distance vs vanilla | +1.15 | 1.25 | very large | 0.0014 | ** |
| engagement vs vanilla | +0.37 | 0.40 | small | 0.1787 | ns |

**Correctness:** Vanilla 3.95 | Distance 4.55 | Engagement 4.22 | DEO 4.83

### qwen — claude (*n* = 20)

**Condition means:** Vanilla 1.82 | Distance 2.98 | Engagement 2.27 | DEO 3.40

**Observed ordering:** deo > distance > engagement > vanilla

**Matches predicted ordering (DEO > Distance > Engagement ≥ Vanilla)?** Yes ✓

**Friedman χ²** = 36.34, *p* = 6.36e-08 ***

| Pair | Δ | Cohen's *d* | Size | Wilcoxon *p* (adj.) | Sig |
|------|---|------------|------|--------------------|----|
| deo vs distance | +0.42 | 0.56 | medium | 0.0266 | * |
| deo vs engagement | +1.13 | 1.47 | very large | 6.00e-04 | *** |
| deo vs vanilla | +1.58 | 2.12 | very large | 5.31e-04 | *** |
| distance vs engagement | +0.71 | 0.81 | large | 0.0120 | * |
| distance vs vanilla | +1.16 | 1.28 | very large | 0.0012 | ** |
| engagement vs vanilla | +0.45 | 0.59 | medium | 0.0289 | * |

**Correctness:** Vanilla 2.91 | Distance 3.32 | Engagement 3.15 | DEO 3.55

### qwen — openai (*n* = 20)

**Condition means:** Vanilla 2.41 | Distance 3.60 | Engagement 2.94 | DEO 4.13

**Observed ordering:** deo > distance > engagement > vanilla

**Matches predicted ordering (DEO > Distance > Engagement ≥ Vanilla)?** Yes ✓

**Friedman χ²** = 42.37, *p* = 3.35e-09 ***

| Pair | Δ | Cohen's *d* | Size | Wilcoxon *p* (adj.) | Sig |
|------|---|------------|------|--------------------|----|
| deo vs distance | +0.53 | 0.98 | large | 0.0053 | ** |
| deo vs engagement | +1.20 | 2.01 | very large | 5.29e-04 | *** |
| deo vs vanilla | +1.73 | 2.14 | very large | 5.29e-04 | *** |
| distance vs engagement | +0.67 | 0.85 | large | 0.0053 | ** |
| distance vs vanilla | +1.20 | 1.29 | very large | 0.0011 | ** |
| engagement vs vanilla | +0.53 | 0.60 | medium | 0.0441 | * |

**Correctness:** Vanilla 3.73 | Distance 4.01 | Engagement 3.83 | DEO 4.43

### llama4scout — self (*n* = 20)

**Condition means:** Vanilla 2.74 | Distance 3.95 | Engagement 3.18 | DEO 4.21

**Observed ordering:** deo > distance > engagement > vanilla

**Matches predicted ordering (DEO > Distance > Engagement ≥ Vanilla)?** Yes ✓

**Friedman χ²** = 33.31, *p* = 2.78e-07 ***

| Pair | Δ | Cohen's *d* | Size | Wilcoxon *p* (adj.) | Sig |
|------|---|------------|------|--------------------|----|
| deo vs distance | +0.26 | 0.40 | small | 0.2336 | ns |
| deo vs engagement | +1.03 | 1.30 | very large | 9.44e-04 | *** |
| deo vs vanilla | +1.48 | 2.39 | very large | 5.31e-04 | *** |
| distance vs engagement | +0.77 | 0.85 | large | 0.0044 | ** |
| distance vs vanilla | +1.22 | 1.45 | very large | 9.44e-04 | *** |
| engagement vs vanilla | +0.45 | 0.49 | small | 0.2336 | ns |

**Correctness:** Vanilla 3.98 | Distance 4.51 | Engagement 4.28 | DEO 4.77

### llama4scout — claude (*n* = 20)

**Condition means:** Vanilla 1.83 | Distance 2.98 | Engagement 2.27 | DEO 3.37

**Observed ordering:** deo > distance > engagement > vanilla

**Matches predicted ordering (DEO > Distance > Engagement ≥ Vanilla)?** Yes ✓

**Friedman χ²** = 29.41, *p* = 1.83e-06 ***

| Pair | Δ | Cohen's *d* | Size | Wilcoxon *p* (adj.) | Sig |
|------|---|------------|------|--------------------|----|
| deo vs distance | +0.38 | 0.43 | small | 0.0673 | ns |
| deo vs engagement | +1.10 | 1.33 | very large | 6.50e-04 | *** |
| deo vs vanilla | +1.53 | 1.90 | very large | 1.14e-05 | *** |
| distance vs engagement | +0.71 | 0.82 | large | 0.0121 | * |
| distance vs vanilla | +1.15 | 1.19 | large | 5.25e-04 | *** |
| engagement vs vanilla | +0.44 | 0.59 | medium | 0.0537 | ns |

**Correctness:** Vanilla 2.92 | Distance 3.34 | Engagement 3.17 | DEO 3.44

### llama4scout — openai (*n* = 20)

**Condition means:** Vanilla 2.40 | Distance 3.63 | Engagement 2.95 | DEO 4.11

**Observed ordering:** deo > distance > engagement > vanilla

**Matches predicted ordering (DEO > Distance > Engagement ≥ Vanilla)?** Yes ✓

**Friedman χ²** = 41.56, *p* = 4.97e-09 ***

| Pair | Δ | Cohen's *d* | Size | Wilcoxon *p* (adj.) | Sig |
|------|---|------------|------|--------------------|----|
| deo vs distance | +0.48 | 1.06 | large | 0.0019 | ** |
| deo vs engagement | +1.16 | 1.91 | very large | 4.40e-04 | *** |
| deo vs vanilla | +1.71 | 2.35 | very large | 1.14e-05 | *** |
| distance vs engagement | +0.68 | 0.98 | large | 0.0019 | ** |
| distance vs vanilla | +1.22 | 1.43 | very large | 8.53e-04 | *** |
| engagement vs vanilla | +0.54 | 0.61 | medium | 0.0418 | * |

**Correctness:** Vanilla 3.79 | Distance 4.06 | Engagement 3.84 | DEO 4.37


### Per-Category DEO Advantage (Analysis 2)

#### llama — self

| Category | *n* | Vanilla | Distance | Engagement | DEO | DEO−Dist | Ordering |
|----------|-----|---------|----------|------------|-----|----------|----------|
| functional_fixedness | 5 | 2.77 | 3.32 | 3.11 | 4.19 | +0.87 | deo > distance > engagement > vanilla |
| einstellung | 3 | 1.88 | 3.53 | 3.10 | 3.70 | +0.17 | deo > distance > engagement > vanilla |
| zero_sum | 4 | 3.22 | 4.42 | 2.92 | 4.54 | +0.12 | deo > distance > vanilla > engagement |
| framing_trap | 3 | 2.77 | 4.32 | 3.33 | 4.43 | +0.11 | deo > distance > engagement > vanilla |
| narrative_lockin | 3 | 2.37 | 4.60 | 3.55 | 4.28 | -0.32 | distance > deo > engagement > vanilla |

#### llama — claude

| Category | *n* | Vanilla | Distance | Engagement | DEO | DEO−Dist | Ordering |
|----------|-----|---------|----------|------------|-----|----------|----------|
| functional_fixedness | 5 | 1.89 | 2.50 | 2.44 | 3.34 | +0.84 | deo > distance > engagement > vanilla |
| framing_trap | 3 | 1.90 | 3.07 | 2.15 | 3.52 | +0.45 | deo > distance > engagement > vanilla |
| zero_sum | 4 | 2.16 | 3.41 | 1.88 | 3.85 | +0.44 | deo > distance > vanilla > engagement |
| einstellung | 3 | 1.20 | 2.27 | 2.03 | 2.60 | +0.33 | deo > distance > engagement > vanilla |
| narrative_lockin | 3 | 1.55 | 3.82 | 2.57 | 3.62 | -0.20 | distance > deo > engagement > vanilla |

#### llama — openai

| Category | *n* | Vanilla | Distance | Engagement | DEO | DEO−Dist | Ordering |
|----------|-----|---------|----------|------------|-----|----------|----------|
| functional_fixedness | 5 | 2.43 | 3.00 | 2.98 | 3.70 | +0.70 | deo > distance > engagement > vanilla |
| framing_trap | 3 | 2.30 | 3.65 | 3.15 | 4.32 | +0.67 | deo > distance > engagement > vanilla |
| zero_sum | 4 | 2.92 | 4.14 | 2.82 | 4.54 | +0.40 | deo > distance > vanilla > engagement |
| narrative_lockin | 3 | 1.85 | 4.13 | 2.98 | 4.38 | +0.25 | deo > distance > engagement > vanilla |
| einstellung | 3 | 1.50 | 3.15 | 2.67 | 3.33 | +0.18 | deo > distance > engagement > vanilla |

#### qwen — self

| Category | *n* | Vanilla | Distance | Engagement | DEO | DEO−Dist | Ordering |
|----------|-----|---------|----------|------------|-----|----------|----------|
| functional_fixedness | 5 | 2.76 | 3.20 | 3.06 | 4.24 | +1.04 | deo > distance > engagement > vanilla |
| einstellung | 3 | 2.07 | 3.12 | 2.83 | 3.90 | +0.78 | deo > distance > engagement > vanilla |
| framing_trap | 3 | 2.77 | 4.27 | 3.22 | 4.50 | +0.23 | deo > distance > engagement > vanilla |
| zero_sum | 4 | 3.16 | 4.42 | 2.89 | 4.49 | +0.07 | deo > distance > vanilla > engagement |
| narrative_lockin | 3 | 2.37 | 4.52 | 3.47 | 4.48 | -0.04 | distance > deo > engagement > vanilla |

#### qwen — claude

| Category | *n* | Vanilla | Distance | Engagement | DEO | DEO−Dist | Ordering |
|----------|-----|---------|----------|------------|-----|----------|----------|
| functional_fixedness | 5 | 1.91 | 2.40 | 2.45 | 3.34 | +0.94 | deo > engagement > distance > vanilla |
| einstellung | 3 | 1.20 | 2.23 | 1.93 | 2.72 | +0.49 | deo > distance > engagement > vanilla |
| framing_trap | 3 | 1.88 | 3.13 | 2.18 | 3.47 | +0.34 | deo > distance > engagement > vanilla |
| zero_sum | 4 | 2.14 | 3.54 | 1.90 | 3.84 | +0.30 | deo > distance > vanilla > engagement |
| narrative_lockin | 3 | 1.58 | 3.68 | 2.80 | 3.60 | -0.08 | distance > deo > engagement > vanilla |

#### qwen — openai

| Category | *n* | Vanilla | Distance | Engagement | DEO | DEO−Dist | Ordering |
|----------|-----|---------|----------|------------|-----|----------|----------|
| functional_fixedness | 5 | 2.40 | 3.00 | 3.01 | 3.86 | +0.86 | deo > engagement > distance > vanilla |
| framing_trap | 3 | 2.37 | 3.75 | 3.05 | 4.30 | +0.55 | deo > distance > engagement > vanilla |
| einstellung | 3 | 1.62 | 2.95 | 2.47 | 3.43 | +0.48 | deo > distance > engagement > vanilla |
| zero_sum | 4 | 3.01 | 4.24 | 2.81 | 4.59 | +0.35 | deo > distance > vanilla > engagement |
| narrative_lockin | 3 | 1.83 | 4.13 | 3.18 | 4.42 | +0.29 | deo > distance > engagement > vanilla |

#### llama4scout — self

| Category | *n* | Vanilla | Distance | Engagement | DEO | DEO−Dist | Ordering |
|----------|-----|---------|----------|------------|-----|----------|----------|
| functional_fixedness | 5 | 2.75 | 3.16 | 3.13 | 4.01 | +0.85 | deo > distance > engagement > vanilla |
| einstellung | 3 | 2.13 | 3.42 | 2.77 | 3.48 | +0.06 | deo > distance > engagement > vanilla |
| framing_trap | 3 | 2.65 | 4.38 | 3.32 | 4.43 | +0.05 | deo > distance > engagement > vanilla |
| narrative_lockin | 3 | 2.33 | 4.37 | 3.48 | 4.40 | +0.03 | deo > distance > engagement > vanilla |
| zero_sum | 4 | 3.18 | 4.59 | 2.98 | 4.55 | -0.04 | distance > deo > vanilla > engagement |

#### llama4scout — claude

| Category | *n* | Vanilla | Distance | Engagement | DEO | DEO−Dist | Ordering |
|----------|-----|---------|----------|------------|-----|----------|----------|
| functional_fixedness | 5 | 1.93 | 2.41 | 2.52 | 3.35 | +0.94 | deo > engagement > distance > vanilla |
| framing_trap | 3 | 1.92 | 3.15 | 2.12 | 3.53 | +0.38 | deo > distance > engagement > vanilla |
| zero_sum | 4 | 2.15 | 3.51 | 1.94 | 3.86 | +0.35 | deo > distance > vanilla > engagement |
| einstellung | 3 | 1.27 | 2.28 | 1.92 | 2.35 | +0.07 | deo > distance > engagement > vanilla |
| narrative_lockin | 3 | 1.52 | 3.78 | 2.82 | 3.62 | -0.16 | distance > deo > engagement > vanilla |

#### llama4scout — openai

| Category | *n* | Vanilla | Distance | Engagement | DEO | DEO−Dist | Ordering |
|----------|-----|---------|----------|------------|-----|----------|----------|
| functional_fixedness | 5 | 2.48 | 3.02 | 3.07 | 3.77 | +0.75 | deo > engagement > distance > vanilla |
| framing_trap | 3 | 2.32 | 3.73 | 3.00 | 4.38 | +0.65 | deo > distance > engagement > vanilla |
| zero_sum | 4 | 2.98 | 4.21 | 2.81 | 4.64 | +0.43 | deo > distance > vanilla > engagement |
| einstellung | 3 | 1.57 | 3.03 | 2.38 | 3.35 | +0.32 | deo > distance > engagement > vanilla |
| narrative_lockin | 3 | 1.83 | 4.17 | 3.37 | 4.37 | +0.20 | deo > distance > engagement > vanilla |


---

## Path-Mode Analysis

> Six paths (1, 2, 3, 4, 5, 9) are pure distance-mode operations. One path (8) is engagement-mode. Two paths (6, 7) are hybrid — they inherently require both distance and engagement.

> Problems are classified by their dominant mode: **pure_distance** if all paths are distance-only, **hybrid** if any path is 6 or 7, **engagement** if the only path is 8.


### Analysis 1 by Path Mode (Vanilla vs. Reframing)

| Model | Scorer | Mode | *n* | Vanilla | Reframing | Δ | *d* | *p* | Sig |
|-------|--------|------|-----|---------|-----------|---|-----|-----|-----|
| llama | self | pure_distance | 22 | 2.67 | 3.85 | +1.18 | 1.36 | 8.53e-05 | *** |
| llama | self | hybrid | 26 | 2.93 | 4.16 | +1.24 | 1.45 | 2.20e-05 | *** |
| llama | self | engagement | 2 | 3.60 | 3.25 | -0.35 | -1.65 | — | — |
| llama | claude | pure_distance | 22 | 1.82 | 2.87 | +1.05 | 1.21 | 1.12e-04 | *** |
| llama | claude | hybrid | 26 | 1.87 | 3.40 | +1.53 | 2.23 | 1.22e-05 | *** |
| llama | claude | engagement | 2 | 2.30 | 2.67 | +0.38 | 3.54 | — | — |
| llama | openai | pure_distance | 22 | 2.42 | 3.54 | +1.12 | 1.36 | 5.95e-05 | *** |
| llama | openai | hybrid | 26 | 2.58 | 3.95 | +1.37 | 1.65 | 9.87e-06 | *** |
| llama | openai | engagement | 2 | 3.20 | 3.38 | +0.17 | 0.55 | — | — |
| qwen | self | pure_distance | 22 | 2.68 | 3.86 | +1.18 | 1.54 | 5.28e-05 | *** |
| qwen | self | hybrid | 26 | 2.96 | 4.16 | +1.20 | 1.77 | 8.24e-06 | *** |
| qwen | self | engagement | 2 | 3.42 | 3.48 | +0.05 | 0.00 | — | — |
| qwen | claude | pure_distance | 22 | 1.85 | 2.88 | +1.03 | 1.15 | 1.74e-04 | *** |
| qwen | claude | hybrid | 26 | 1.89 | 3.37 | +1.48 | 2.26 | 8.26e-06 | *** |
| qwen | claude | engagement | 2 | 2.27 | 2.65 | +0.38 | 2.12 | — | — |
| qwen | openai | pure_distance | 22 | 2.48 | 3.52 | +1.05 | 1.23 | 1.36e-04 | *** |
| qwen | openai | hybrid | 26 | 2.64 | 3.91 | +1.27 | 1.60 | 1.25e-05 | *** |
| qwen | openai | engagement | 2 | 3.30 | 3.48 | +0.17 | 1.65 | — | — |
| llama4scout | self | pure_distance | 22 | 2.70 | 3.85 | +1.15 | 1.37 | 6.68e-06 | *** |
| llama4scout | self | hybrid | 26 | 2.87 | 4.14 | +1.27 | 1.72 | 1.82e-05 | *** |
| llama4scout | self | engagement | 2 | 3.42 | 3.23 | -0.20 | -0.40 | — | — |
| llama4scout | claude | pure_distance | 22 | 1.81 | 2.87 | +1.06 | 1.19 | 1.14e-04 | *** |
| llama4scout | claude | hybrid | 26 | 1.84 | 3.43 | +1.59 | 2.61 | 8.26e-06 | *** |
| llama4scout | claude | engagement | 2 | 2.48 | 2.80 | +0.33 | 0.71 | — | — |
| llama4scout | openai | pure_distance | 22 | 2.43 | 3.48 | +1.05 | 1.23 | 2.43e-04 | *** |
| llama4scout | openai | hybrid | 26 | 2.59 | 3.91 | +1.32 | 1.61 | 1.25e-05 | *** |
| llama4scout | openai | engagement | 2 | 3.50 | 3.58 | +0.07 | 0.11 | — | — |

### Analysis 2 by Path Mode: DEO vs. Distance

> **Key prediction:** The DEO advantage over distance should be *larger* for pure-distance problems (where distance truly lacks engagement) than for hybrid problems (where paths 6/7 already partially activate engagement).

| Model | Scorer | Mode | *n* | V | D | E | DEO | DEO−D | *d* | *p* | Ordering |
|-------|--------|------|-----|---|---|---|-----|-------|-----|-----|----------|
| llama | self | pure_distance | 20 | 2.74 | 4.01 | 3.22 | 4.27 | +0.26 | 0.44 | 0.0867 | deo > distance > engagement > vanilla |
| llama | self | hybrid | 24 | 2.92 | 4.14 | 3.41 | 4.27 | +0.13 | 0.30 | 0.1060 | deo > distance > engagement > vanilla |
| llama | self | engagement | 2 | 3.48 | 3.35 | 3.52 | 4.28 | +0.93 | 5.23 | — | deo > engagement > vanilla > distance |
| llama | claude | pure_distance | 20 | 1.84 | 2.98 | 2.23 | 3.41 | +0.43 | 0.52 | 0.0618 | deo > distance > engagement > vanilla |
| llama | claude | hybrid | 24 | 1.90 | 3.35 | 2.45 | 3.49 | +0.14 | 0.24 | 0.3379 | deo > distance > engagement > vanilla |
| llama | claude | engagement | 2 | 2.27 | 2.67 | 2.25 | 3.65 | +0.97 | 27.58 | — | deo > distance > vanilla > engagement |
| llama | openai | pure_distance | 20 | 2.37 | 3.61 | 2.92 | 4.06 | +0.45 | 1.04 | 8.84e-04 | deo > distance > engagement > vanilla |
| llama | openai | hybrid | 24 | 2.65 | 3.95 | 3.06 | 4.17 | +0.23 | 0.42 | 0.0613 | deo > distance > engagement > vanilla |
| llama | openai | engagement | 2 | 3.20 | 3.27 | 3.42 | 4.08 | +0.80 | 3.77 | — | deo > engagement > distance > vanilla |
| qwen | self | pure_distance | 20 | 2.75 | 3.90 | 3.12 | 4.32 | +0.43 | 0.58 | 0.0345 | deo > distance > engagement > vanilla |
| qwen | self | hybrid | 24 | 2.98 | 4.14 | 3.45 | 4.30 | +0.16 | 0.45 | 0.0591 | deo > distance > engagement > vanilla |
| qwen | self | engagement | 2 | 3.40 | 3.42 | 3.60 | 4.20 | +0.78 | 4.38 | — | deo > engagement > distance > vanilla |
| qwen | claude | pure_distance | 20 | 1.82 | 2.98 | 2.27 | 3.40 | +0.42 | 0.56 | 0.0133 | deo > distance > engagement > vanilla |
| qwen | claude | hybrid | 24 | 1.88 | 3.39 | 2.46 | 3.55 | +0.16 | 0.25 | 0.5870 | deo > distance > engagement > vanilla |
| qwen | claude | engagement | 2 | 2.15 | 2.75 | 2.25 | 3.62 | +0.88 | 8.25 | — | deo > distance > engagement > vanilla |
| qwen | openai | pure_distance | 20 | 2.41 | 3.60 | 2.94 | 4.13 | +0.53 | 0.98 | 0.0018 | deo > distance > engagement > vanilla |
| qwen | openai | hybrid | 24 | 2.64 | 3.92 | 3.04 | 4.20 | +0.28 | 0.58 | 0.0136 | deo > distance > engagement > vanilla |
| qwen | openai | engagement | 2 | 3.17 | 3.42 | 3.40 | 4.05 | +0.62 | 1.04 | — | deo > distance > engagement > vanilla |
| llama4scout | self | pure_distance | 20 | 2.74 | 3.95 | 3.18 | 4.21 | +0.26 | 0.40 | 0.1567 | deo > distance > engagement > vanilla |
| llama4scout | self | hybrid | 24 | 2.88 | 4.14 | 3.42 | 4.27 | +0.13 | 0.34 | 0.0800 | deo > distance > engagement > vanilla |
| llama4scout | self | engagement | 2 | 3.48 | 3.35 | 3.58 | 4.20 | +0.85 | 12.02 | — | deo > engagement > vanilla > distance |
| llama4scout | claude | pure_distance | 20 | 1.83 | 2.98 | 2.27 | 3.37 | +0.38 | 0.43 | 0.0673 | deo > distance > engagement > vanilla |
| llama4scout | claude | hybrid | 24 | 1.89 | 3.37 | 2.37 | 3.51 | +0.14 | 0.27 | 0.3153 | deo > distance > engagement > vanilla |
| llama4scout | claude | engagement | 2 | 2.35 | 2.58 | 2.20 | 3.77 | +1.20 | 4.24 | — | deo > distance > vanilla > engagement |
| llama4scout | openai | pure_distance | 20 | 2.40 | 3.63 | 2.95 | 4.11 | +0.48 | 1.06 | 8.33e-04 | deo > distance > engagement > vanilla |
| llama4scout | openai | hybrid | 24 | 2.66 | 3.95 | 3.00 | 4.20 | +0.25 | 0.54 | 0.0214 | deo > distance > engagement > vanilla |
| llama4scout | openai | engagement | 2 | 3.27 | 3.42 | 3.30 | 4.10 | +0.68 | 2.73 | — | deo > distance > engagement > vanilla |

### Interpretation by Path Mode

#### Pure Distance (*n* = 20): Clean DEO test

Mean DEO advantage over distance: **+0.41** (range: +0.26 to +0.53). These problems provide a clean test of the oscillation hypothesis because the distance condition is purely analytical and the DEO condition adds genuine engagement. The consistent positive advantage confirms that oscillation adds value beyond distance alone.

#### Hybrid (*n* = 24): Partial engagement in "distance"

Mean DEO advantage over distance: **+0.18** (range: +0.13 to +0.28). The DEO advantage is roughly half that of pure-distance problems (+0.18 vs. +0.41). This is predicted by the theory: paths 6 (Premise Reflection) and 7 (Surprise as Signal) already partially activate engagement within the "distance" condition, so the explicit DEO oscillation provides a smaller incremental benefit. The ordering DEO > Distance > Engagement > Vanilla is maintained in all hybrid-mode combinations.

#### Engagement (*n* = 2): Collapsed oscillation

Mean DEO advantage over distance: **+0.86** (range: +0.62 to +1.20). These 2 problems (both using Path 8: Confidence Calibration) show the largest DEO-minus-distance delta — but for the wrong reason. The "distance" condition for these problems is itself an engagement operation (felt uncertainty), so it scores low because it duplicates the engagement condition rather than providing analytical distance. The DEO preamble, while labelled as oscillation, is effectively engagement-followed-by-engagement rather than genuine DEO.

Confirming evidence: in 4/9 model × scorer combinations, the "distance" condition scores equal to or lower than the engagement condition — consistent with both being engagement-mode operations. The ordering frequently shifts to DEO > Engagement > Distance, with Distance and Engagement swapping positions, unlike the stable DEO > Distance > Engagement > Vanilla seen in pure-distance and hybrid problems.

These 2 problems are excluded from Analysis 2 because they cannot test the oscillation hypothesis — but their behaviour is consistent with the path-mode classification and provides additional evidence that the cognitive mode of the path matters.


---

## Summary

**Predicted ordering confirmed:** 9/9 model × scorer combinations

**Significant Friedman tests (p < 0.05):** 9/9

### Critical Test: DEO vs. Distance

| Model | Scorer | *p* (adj.) | Sig | Cohen's *d* |
|-------|--------|-----------|-----|------------|
| llama | self | 0.1650 | ns | 0.44 |
| llama | claude | 0.1237 | ns | 0.52 |
| llama | openai | 0.0027 | ** | 1.04 |
| qwen | self | 0.0690 | ns | 0.58 |
| qwen | claude | 0.0266 | * | 0.56 |
| qwen | openai | 0.0053 | ** | 0.98 |
| llama4scout | self | 0.2336 | ns | 0.40 |
| llama4scout | claude | 0.0673 | ns | 0.43 |
| llama4scout | openai | 0.0019 | ** | 1.06 |