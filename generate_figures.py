"""Generate publication-quality figures for the paper."""

import json
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

RESULTS_DIR = Path("results")
FIGURES_DIR = Path("paper/figures")
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

MODELS = ["llama", "qwen", "llama4scout"]
MODEL_LABELS = {"llama": "Llama 70B", "qwen": "Qwen 32B", "llama4scout": "Scout 17B"}
SCORERS = {"self": "", "claude": "_claude", "openai": "_openai"}
SCORER_LABELS = {"self": "Self", "claude": "Claude", "openai": "GPT-4.1"}

REFRAMING_DIMS = ["frame_diversity", "assumption_surfacing", "solution_novelty", "premise_questioning"]

PURE_DISTANCE_PATHS = {
    "path_1_name_the_frame", "path_2_decompose_to_generic", "path_3_distant_analogy",
    "path_4_incubate_reset", "path_5_invert", "path_9_step_outside",
}
HYBRID_PATHS = {"path_6_premise_reflection", "path_7_surprise_as_signal"}
ENGAGEMENT_PATHS = {"path_8_confidence_calibration"}

# Colours
C_VANILLA = "#94a3b8"
C_DISTANCE = "#3b82f6"
C_ENGAGEMENT = "#f97316"
C_DEO = "#10b981"
C_REFRAMING = "#6366f1"

# Style
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 300,
})


# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

def safe_score(score_dict, dim):
    if dim in score_dict and isinstance(score_dict[dim], dict):
        return score_dict[dim].get("score", 3)
    return 3


def reframing_score(score_dict):
    return sum(safe_score(score_dict, d) for d in REFRAMING_DIMS) / 4


def load_study1(model):
    raw = RESULTS_DIR / model / "raw"
    return [json.loads(p.read_text()) for p in sorted(raw.glob("*.json")) if not p.name.startswith("deo_")]


def load_study2(model):
    raw = RESULTS_DIR / model / "raw"
    results = []
    for p in sorted(raw.glob("deo_*.json")):
        d = json.loads(p.read_text())
        paths = set(d.get("paths_applied", []))
        if not paths:
            continue  # skip orphan files with no metadata
        if paths & HYBRID_PATHS or paths & ENGAGEMENT_PATHS:
            continue
        results.append(d)
    return results


def problem_means(results, condition, scorer_suffix):
    scores_key = f"{condition}{scorer_suffix}_scores"
    means = []
    for r in results:
        if scores_key not in r or not r[scores_key]:
            continue
        means.append(np.mean([reframing_score(s) for s in r[scores_key]]))
    return np.array(means)


def problem_means_with_paths(results, condition, scorer_suffix):
    scores_key = f"{condition}{scorer_suffix}_scores"
    out = []
    for r in results:
        if scores_key not in r or not r[scores_key]:
            continue
        mean = np.mean([reframing_score(s) for s in r[scores_key]])
        out.append((mean, r.get("paths_applied", [])))
    return out


# ---------------------------------------------------------------------------
# Figure 1: Analysis 1 — Vanilla vs. Reframing
# ---------------------------------------------------------------------------

def fig1_analysis1_overview():
    fig, axes = plt.subplots(1, 3, figsize=(10, 4), sharey=True)

    for ax, model in zip(axes, MODELS):
        data = load_study1(model)
        x = np.arange(len(SCORERS))
        width = 0.35
        v_means, r_means, v_sems, r_sems = [], [], [], []

        for scorer_name, suffix in SCORERS.items():
            v = problem_means(data, "vanilla", suffix)
            r = problem_means(data, "reframed", suffix)
            v_means.append(np.mean(v))
            r_means.append(np.mean(r))
            v_sems.append(np.std(v) / np.sqrt(len(v)))
            r_sems.append(np.std(r) / np.sqrt(len(r)))

        bars1 = ax.bar(x - width/2, v_means, width, yerr=v_sems, capsize=3,
                        label="Vanilla", color=C_VANILLA, edgecolor="white", linewidth=0.5)
        bars2 = ax.bar(x + width/2, r_means, width, yerr=r_sems, capsize=3,
                        label="Reframing", color=C_REFRAMING, edgecolor="white", linewidth=0.5)

        ax.set_title(MODEL_LABELS[model], fontweight="bold")
        ax.set_xticks(x)
        ax.set_xticklabels([SCORER_LABELS[s] for s in SCORERS])
        ax.set_ylim(0, 5)
        ax.set_ylabel("Reframing Score" if model == "llama" else "")

    axes[0].legend(frameon=False, loc="upper left")
    fig.suptitle("Analysis 1: Vanilla vs. Reframing (n = 50)", fontweight="bold", y=1.02)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "fig1_analysis1_overview.png", bbox_inches="tight")
    fig.savefig(FIGURES_DIR / "fig1_analysis1_overview.pdf", bbox_inches="tight")
    plt.close(fig)
    print("  Fig 1 saved")


# ---------------------------------------------------------------------------
# Figure 2: Analysis 2 — Four conditions (pure-distance only)
# ---------------------------------------------------------------------------

def fig2_analysis2_conditions():
    conditions = ["vanilla", "distance", "engagement", "deo"]
    cond_labels = ["Vanilla", "Distance", "Engagement", "DEO"]
    cond_colors = [C_VANILLA, C_DISTANCE, C_ENGAGEMENT, C_DEO]

    fig, axes = plt.subplots(1, 3, figsize=(10, 4), sharey=True)

    for ax, model in zip(axes, MODELS):
        data = load_study2(model)
        x = np.arange(len(SCORERS))
        n_conds = len(conditions)
        width = 0.18

        for ci, (cond, color) in enumerate(zip(conditions, cond_colors)):
            means, sems = [], []
            for scorer_name, suffix in SCORERS.items():
                vals = problem_means(data, cond, suffix)
                means.append(np.mean(vals))
                sems.append(np.std(vals) / np.sqrt(len(vals)))
            offset = (ci - (n_conds - 1) / 2) * width
            ax.bar(x + offset, means, width, yerr=sems, capsize=2,
                   label=cond_labels[ci] if model == "llama" else "",
                   color=color, edgecolor="white", linewidth=0.5)

        ax.set_title(MODEL_LABELS[model], fontweight="bold")
        ax.set_xticks(x)
        ax.set_xticklabels([SCORER_LABELS[s] for s in SCORERS])
        ax.set_ylim(0, 5)
        ax.set_ylabel("Reframing Score" if model == "llama" else "")

    axes[0].legend(frameon=False, loc="upper left", fontsize=8)
    fig.suptitle("Analysis 2: Four Conditions — Pure Distance Problems (n = 20)",
                 fontweight="bold", y=1.02)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "fig2_analysis2_conditions.png", bbox_inches="tight")
    fig.savefig(FIGURES_DIR / "fig2_analysis2_conditions.pdf", bbox_inches="tight")
    plt.close(fig)
    print("  Fig 2 saved")


# ---------------------------------------------------------------------------
# Figure 3: Forest plot — DEO vs. Distance effect sizes
# ---------------------------------------------------------------------------

def fig3_deo_vs_distance_forest():
    from scipy import stats

    labels = []
    ds = []
    ci_lows = []
    ci_highs = []
    ps = []

    for model in MODELS:
        data = load_study2(model)
        for scorer_name, suffix in SCORERS.items():
            deo = problem_means(data, "deo", suffix)
            dist = problem_means(data, "distance", suffix)
            n = min(len(deo), len(dist))
            deo, dist = deo[:n], dist[:n]
            diff = deo - dist
            sd = np.std(diff, ddof=1)
            d = np.mean(diff) / sd if sd > 0 else 0

            # CI for d using noncentral t approximation
            se_d = np.sqrt(1/n + d**2 / (2*n))
            ci_low = d - 1.96 * se_d
            ci_high = d + 1.96 * se_d

            _, w_p = stats.wilcoxon(diff[diff != 0], alternative="two-sided") if np.sum(diff != 0) >= 6 else (0, 1)

            labels.append(f"{MODEL_LABELS[model]} / {SCORER_LABELS[scorer_name]}")
            ds.append(d)
            ci_lows.append(ci_low)
            ci_highs.append(ci_high)
            ps.append(w_p)

    fig, ax = plt.subplots(figsize=(7, 5))
    y = np.arange(len(labels))[::-1]

    for i in range(len(labels)):
        color = C_DEO if ps[i] < 0.05 else "#94a3b8"
        ax.plot(ds[i], y[i], "o", color=color, markersize=8, zorder=3)
        ax.plot([ci_lows[i], ci_highs[i]], [y[i], y[i]], "-", color=color, linewidth=2, zorder=2)

    ax.axvline(0, color="#e2e8f0", linewidth=1, linestyle="--", zorder=1)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Cohen's d (DEO minus Distance)")
    ax.set_title("DEO vs. Distance: Effect Sizes with 95% CI", fontweight="bold")

    # Effect size reference lines
    for threshold, label in [(0.2, "small"), (0.5, "medium"), (0.8, "large")]:
        ax.axvline(threshold, color="#e2e8f0", linewidth=0.5, linestyle=":", zorder=1)
        ax.text(threshold, y[-1] - 0.8, label, ha="center", fontsize=7, color="#94a3b8")

    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "fig3_deo_vs_distance_forest.png", bbox_inches="tight")
    fig.savefig(FIGURES_DIR / "fig3_deo_vs_distance_forest.pdf", bbox_inches="tight")
    plt.close(fig)
    print("  Fig 3 saved")


# ---------------------------------------------------------------------------
# Figure 4: Per-path effectiveness
# ---------------------------------------------------------------------------

PATH_LABELS = {
    "path_1_name_the_frame": "P1: Name Frame",
    "path_2_decompose_to_generic": "P2: Decompose",
    "path_3_distant_analogy": "P3: Analogy",
    "path_4_incubate_reset": "P4: Incubate",
    "path_5_invert": "P5: Invert",
    "path_6_premise_reflection": "P6: Premise",
    "path_7_surprise_as_signal": "P7: Surprise",
    "path_8_confidence_calibration": "P8: Confidence",
    "path_9_step_outside": "P9: Step Outside",
}

PATH_MODE_COLORS = {
    "path_1_name_the_frame": C_DISTANCE,
    "path_2_decompose_to_generic": C_DISTANCE,
    "path_3_distant_analogy": C_DISTANCE,
    "path_4_incubate_reset": C_DISTANCE,
    "path_5_invert": C_DISTANCE,
    "path_6_premise_reflection": "#a855f7",  # purple for hybrid
    "path_7_surprise_as_signal": "#a855f7",
    "path_8_confidence_calibration": C_ENGAGEMENT,
    "path_9_step_outside": C_DISTANCE,
}


def fig4_per_path():
    # Average across all 3 models and 3 scorers
    path_improvements = defaultdict(list)

    for model in MODELS:
        data = load_study1(model)
        for scorer_name, suffix in SCORERS.items():
            v_meta = problem_means_with_paths(data, "vanilla", suffix)
            r_meta = problem_means_with_paths(data, "reframed", suffix)
            for (v_score, v_paths), (r_score, _) in zip(v_meta, r_meta):
                diff = r_score - v_score
                for path in v_paths:
                    path_improvements[path].append(diff)

    # Sort by mean improvement
    path_order = sorted(path_improvements, key=lambda p: np.mean(path_improvements[p]), reverse=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    y = np.arange(len(path_order))[::-1]

    for i, path in enumerate(path_order):
        vals = np.array(path_improvements[path])
        mean_imp = np.mean(vals)
        sem = np.std(vals) / np.sqrt(len(vals))
        color = PATH_MODE_COLORS.get(path, C_DISTANCE)
        ax.barh(y[i], mean_imp, xerr=sem, capsize=3, color=color,
                edgecolor="white", linewidth=0.5, height=0.6)
        ax.text(mean_imp + sem + 0.02, y[i], f"n={len(vals)//9}",
                va="center", fontsize=8, color="#64748b")

    ax.set_yticks(y)
    ax.set_yticklabels([PATH_LABELS.get(p, p) for p in path_order])
    ax.set_xlabel("Mean Improvement (Reframing minus Vanilla)")
    ax.set_title("Per-Path Effectiveness (averaged across models and scorers)", fontweight="bold")
    ax.axvline(0, color="#e2e8f0", linewidth=1, linestyle="--")

    # Legend for path modes
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=C_DISTANCE, label="Distance mode"),
        Patch(facecolor="#a855f7", label="Hybrid mode"),
        Patch(facecolor=C_ENGAGEMENT, label="Engagement mode"),
    ]
    ax.legend(handles=legend_elements, frameon=False, loc="lower right", fontsize=8)

    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "fig4_per_path_effectiveness.png", bbox_inches="tight")
    fig.savefig(FIGURES_DIR / "fig4_per_path_effectiveness.pdf", bbox_inches="tight")
    plt.close(fig)
    print("  Fig 4 saved")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Generating figures...")
    fig1_analysis1_overview()
    fig2_analysis2_conditions()
    fig3_deo_vs_distance_forest()
    fig4_per_path()
    print(f"\nAll figures saved to {FIGURES_DIR}/")
