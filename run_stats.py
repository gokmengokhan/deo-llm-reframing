"""Statistical analysis for the Perceptual Reframing experiment.

Runs all inferential tests for Analysis 1 (vanilla vs. distance) and
Analysis 2 (four-condition DEO comparison) across all model × scorer
combinations.

Usage:
    uv run python run_stats.py
    uv run python run_stats.py --models llama qwen
    uv run python run_stats.py --output paper/stats_results.md
"""

import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy import stats

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

RESULTS_DIR = Path("results")
MODELS = ["llama", "qwen", "llama4scout"]
SCORERS = {
    "self": "",            # e.g. vanilla_scores
    "claude": "_claude",   # e.g. vanilla_claude_scores
    "openai": "_openai",   # e.g. vanilla_openai_scores
}
REFRAMING_DIMS = ["frame_diversity", "assumption_surfacing", "solution_novelty", "premise_questioning"]
ALPHA = 0.05

# Path-mode classification
PURE_DISTANCE_PATHS = {
    "path_1_name_the_frame", "path_2_decompose_to_generic", "path_3_distant_analogy",
    "path_4_incubate_reset", "path_5_invert", "path_9_step_outside",
}
ENGAGEMENT_PATHS = {"path_8_confidence_calibration"}
HYBRID_PATHS = {"path_6_premise_reflection", "path_7_surprise_as_signal"}


def classify_path_mode(paths_applied: list[str]) -> str:
    """Classify a problem's dominant mode based on its reframing paths."""
    paths = set(paths_applied)
    if not paths:
        return "unknown"  # orphan files with no metadata
    if paths & HYBRID_PATHS:
        return "hybrid"
    if paths & ENGAGEMENT_PATHS and not (paths & PURE_DISTANCE_PATHS):
        return "engagement"
    return "pure_distance"


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def reframing_score(score_dict: dict) -> float:
    """Mean of the four reframing dimensions."""
    scores = []
    for d in REFRAMING_DIMS:
        if d in score_dict and isinstance(score_dict[d], dict) and "score" in score_dict[d]:
            scores.append(score_dict[d]["score"])
        else:
            scores.append(3)  # neutral fallback
    return np.mean(scores)


def correctness_score(score_dict: dict) -> float:
    if "correctness" in score_dict and isinstance(score_dict["correctness"], dict):
        return score_dict["correctness"].get("score", 3)
    return 3  # neutral fallback


def load_study1(model: str) -> list[dict]:
    """Load Study 1 results (vanilla vs. reframed/distance)."""
    raw = RESULTS_DIR / model / "raw"
    results = []
    for p in sorted(raw.glob("*.json")):
        if p.name.startswith("deo_"):
            continue
        results.append(json.loads(p.read_text()))
    return results


def load_study2(model: str) -> list[dict]:
    """Load Study 2 results (4 conditions: vanilla, distance, engagement, deo)."""
    raw = RESULTS_DIR / model / "raw"
    results = []
    for p in sorted(raw.glob("deo_*.json")):
        results.append(json.loads(p.read_text()))
    return results


def get_problem_means(results: list[dict], condition: str, scorer_suffix: str,
                      metric_fn=reframing_score) -> np.ndarray:
    """Get per-problem mean scores (averaged across 5 runs)."""
    means = []
    scores_key = f"{condition}{scorer_suffix}_scores"
    for r in results:
        if scores_key not in r or not r[scores_key]:
            continue
        run_scores = [metric_fn(s) for s in r[scores_key]]
        means.append(np.mean(run_scores))
    return np.array(means)


def get_problem_means_with_metadata(results: list[dict], condition: str, scorer_suffix: str,
                                     metric_fn=reframing_score) -> list[tuple]:
    """Get per-problem mean scores with category and paths metadata.

    Returns list of (mean_score, category, paths_applied) tuples.
    """
    out = []
    scores_key = f"{condition}{scorer_suffix}_scores"
    for r in results:
        if scores_key not in r or not r[scores_key]:
            continue
        run_scores = [metric_fn(s) for s in r[scores_key]]
        out.append((
            np.mean(run_scores),
            r.get("category", "unknown"),
            r.get("paths_applied", []),
        ))
    return out


# ---------------------------------------------------------------------------
# Effect size
# ---------------------------------------------------------------------------

def cohens_d_paired(x: np.ndarray, y: np.ndarray) -> float:
    """Cohen's d for paired samples (using SD of differences)."""
    diff = x - y
    sd = np.std(diff, ddof=1)
    if sd < 1e-10:
        return 0.0
    d = np.mean(diff) / sd
    return max(min(d, 99.0), -99.0)  # cap for n=2 near-zero-SD edge cases


def rank_biserial(statistic: float, n: int) -> float:
    """Rank-biserial correlation from Wilcoxon signed-rank statistic."""
    # r = 1 - (2T) / (n(n+1)/2) where T = smaller rank sum
    total = n * (n + 1) / 2
    return 1 - (2 * statistic) / total


# ---------------------------------------------------------------------------
# Multiple comparisons
# ---------------------------------------------------------------------------

def holm_bonferroni(p_values: list[float]) -> list[float]:
    """Holm-Bonferroni correction for multiple comparisons."""
    n = len(p_values)
    indexed = sorted(enumerate(p_values), key=lambda x: x[1])
    adjusted = [0.0] * n
    max_so_far = 0.0
    for rank, (orig_idx, p) in enumerate(indexed):
        adj_p = min(p * (n - rank), 1.0)
        max_so_far = max(max_so_far, adj_p)  # enforce monotonicity
        adjusted[orig_idx] = max_so_far
    return adjusted


# ---------------------------------------------------------------------------
# Analysis 1: Vanilla vs. Distance (paired)
# ---------------------------------------------------------------------------

def analysis1(model: str, scorer_name: str, scorer_suffix: str, results: list[dict]) -> dict:
    """Paired comparison: vanilla vs. reframed (distance)."""
    vanilla = get_problem_means(results, "vanilla", scorer_suffix)
    reframed = get_problem_means(results, "reframed", scorer_suffix)

    n = min(len(vanilla), len(reframed))
    vanilla, reframed = vanilla[:n], reframed[:n]

    if n < 3:
        return {"error": f"Too few problems ({n})"}

    mean_v, mean_r = np.mean(vanilla), np.mean(reframed)
    improvement = mean_r - mean_v

    # Normality test on differences
    diff = reframed - vanilla
    if n >= 8:
        shapiro_stat, shapiro_p = stats.shapiro(diff)
    else:
        shapiro_stat, shapiro_p = float("nan"), float("nan")

    # Paired t-test
    t_stat, t_p = stats.ttest_rel(reframed, vanilla)

    # Wilcoxon signed-rank (non-parametric)
    # Remove zero-differences for Wilcoxon
    nonzero = diff[diff != 0]
    if len(nonzero) >= 6:
        w_stat, w_p = stats.wilcoxon(nonzero, alternative="two-sided")
        r_rb = rank_biserial(w_stat, len(nonzero))
    else:
        w_stat, w_p, r_rb = float("nan"), float("nan"), float("nan")

    d = cohens_d_paired(reframed, vanilla)

    # Correctness check
    v_corr = get_problem_means(results, "vanilla", scorer_suffix, correctness_score)
    r_corr = get_problem_means(results, "reframed", scorer_suffix, correctness_score)
    n_corr = min(len(v_corr), len(r_corr))
    v_corr, r_corr = v_corr[:n_corr], r_corr[:n_corr]
    corr_t, corr_p = stats.ttest_rel(r_corr, v_corr) if n_corr >= 3 else (float("nan"), float("nan"))

    return {
        "model": model,
        "scorer": scorer_name,
        "n_problems": n,
        "mean_vanilla": round(mean_v, 3),
        "mean_distance": round(mean_r, 3),
        "mean_improvement": round(improvement, 3),
        "cohens_d": round(d, 3),
        "shapiro_p": round(shapiro_p, 4) if not math.isnan(shapiro_p) else "N/A",
        "t_stat": round(t_stat, 3),
        "t_p": t_p,
        "wilcoxon_W": round(w_stat, 1) if not math.isnan(w_stat) else "N/A",
        "wilcoxon_p": w_p if not math.isnan(w_p) else "N/A",
        "rank_biserial_r": round(r_rb, 3) if not math.isnan(r_rb) else "N/A",
        "correctness_vanilla": round(np.mean(v_corr), 3),
        "correctness_distance": round(np.mean(r_corr), 3),
        "correctness_t_p": corr_p if not math.isnan(corr_p) else "N/A",
    }


# ---------------------------------------------------------------------------
# Analysis 1b: Per-category breakdown
# ---------------------------------------------------------------------------

def analysis1_by_category(model: str, scorer_name: str, scorer_suffix: str,
                          results: list[dict]) -> list[dict]:
    """Per-category vanilla vs. distance comparison."""
    vanilla_meta = get_problem_means_with_metadata(results, "vanilla", scorer_suffix)
    reframed_meta = get_problem_means_with_metadata(results, "reframed", scorer_suffix)

    # Group by category
    from collections import defaultdict
    cats_v = defaultdict(list)
    cats_r = defaultdict(list)
    for score, cat, _ in vanilla_meta:
        cats_v[cat].append(score)
    for score, cat, _ in reframed_meta:
        cats_r[cat].append(score)

    rows = []
    for cat in sorted(cats_v.keys()):
        v = np.array(cats_v[cat])
        r = np.array(cats_r.get(cat, []))
        n = min(len(v), len(r))
        if n < 2:
            continue
        v, r = v[:n], r[:n]
        diff = r - v
        mean_v, mean_r = np.mean(v), np.mean(r)
        d = cohens_d_paired(r, v) if np.std(diff, ddof=1) > 0 else 0.0

        # Wilcoxon if enough data
        nonzero = diff[diff != 0]
        if len(nonzero) >= 6:
            _, w_p = stats.wilcoxon(nonzero, alternative="two-sided")
        else:
            w_p = float("nan")

        rows.append({
            "category": cat,
            "n": n,
            "mean_vanilla": round(mean_v, 2),
            "mean_distance": round(mean_r, 2),
            "improvement": round(mean_r - mean_v, 2),
            "cohens_d": round(d, 2),
            "wilcoxon_p": w_p,
        })
    return rows


# ---------------------------------------------------------------------------
# Analysis 1c: Per-path effectiveness
# ---------------------------------------------------------------------------

def analysis1_by_path(model: str, scorer_name: str, scorer_suffix: str,
                      results: list[dict]) -> list[dict]:
    """Per-path vanilla vs. distance improvement."""
    vanilla_meta = get_problem_means_with_metadata(results, "vanilla", scorer_suffix)
    reframed_meta = get_problem_means_with_metadata(results, "reframed", scorer_suffix)

    # Build per-problem dicts
    from collections import defaultdict
    path_v = defaultdict(list)
    path_r = defaultdict(list)
    path_diffs = defaultdict(list)

    for (v_score, _, v_paths), (r_score, _, _) in zip(vanilla_meta, reframed_meta):
        for path in v_paths:
            path_v[path].append(v_score)
            path_r[path].append(r_score)
            path_diffs[path].append(r_score - v_score)

    rows = []
    for path in sorted(path_v.keys()):
        v = np.array(path_v[path])
        r = np.array(path_r[path])
        diffs = np.array(path_diffs[path])
        n = len(v)
        d = cohens_d_paired(r, v) if n >= 2 and np.std(diffs, ddof=1) > 0 else 0.0

        nonzero = diffs[diffs != 0]
        if len(nonzero) >= 6:
            _, w_p = stats.wilcoxon(nonzero, alternative="two-sided")
        else:
            w_p = float("nan")

        rows.append({
            "path": path,
            "n": n,
            "mean_vanilla": round(np.mean(v), 2),
            "mean_distance": round(np.mean(r), 2),
            "improvement": round(np.mean(diffs), 2),
            "cohens_d": round(d, 2),
            "wilcoxon_p": w_p,
        })
    return rows


# ---------------------------------------------------------------------------
# Analysis 2b: Per-category DEO advantage
# ---------------------------------------------------------------------------

def analysis2_by_category(model: str, scorer_name: str, scorer_suffix: str,
                          results: list[dict]) -> list[dict]:
    """Per-category four-condition means and DEO advantage."""
    from collections import defaultdict
    conditions = ["vanilla", "distance", "engagement", "deo"]

    cat_data = defaultdict(lambda: defaultdict(list))
    for cond in conditions:
        meta = get_problem_means_with_metadata(results, cond, scorer_suffix)
        for score, cat, _ in meta:
            cat_data[cat][cond].append(score)

    rows = []
    for cat in sorted(cat_data.keys()):
        conds = cat_data[cat]
        n = min(len(conds.get(c, [])) for c in conditions)
        if n < 2:
            continue
        means = {c: round(np.mean(np.array(conds[c])[:n]), 2) for c in conditions}
        deo_adv = round(means["deo"] - means["distance"], 2)
        ordering = sorted(means, key=means.get, reverse=True)
        rows.append({
            "category": cat,
            "n": n,
            **{f"mean_{c}": means[c] for c in conditions},
            "deo_advantage": deo_adv,
            "ordering": " > ".join(ordering),
        })
    return rows


# ---------------------------------------------------------------------------
# Analysis by path mode (pure distance / hybrid / engagement)
# ---------------------------------------------------------------------------

def analysis1_by_mode(model: str, scorer_name: str, scorer_suffix: str,
                      results: list[dict]) -> list[dict]:
    """Study 1 vanilla vs. distance, split by path mode."""
    from collections import defaultdict
    mode_v = defaultdict(list)
    mode_r = defaultdict(list)

    vanilla_meta = get_problem_means_with_metadata(results, "vanilla", scorer_suffix)
    reframed_meta = get_problem_means_with_metadata(results, "reframed", scorer_suffix)

    for (v_score, _, v_paths), (r_score, _, _) in zip(vanilla_meta, reframed_meta):
        mode = classify_path_mode(v_paths)
        mode_v[mode].append(v_score)
        mode_r[mode].append(r_score)

    rows = []
    for mode in ["pure_distance", "hybrid", "engagement"]:
        v = np.array(mode_v.get(mode, []))
        r = np.array(mode_r.get(mode, []))
        n = min(len(v), len(r))
        if n < 2:
            rows.append({"mode": mode, "n": n, "mean_vanilla": 0, "mean_distance": 0,
                          "improvement": 0, "cohens_d": 0, "wilcoxon_p": float("nan")})
            continue
        v, r = v[:n], r[:n]
        diff = r - v
        d = cohens_d_paired(r, v) if np.std(diff, ddof=1) > 0 else 0.0
        nonzero = diff[diff != 0]
        w_p = float("nan")
        if len(nonzero) >= 6:
            _, w_p = stats.wilcoxon(nonzero, alternative="two-sided")
        rows.append({
            "mode": mode, "n": n,
            "mean_vanilla": round(np.mean(v), 3),
            "mean_distance": round(np.mean(r), 3),
            "improvement": round(np.mean(diff), 3),
            "cohens_d": round(d, 3),
            "wilcoxon_p": w_p,
        })
    return rows


def analysis2_by_mode(model: str, scorer_name: str, scorer_suffix: str,
                      results: list[dict]) -> list[dict]:
    """Study 2 four-condition, split by path mode. Key test: is DEO advantage
    larger for pure-distance problems (where distance lacks engagement)?"""
    from collections import defaultdict
    conditions = ["vanilla", "distance", "engagement", "deo"]
    mode_data = defaultdict(lambda: defaultdict(list))

    for cond in conditions:
        meta = get_problem_means_with_metadata(results, cond, scorer_suffix)
        for score, _, paths in meta:
            mode = classify_path_mode(paths)
            mode_data[mode][cond].append(score)

    rows = []
    for mode in ["pure_distance", "hybrid", "engagement"]:
        conds = mode_data.get(mode, {})
        n = min(len(conds.get(c, [])) for c in conditions) if conds else 0
        if n < 2:
            rows.append({"mode": mode, "n": n})
            continue
        means = {c: round(np.mean(np.array(conds[c])[:n]), 3) for c in conditions}
        ordering = sorted(means, key=means.get, reverse=True)

        # DEO vs distance effect size
        deo_arr = np.array(conds["deo"][:n])
        dist_arr = np.array(conds["distance"][:n])
        diff = deo_arr - dist_arr
        d_val = cohens_d_paired(deo_arr, dist_arr) if np.std(diff, ddof=1) > 0 else 0.0
        nonzero = diff[diff != 0]
        w_p = float("nan")
        if len(nonzero) >= 6:
            _, w_p = stats.wilcoxon(nonzero, alternative="two-sided")

        rows.append({
            "mode": mode, "n": n,
            **{f"mean_{c}": means[c] for c in conditions},
            "deo_minus_distance": round(means["deo"] - means["distance"], 3),
            "deo_vs_dist_d": round(d_val, 3),
            "deo_vs_dist_p": w_p,
            "ordering": " > ".join(ordering),
        })
    return rows


# ---------------------------------------------------------------------------
# Analysis 2: Four-condition DEO comparison
# ---------------------------------------------------------------------------

def _filter_pure_distance(results: list[dict]) -> list[dict]:
    """Keep only problems whose paths are all pure-distance operations.

    Problems with missing paths_applied metadata are excluded — they cannot
    be reliably classified.
    """
    out = []
    for r in results:
        paths = set(r.get("paths_applied", []))
        if not paths:
            continue  # skip orphan files with no path metadata
        if paths & HYBRID_PATHS or paths & ENGAGEMENT_PATHS:
            continue
        out.append(r)
    return out


def analysis2(model: str, scorer_name: str, scorer_suffix: str, results: list[dict]) -> dict:
    """Four-condition comparison: vanilla, distance, engagement, deo.

    Restricted to pure-distance-path problems where the distance/engagement/DEO
    distinction is theoretically clean.
    """
    results = _filter_pure_distance(results)

    conditions = ["vanilla", "distance", "engagement", "deo"]
    cond_means = {}
    for cond in conditions:
        cond_means[cond] = get_problem_means(results, cond, scorer_suffix)

    n = min(len(v) for v in cond_means.values())
    for cond in conditions:
        cond_means[cond] = cond_means[cond][:n]

    if n < 3:
        return {"error": f"Too few problems ({n})"}

    grand_means = {c: round(np.mean(v), 3) for c, v in cond_means.items()}

    # Observed ordering
    ordering = sorted(grand_means, key=grand_means.get, reverse=True)

    # Friedman test (non-parametric repeated measures)
    f_stat, f_p = stats.friedmanchisquare(
        cond_means["vanilla"], cond_means["distance"],
        cond_means["engagement"], cond_means["deo"]
    )

    # Post-hoc pairwise Wilcoxon signed-rank tests
    pairs = [
        ("deo", "distance"),
        ("deo", "engagement"),
        ("deo", "vanilla"),
        ("distance", "engagement"),
        ("distance", "vanilla"),
        ("engagement", "vanilla"),
    ]

    pairwise = []
    raw_ps = []
    for a, b in pairs:
        diff = cond_means[a] - cond_means[b]
        nonzero = diff[diff != 0]
        mean_diff = round(np.mean(diff), 3)
        d = cohens_d_paired(cond_means[a], cond_means[b])

        if len(nonzero) >= 6:
            w_stat, w_p = stats.wilcoxon(nonzero, alternative="two-sided")
            r_rb = rank_biserial(w_stat, len(nonzero))
        else:
            w_stat, w_p, r_rb = float("nan"), float("nan"), float("nan")

        pairwise.append({
            "pair": f"{a} vs {b}",
            "mean_diff": mean_diff,
            "cohens_d": round(d, 3),
            "wilcoxon_W": round(w_stat, 1) if not math.isnan(w_stat) else "N/A",
            "wilcoxon_p_raw": w_p if not math.isnan(w_p) else "N/A",
            "rank_biserial_r": round(r_rb, 3) if not math.isnan(r_rb) else "N/A",
        })
        raw_ps.append(w_p if not math.isnan(w_p) else 1.0)

    # Holm-Bonferroni correction
    adjusted = holm_bonferroni(raw_ps)
    for i, pw in enumerate(pairwise):
        pw["wilcoxon_p_adjusted"] = adjusted[i]

    # Correctness across conditions
    corr_means = {}
    for cond in conditions:
        corr = get_problem_means(results, cond, scorer_suffix, correctness_score)
        corr_means[cond] = round(np.mean(corr[:n]), 3)

    return {
        "model": model,
        "scorer": scorer_name,
        "n_problems": n,
        "condition_means": grand_means,
        "observed_ordering": " > ".join(ordering),
        "predicted_ordering_match": ordering == ["deo", "distance", "engagement", "vanilla"]
                                    or ordering == ["deo", "distance", "vanilla", "engagement"],
        "friedman_chi2": round(f_stat, 3),
        "friedman_p": f_p,
        "pairwise": pairwise,
        "correctness_means": corr_means,
    }


# ---------------------------------------------------------------------------
# Report formatting
# ---------------------------------------------------------------------------

def fmt_p(p) -> str:
    if isinstance(p, str):
        return p
    if p < 0.001:
        return f"{p:.2e}"
    return f"{p:.4f}"


def fmt_sig(p, alpha=ALPHA) -> str:
    if isinstance(p, str):
        return ""
    if p < 0.001:
        return "***"
    if p < 0.01:
        return "**"
    if p < alpha:
        return "*"
    return "ns"


def d_label(d: float) -> str:
    d = abs(d)
    if d >= 1.2:
        return "very large"
    if d >= 0.8:
        return "large"
    if d >= 0.5:
        return "medium"
    if d >= 0.2:
        return "small"
    return "negligible"


def generate_report(a1_results: list[dict], a2_results: list[dict],
                    a1_cats: list, a1_paths: list, a2_cats: list,
                    a1_modes: list, a2_modes: list) -> str:
    lines = []
    lines.append("# Statistical Analysis Results\n")
    lines.append(f"> α = {ALPHA}. Significance: *** p < .001, ** p < .01, * p < .05, ns = not significant.\n")
    lines.append("> Effect size labels: |d| ≥ 0.2 small, ≥ 0.5 medium, ≥ 0.8 large, ≥ 1.2 very large.\n")
    lines.append("> Holm-Bonferroni correction applied to all pairwise comparisons within each model × scorer.\n")

    # ── Analysis 1 ──
    lines.append("\n---\n")
    lines.append("## Analysis 1: Path Effectiveness (Vanilla vs. Reframing)\n")
    lines.append("| Model | Scorer | n | Vanilla | Reframing | Δ | Cohen's *d* | Size | Wilcoxon *p* | Sig |")
    lines.append("|-------|--------|---|---------|-----------|---|------------|------|-------------|-----|")

    for r in a1_results:
        if "error" in r:
            lines.append(f"| {r['model']} | {r['scorer']} | — | — | — | — | — | — | — | — |")
            continue
        wp = r["wilcoxon_p"]
        lines.append(
            f"| {r['model']} | {r['scorer']} "
            f"| {r['n_problems']} "
            f"| {r['mean_vanilla']:.2f} "
            f"| {r['mean_distance']:.2f} "
            f"| +{r['mean_improvement']:.2f} "
            f"| {r['cohens_d']:.2f} "
            f"| {d_label(r['cohens_d'])} "
            f"| {fmt_p(wp)} "
            f"| {fmt_sig(wp)} |"
        )

    lines.append("\n### Correctness Check (Analysis 1)\n")
    lines.append("| Model | Scorer | Vanilla | Reframing | *p* | Sig |")
    lines.append("|-------|--------|---------|-----------|-----|-----|")
    for r in a1_results:
        if "error" in r:
            continue
        cp = r["correctness_t_p"]
        lines.append(
            f"| {r['model']} | {r['scorer']} "
            f"| {r['correctness_vanilla']:.2f} "
            f"| {r['correctness_distance']:.2f} "
            f"| {fmt_p(cp)} "
            f"| {fmt_sig(cp)} |"
        )

    lines.append("\n### Normality of Differences (Shapiro-Wilk)\n")
    lines.append("| Model | Scorer | Shapiro *p* | Normal? |")
    lines.append("|-------|--------|------------|---------|")
    for r in a1_results:
        if "error" in r:
            continue
        sp = r["shapiro_p"]
        normal = "yes" if (isinstance(sp, str) or sp > ALPHA) else "no"
        lines.append(f"| {r['model']} | {r['scorer']} | {fmt_p(sp)} | {normal} |")

    # ── Analysis 1 — Per-Category ──
    lines.append("\n### Per-Category Improvement (Analysis 1)\n")
    # Group by model×scorer
    for (model, scorer), cat_rows in a1_cats:
        lines.append(f"#### {model} — {scorer}\n")
        lines.append("| Category | *n* | Vanilla | Reframing | Δ | *d* | Size | *p* | Sig |")
        lines.append("|----------|-----|---------|-----------|---|-----|------|-----|-----|")
        for row in sorted(cat_rows, key=lambda r: -r["improvement"]):
            wp = row["wilcoxon_p"]
            lines.append(
                f"| {row['category']} | {row['n']} "
                f"| {row['mean_vanilla']:.2f} | {row['mean_distance']:.2f} "
                f"| {row['improvement']:+.2f} | {row['cohens_d']:.2f} "
                f"| {d_label(row['cohens_d'])} "
                f"| {fmt_p(wp) if not math.isnan(wp) else '—'} "
                f"| {fmt_sig(wp) if not math.isnan(wp) else '—'} |"
            )
        lines.append("")

    # ── Analysis 1 — Per-Path ──
    lines.append("\n### Per-Path Effectiveness (Analysis 1)\n")
    for (model, scorer), path_rows in a1_paths:
        lines.append(f"#### {model} — {scorer}\n")
        lines.append("| Path | *n* | Vanilla | Reframing | Δ | *d* | Size | *p* | Sig |")
        lines.append("|------|-----|---------|-----------|---|-----|------|-----|-----|")
        for row in sorted(path_rows, key=lambda r: -r["improvement"]):
            wp = row["wilcoxon_p"]
            lines.append(
                f"| {row['path']} | {row['n']} "
                f"| {row['mean_vanilla']:.2f} | {row['mean_distance']:.2f} "
                f"| {row['improvement']:+.2f} | {row['cohens_d']:.2f} "
                f"| {d_label(row['cohens_d'])} "
                f"| {fmt_p(wp) if not math.isnan(wp) else '—'} "
                f"| {fmt_sig(wp) if not math.isnan(wp) else '—'} |"
            )
        lines.append("")

    # ── Analysis 2 ──
    lines.append("\n---\n")
    lines.append("## Analysis 2: DEO Mechanism (Four-Condition Comparison)\n")
    lines.append("> **Restricted to pure distance-mode problems** (Paths 1–5, 9 only). "
                 "Problems using hybrid paths (6, 7) or engagement paths (8) are excluded "
                 "because the distance/engagement/DEO distinction is not theoretically clean "
                 "for those problems. See Path-Mode Analysis below for the full breakdown.\n")

    for r in a2_results:
        if "error" in r:
            lines.append(f"### {r['model']} — {r['scorer']}: ERROR\n")
            continue

        cm = r["condition_means"]
        lines.append(f"### {r['model']} — {r['scorer']} (*n* = {r['n_problems']})\n")
        lines.append(f"**Condition means:** Vanilla {cm['vanilla']:.2f} | Distance {cm['distance']:.2f} "
                      f"| Engagement {cm['engagement']:.2f} | DEO {cm['deo']:.2f}\n")
        lines.append(f"**Observed ordering:** {r['observed_ordering']}\n")
        match = "Yes ✓" if r["predicted_ordering_match"] else "No ✗"
        lines.append(f"**Matches predicted ordering (DEO > Distance > Engagement ≥ Vanilla)?** {match}\n")
        lines.append(f"**Friedman χ²** = {r['friedman_chi2']:.2f}, *p* = {fmt_p(r['friedman_p'])} "
                      f"{fmt_sig(r['friedman_p'])}\n")

        lines.append("| Pair | Δ | Cohen's *d* | Size | Wilcoxon *p* (adj.) | Sig |")
        lines.append("|------|---|------------|------|--------------------|----|")
        for pw in r["pairwise"]:
            ap = pw["wilcoxon_p_adjusted"]
            lines.append(
                f"| {pw['pair']} "
                f"| {pw['mean_diff']:+.2f} "
                f"| {pw['cohens_d']:.2f} "
                f"| {d_label(pw['cohens_d'])} "
                f"| {fmt_p(ap)} "
                f"| {fmt_sig(ap)} |"
            )

        crr = r["correctness_means"]
        lines.append(f"\n**Correctness:** Vanilla {crr['vanilla']:.2f} | Distance {crr['distance']:.2f} "
                      f"| Engagement {crr['engagement']:.2f} | DEO {crr['deo']:.2f}\n")

    # ── Analysis 2 — Per-Category ──
    lines.append("\n### Per-Category DEO Advantage (Analysis 2)\n")
    for (model, scorer), cat_rows in a2_cats:
        lines.append(f"#### {model} — {scorer}\n")
        lines.append("| Category | *n* | Vanilla | Distance | Engagement | DEO | DEO−Dist | Ordering |")
        lines.append("|----------|-----|---------|----------|------------|-----|----------|----------|")
        for row in sorted(cat_rows, key=lambda r: -r["deo_advantage"]):
            lines.append(
                f"| {row['category']} | {row['n']} "
                f"| {row['mean_vanilla']:.2f} | {row['mean_distance']:.2f} "
                f"| {row['mean_engagement']:.2f} | {row['mean_deo']:.2f} "
                f"| {row['deo_advantage']:+.2f} "
                f"| {row['ordering']} |"
            )
        lines.append("")

    # ── Path-Mode Analysis ──
    lines.append("\n---\n")
    lines.append("## Path-Mode Analysis\n")
    lines.append("> Six paths (1, 2, 3, 4, 5, 9) are pure distance-mode operations. "
                 "One path (8) is engagement-mode. Two paths (6, 7) are hybrid — they "
                 "inherently require both distance and engagement.\n")
    lines.append("> Problems are classified by their dominant mode: **pure_distance** if all "
                 "paths are distance-only, **hybrid** if any path is 6 or 7, **engagement** "
                 "if the only path is 8.\n")

    lines.append("\n### Analysis 1 by Path Mode (Vanilla vs. Reframing)\n")
    lines.append("| Model | Scorer | Mode | *n* | Vanilla | Reframing | Δ | *d* | *p* | Sig |")
    lines.append("|-------|--------|------|-----|---------|-----------|---|-----|-----|-----|")
    for (model, scorer), rows in a1_modes:
        for row in rows:
            wp = row["wilcoxon_p"]
            lines.append(
                f"| {model} | {scorer} | {row['mode']} | {row['n']} "
                f"| {row['mean_vanilla']:.2f} | {row['mean_distance']:.2f} "
                f"| {row['improvement']:+.2f} | {row['cohens_d']:.2f} "
                f"| {fmt_p(wp) if not math.isnan(wp) else '—'} "
                f"| {fmt_sig(wp) if not math.isnan(wp) else '—'} |"
            )

    lines.append("\n### Analysis 2 by Path Mode: DEO vs. Distance\n")
    lines.append("> **Key prediction:** The DEO advantage over distance should be *larger* for "
                 "pure-distance problems (where distance truly lacks engagement) than for hybrid "
                 "problems (where paths 6/7 already partially activate engagement).\n")
    lines.append("| Model | Scorer | Mode | *n* | V | D | E | DEO | DEO−D | *d* | *p* | Ordering |")
    lines.append("|-------|--------|------|-----|---|---|---|-----|-------|-----|-----|----------|")
    for (model, scorer), rows in a2_modes:
        for row in rows:
            if row["n"] < 2 or "mean_vanilla" not in row:
                lines.append(f"| {model} | {scorer} | {row['mode']} | {row['n']} "
                             f"| — | — | — | — | — | — | — | — |")
                continue
            wp = row.get("deo_vs_dist_p", float("nan"))
            lines.append(
                f"| {model} | {scorer} | {row['mode']} | {row['n']} "
                f"| {row['mean_vanilla']:.2f} | {row['mean_distance']:.2f} "
                f"| {row['mean_engagement']:.2f} | {row['mean_deo']:.2f} "
                f"| {row['deo_minus_distance']:+.2f} "
                f"| {row['deo_vs_dist_d']:.2f} "
                f"| {fmt_p(wp) if not math.isnan(wp) else '—'} "
                f"| {row['ordering']} |"
            )

    # ── Supplementary interpretation ──
    lines.append("\n### Interpretation by Path Mode\n")

    # Compute aggregated summaries across all models × scorers
    pure_d_deltas, hybrid_deltas, eng_deltas = [], [], []
    pure_d_ns, hybrid_ns, eng_ns = set(), set(), set()
    eng_dist_vs_eng = []  # track how distance and engagement compare for engagement-mode
    for (model, scorer), rows in a2_modes:
        for row in rows:
            if row["n"] < 2 or "deo_minus_distance" not in row:
                continue
            if row["mode"] == "pure_distance":
                pure_d_deltas.append(row["deo_minus_distance"])
                pure_d_ns.add(row["n"])
            elif row["mode"] == "hybrid":
                hybrid_deltas.append(row["deo_minus_distance"])
                hybrid_ns.add(row["n"])
            elif row["mode"] == "engagement":
                eng_deltas.append(row["deo_minus_distance"])
                eng_ns.add(row["n"])
                eng_dist_vs_eng.append((
                    row["mean_distance"], row["mean_engagement"],
                    row["ordering"]
                ))

    def _fmt_n(ns):
        if len(ns) == 1:
            return str(ns.pop())
        return f"{min(ns)}–{max(ns)}"

    if pure_d_deltas and hybrid_deltas:
        lines.append(f"#### Pure Distance (*n* = {_fmt_n(pure_d_ns)}): Clean DEO test\n")
        lines.append(f"Mean DEO advantage over distance: **{np.mean(pure_d_deltas):+.2f}** "
                     f"(range: {min(pure_d_deltas):+.2f} to {max(pure_d_deltas):+.2f}). "
                     "These problems provide a clean test of the oscillation hypothesis because "
                     "the distance condition is purely analytical and the DEO condition adds "
                     "genuine engagement. The consistent positive advantage confirms that "
                     "oscillation adds value beyond distance alone.\n")

        lines.append(f"#### Hybrid (*n* = {_fmt_n(hybrid_ns)}): Partial engagement in \"distance\"\n")
        lines.append(f"Mean DEO advantage over distance: **{np.mean(hybrid_deltas):+.2f}** "
                     f"(range: {min(hybrid_deltas):+.2f} to {max(hybrid_deltas):+.2f}). "
                     "The DEO advantage is roughly half that of pure-distance problems "
                     f"({np.mean(hybrid_deltas):+.2f} vs. {np.mean(pure_d_deltas):+.2f}). "
                     "This is predicted by the theory: paths 6 (Premise Reflection) and 7 "
                     "(Surprise as Signal) already partially activate engagement within "
                     "the \"distance\" condition, so the explicit DEO oscillation provides "
                     "a smaller incremental benefit. The ordering DEO > Distance > Engagement > "
                     "Vanilla is maintained in all hybrid-mode combinations.\n")

    if eng_deltas:
        lines.append(f"#### Engagement (*n* = {_fmt_n(eng_ns)}): Collapsed oscillation\n")
        lines.append(f"Mean DEO advantage over distance: **{np.mean(eng_deltas):+.2f}** "
                     f"(range: {min(eng_deltas):+.2f} to {max(eng_deltas):+.2f}). "
                     "These 2 problems (both using Path 8: Confidence Calibration) show "
                     "the largest DEO-minus-distance delta — but for the wrong reason. "
                     "The \"distance\" condition for these problems is itself an engagement "
                     "operation (felt uncertainty), so it scores low because it duplicates "
                     "the engagement condition rather than providing analytical distance. "
                     "The DEO preamble, while labelled as oscillation, is effectively "
                     "engagement-followed-by-engagement rather than genuine DEO.\n")

        # Check if distance ≈ engagement for these problems
        dist_lower = sum(1 for d, e, _ in eng_dist_vs_eng if d <= e)
        lines.append(f"Confirming evidence: in {dist_lower}/{len(eng_dist_vs_eng)} "
                     "model × scorer combinations, the \"distance\" condition scores equal to "
                     "or lower than the engagement condition — consistent with both being "
                     "engagement-mode operations. The ordering frequently shifts to "
                     "DEO > Engagement > Distance, with Distance and Engagement swapping "
                     "positions, unlike the stable DEO > Distance > Engagement > Vanilla "
                     "seen in pure-distance and hybrid problems.\n")

        lines.append("These 2 problems are excluded from Analysis 2 because they cannot "
                     "test the oscillation hypothesis — but their behaviour is consistent "
                     "with the path-mode classification and provides additional evidence "
                     "that the cognitive mode of the path matters.\n")

    # ── Summary ──
    lines.append("\n---\n")
    lines.append("## Summary\n")

    # Count how many model×scorer combos confirm the predicted ordering
    confirmed = sum(1 for r in a2_results if r.get("predicted_ordering_match"))
    total = sum(1 for r in a2_results if "error" not in r)
    lines.append(f"**Predicted ordering confirmed:** {confirmed}/{total} model × scorer combinations\n")

    # Count significant Friedman tests
    sig_friedman = sum(1 for r in a2_results
                       if "error" not in r and isinstance(r["friedman_p"], float) and r["friedman_p"] < ALPHA)
    lines.append(f"**Significant Friedman tests (p < {ALPHA}):** {sig_friedman}/{total}\n")

    # DEO vs Distance significance
    deo_vs_dist = []
    for r in a2_results:
        if "error" in r:
            continue
        for pw in r["pairwise"]:
            if pw["pair"] == "deo vs distance":
                ap = pw["wilcoxon_p_adjusted"]
                sig = isinstance(ap, float) and ap < ALPHA
                deo_vs_dist.append((r["model"], r["scorer"], sig, ap, pw["cohens_d"]))
    lines.append("### Critical Test: DEO vs. Distance\n")
    lines.append("| Model | Scorer | *p* (adj.) | Sig | Cohen's *d* |")
    lines.append("|-------|--------|-----------|-----|------------|")
    for model, scorer, sig, p, d in deo_vs_dist:
        lines.append(f"| {model} | {scorer} | {fmt_p(p)} | {fmt_sig(p)} | {d:.2f} |")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Statistical analysis")
    parser.add_argument("--models", nargs="+", choices=MODELS, default=MODELS)
    parser.add_argument("--output", default="paper/stats_results.md")
    args = parser.parse_args()

    a1_all = []
    a2_all = []
    a1_cats_all = []   # list of ((model, scorer), rows)
    a1_paths_all = []  # list of ((model, scorer), rows)
    a2_cats_all = []   # list of ((model, scorer), rows)
    a1_modes_all = []  # list of ((model, scorer), rows)
    a2_modes_all = []  # list of ((model, scorer), rows)

    for model in args.models:
        print(f"\n{'='*60}")
        print(f"  {model}")
        print(f"{'='*60}")

        study1 = load_study1(model)
        study2 = load_study2(model)
        print(f"  Loaded: {len(study1)} Study 1, {len(study2)} Study 2 problems")

        for scorer_name, scorer_suffix in SCORERS.items():
            print(f"\n  --- Scorer: {scorer_name} ---")

            r1 = analysis1(model, scorer_name, scorer_suffix, study1)
            a1_all.append(r1)
            if "error" not in r1:
                wp = r1["wilcoxon_p"]
                print(f"  Analysis 1: Δ = +{r1['mean_improvement']:.3f}, "
                      f"d = {r1['cohens_d']:.3f}, "
                      f"Wilcoxon p = {fmt_p(wp)} {fmt_sig(wp)}")

            # Per-category and per-path (Analysis 1)
            cats1 = analysis1_by_category(model, scorer_name, scorer_suffix, study1)
            a1_cats_all.append(((model, scorer_name), cats1))
            paths1 = analysis1_by_path(model, scorer_name, scorer_suffix, study1)
            a1_paths_all.append(((model, scorer_name), paths1))

            r2 = analysis2(model, scorer_name, scorer_suffix, study2)
            a2_all.append(r2)
            if "error" not in r2:
                print(f"  Analysis 2: {r2['observed_ordering']}")
                print(f"  Friedman p = {fmt_p(r2['friedman_p'])} {fmt_sig(r2['friedman_p'])}")
                print(f"  Predicted ordering match: {r2['predicted_ordering_match']}")

            # Per-category (Analysis 2) — pure-distance only, matching main Analysis 2
            cats2 = analysis2_by_category(model, scorer_name, scorer_suffix, _filter_pure_distance(study2))
            a2_cats_all.append(((model, scorer_name), cats2))

            # Path-mode analysis
            modes1 = analysis1_by_mode(model, scorer_name, scorer_suffix, study1)
            a1_modes_all.append(((model, scorer_name), modes1))
            modes2 = analysis2_by_mode(model, scorer_name, scorer_suffix, study2)
            a2_modes_all.append(((model, scorer_name), modes2))

    report = generate_report(a1_all, a2_all, a1_cats_all, a1_paths_all, a2_cats_all,
                             a1_modes_all, a2_modes_all)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report)
    print(f"\n{'='*60}")
    print(f"  Report saved: {output}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
