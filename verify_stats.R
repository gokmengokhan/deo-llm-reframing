#!/usr/bin/env Rscript
# =============================================================================
# R verification of Python statistical analysis
# Mirrors run_stats.py exactly — same tests, same data, independent implementation
# =============================================================================

suppressPackageStartupMessages({
  library(dplyr)
  library(tidyr)
})

cat("=" |> rep(60) |> paste(collapse=""), "\n")
cat("  R Verification of Statistical Analysis\n")
cat("=" |> rep(60) |> paste(collapse=""), "\n\n")

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------

s1 <- read.csv("paper/study1_data.csv", stringsAsFactors = FALSE)
s2 <- read.csv("paper/study2_data.csv", stringsAsFactors = FALSE)

cat("Study 1:", nrow(s1), "rows\n")
cat("Study 2:", nrow(s2), "rows\n\n")

models  <- c("llama", "qwen", "llama4scout")
scorers <- c("self", "claude", "openai")

# ---------------------------------------------------------------------------
# Helper: compute problem-level means (average across 5 runs)
# ---------------------------------------------------------------------------

problem_means <- function(data, model_name, scorer_name) {
  data |>
    filter(model == model_name, scorer == scorer_name) |>
    group_by(problem_id, condition) |>
    summarise(
      reframing = mean(reframing_score),
      correctness = mean(correctness),
      .groups = "drop"
    ) |>
    pivot_wider(names_from = condition, values_from = c(reframing, correctness))
}

# =============================================================================
# ANALYSIS 1: Vanilla vs. Distance
# =============================================================================

cat("=" |> rep(60) |> paste(collapse=""), "\n")
cat("  ANALYSIS 1: Vanilla vs. Distance\n")
cat("=" |> rep(60) |> paste(collapse=""), "\n\n")

cat(sprintf("%-12s %-8s %5s %8s %8s %8s %8s %12s %5s\n",
            "Model", "Scorer", "n", "Vanilla", "Dist", "Delta", "d",
            "Wilcoxon_p", "Sig"))
cat(strrep("-", 85), "\n")

for (m in models) {
  for (sc in scorers) {
    pm <- problem_means(s1, m, sc)

    v <- pm$reframing_vanilla
    d <- pm$reframing_distance
    n <- length(v)

    diff <- d - v
    mean_v <- mean(v)
    mean_d <- mean(d)
    delta  <- mean_d - mean_v

    # Cohen's d (paired: mean diff / SD of diffs)
    sd_diff <- sd(diff)
    cohens_d <- if (sd_diff > 0) mean(diff) / sd_diff else 0

    # Wilcoxon signed-rank
    wt <- wilcox.test(d, v, paired = TRUE, exact = FALSE)

    sig <- if (wt$p.value < 0.001) "***"
           else if (wt$p.value < 0.01) "**"
           else if (wt$p.value < 0.05) "*"
           else "ns"

    cat(sprintf("%-12s %-8s %5d %8.3f %8.3f %+8.3f %8.3f %12.2e %5s\n",
                m, sc, n, mean_v, mean_d, delta, cohens_d, wt$p.value, sig))
  }
}

# Correctness check
cat("\n  Correctness Check:\n")
cat(sprintf("%-12s %-8s %8s %8s %12s %5s\n",
            "Model", "Scorer", "V_corr", "D_corr", "t_p", "Sig"))
cat(strrep("-", 60), "\n")

for (m in models) {
  for (sc in scorers) {
    pm <- problem_means(s1, m, sc)
    vc <- pm$correctness_vanilla
    dc <- pm$correctness_distance
    tt <- t.test(dc, vc, paired = TRUE)
    sig <- if (tt$p.value < 0.001) "***"
           else if (tt$p.value < 0.01) "**"
           else if (tt$p.value < 0.05) "*"
           else "ns"
    cat(sprintf("%-12s %-8s %8.3f %8.3f %12.2e %5s\n",
                m, sc, mean(vc), mean(dc), tt$p.value, sig))
  }
}

# Shapiro-Wilk
cat("\n  Shapiro-Wilk on differences:\n")
cat(sprintf("%-12s %-8s %12s %8s\n", "Model", "Scorer", "Shapiro_p", "Normal"))
cat(strrep("-", 45), "\n")

for (m in models) {
  for (sc in scorers) {
    pm <- problem_means(s1, m, sc)
    diff <- pm$reframing_distance - pm$reframing_vanilla
    sw <- shapiro.test(diff)
    normal <- if (sw$p.value > 0.05) "yes" else "no"
    cat(sprintf("%-12s %-8s %12.4f %8s\n", m, sc, sw$p.value, normal))
  }
}

# =============================================================================
# ANALYSIS 2: Four-condition DEO comparison
# =============================================================================

cat("\n")
cat("=" |> rep(60) |> paste(collapse=""), "\n")
cat("  ANALYSIS 2: DEO Mechanism (Four Conditions)\n")
cat("=" |> rep(60) |> paste(collapse=""), "\n\n")

problem_means_4 <- function(data, model_name, scorer_name) {
  data |>
    filter(model == model_name, scorer == scorer_name) |>
    group_by(problem_id, condition) |>
    summarise(reframing = mean(reframing_score), .groups = "drop") |>
    pivot_wider(names_from = condition, values_from = reframing)
}

for (m in models) {
  for (sc in scorers) {
    pm <- problem_means_4(s2, m, sc)
    n <- nrow(pm)

    means <- c(
      vanilla    = mean(pm$vanilla),
      distance   = mean(pm$distance),
      engagement = mean(pm$engagement),
      deo        = mean(pm$deo)
    )
    ordering <- names(sort(means, decreasing = TRUE))
    predicted <- identical(ordering, c("deo", "distance", "engagement", "vanilla")) ||
                 identical(ordering, c("deo", "distance", "vanilla", "engagement"))

    # Friedman test
    # Needs matrix: rows = problems, cols = conditions
    mat <- as.matrix(pm[, c("vanilla", "distance", "engagement", "deo")])
    ft <- friedman.test(mat)

    cat(sprintf("--- %s / %s (n=%d) ---\n", m, sc, n))
    cat(sprintf("  Means: V=%.2f  D=%.2f  E=%.2f  DEO=%.2f\n",
                means["vanilla"], means["distance"], means["engagement"], means["deo"]))
    cat(sprintf("  Ordering: %s\n", paste(ordering, collapse=" > ")))
    cat(sprintf("  Predicted match: %s\n", if (predicted) "YES" else "NO"))
    cat(sprintf("  Friedman chi2=%.2f, p=%.2e %s\n",
                ft$statistic, ft$p.value,
                if (ft$p.value < 0.001) "***"
                else if (ft$p.value < 0.01) "**"
                else if (ft$p.value < 0.05) "*"
                else "ns"))

    # Post-hoc pairwise Wilcoxon (with Holm correction)
    pairs <- list(
      c("deo", "distance"),
      c("deo", "engagement"),
      c("deo", "vanilla"),
      c("distance", "engagement"),
      c("distance", "vanilla"),
      c("engagement", "vanilla")
    )

    raw_ps <- numeric(length(pairs))
    pair_labels <- character(length(pairs))
    ds <- numeric(length(pairs))

    for (i in seq_along(pairs)) {
      a <- pm[[ pairs[[i]][1] ]]
      b <- pm[[ pairs[[i]][2] ]]
      diff <- a - b
      sd_d <- sd(diff)
      ds[i] <- if (sd_d > 0) mean(diff) / sd_d else 0
      wt <- wilcox.test(a, b, paired = TRUE, exact = FALSE)
      raw_ps[i] <- wt$p.value
      pair_labels[i] <- paste(pairs[[i]], collapse=" vs ")
    }

    adj_ps <- p.adjust(raw_ps, method = "holm")

    cat("  Pairwise (Holm-adjusted):\n")
    cat(sprintf("    %-24s %+6s %6s %12s %5s\n", "Pair", "d", "Size", "p_adj", "Sig"))
    for (i in seq_along(pairs)) {
      sz <- if (abs(ds[i]) >= 1.2) "vlrg"
            else if (abs(ds[i]) >= 0.8) "lrg"
            else if (abs(ds[i]) >= 0.5) "med"
            else if (abs(ds[i]) >= 0.2) "sml"
            else "negl"
      sig <- if (adj_ps[i] < 0.001) "***"
             else if (adj_ps[i] < 0.01) "**"
             else if (adj_ps[i] < 0.05) "*"
             else "ns"
      cat(sprintf("    %-24s %+6.2f %6s %12.2e %5s\n",
                  pair_labels[i], ds[i], sz, adj_ps[i], sig))
    }
    cat("\n")
  }
}

# =============================================================================
# SUMMARY: Critical test — DEO vs Distance across all combos
# =============================================================================

cat("=" |> rep(60) |> paste(collapse=""), "\n")
cat("  CRITICAL TEST: DEO vs. Distance\n")
cat("=" |> rep(60) |> paste(collapse=""), "\n\n")

cat(sprintf("%-12s %-8s %12s %5s %8s\n",
            "Model", "Scorer", "p_adj", "Sig", "d"))
cat(strrep("-", 50), "\n")

for (m in models) {
  for (sc in scorers) {
    pm <- problem_means_4(s2, m, sc)
    a <- pm$deo
    b <- pm$distance
    diff <- a - b
    sd_d <- sd(diff)
    d_val <- if (sd_d > 0) mean(diff) / sd_d else 0

    # Run all 6 pairwise for Holm correction
    pairs_data <- list(
      c("deo", "distance"), c("deo", "engagement"), c("deo", "vanilla"),
      c("distance", "engagement"), c("distance", "vanilla"), c("engagement", "vanilla")
    )
    raw_ps <- numeric(6)
    for (i in seq_along(pairs_data)) {
      wt <- wilcox.test(pm[[ pairs_data[[i]][1] ]], pm[[ pairs_data[[i]][2] ]],
                        paired = TRUE, exact = FALSE)
      raw_ps[i] <- wt$p.value
    }
    adj_ps <- p.adjust(raw_ps, method = "holm")
    p_deo_dist <- adj_ps[1]  # first pair is deo vs distance

    sig <- if (p_deo_dist < 0.001) "***"
           else if (p_deo_dist < 0.01) "**"
           else if (p_deo_dist < 0.05) "*"
           else "ns"

    cat(sprintf("%-12s %-8s %12.2e %5s %8.2f\n", m, sc, p_deo_dist, sig, d_val))
  }
}

cat("\n  Done.\n")
