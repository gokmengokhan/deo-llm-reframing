"""Report generator — creates a markdown comparison document.

Each problem follows the theory's own cycle:
  Lock-in → Disruption → The Path → Restructuring → The Shift
"""

import json
from pathlib import Path

from .config import RAW_DIR, RESULTS_DIR, SCORING_DIMENSIONS


def _avg_score(scores_list: list[dict], dimension: str) -> float:
    """Average score across runs for one dimension."""
    values = [s[dimension]["score"] for s in scores_list if dimension in s]
    return round(sum(values) / len(values), 2) if values else 0.0


def _reframing_score(scores_list: list[dict]) -> float:
    """Average of the 4 reframing dimensions (excluding correctness)."""
    dims = ["frame_diversity", "assumption_surfacing", "solution_novelty", "premise_questioning"]
    values = []
    for s in scores_list:
        for d in dims:
            if d in s:
                values.append(s[d]["score"])
    return round(sum(values) / len(values), 2) if values else 0.0


def _truncate(text: str, max_lines: int = 30) -> str:
    """Truncate long responses for the report."""
    lines = text.strip().split("\n")
    if len(lines) <= max_lines:
        return text.strip()
    return "\n".join(lines[:max_lines]) + f"\n\n*[... truncated, {len(lines)} lines total]*"


PATH_LABELS = {
    "path_1_name_the_frame": "Path 1: Name the Frame",
    "path_2_decompose_to_generic": "Path 2: Decompose to Generic",
    "path_3_distant_analogy": "Path 3: Bridge the Distant Analogy",
    "path_4_incubate": "Path 4: Incubate Deliberately",
    "path_5_invert": "Path 5: Invert the Problem",
    "path_6_premise_reflection": "Path 6: Reflect on the Premise",
    "path_7_surprise_as_signal": "Path 7: Use Surprise as Signal",
    "path_8_emotional_insight": "Path 8: Seek the Emotional Insight",
    "path_9_step_outside": "Path 9: Step Outside Yourself",
}

CATEGORY_LABELS = {
    "functional_fixedness": "Functional Fixedness",
    "framing_trap": "Framing Trap",
    "einstellung": "Einstellung / Mental Set",
    "false_binary": "Assumption-Laden / False Binary",
}


def generate_report(problem_ids: list[str] | None = None) -> str:
    """Generate the full markdown report from scored results."""
    # Load all scored results
    if problem_ids:
        paths = [RAW_DIR / f"{pid}.json" for pid in problem_ids]
    else:
        paths = sorted(RAW_DIR.glob("*.json"))

    results = []
    for p in paths:
        if p.exists():
            data = json.loads(p.read_text())
            if data.get("study") == "deo":
                continue  # Skip DEO files
            results.append(data)

    if not results:
        return "# No results found.\n\nRun the experiment first: `uv run python run_experiment.py`"

    has_scores = "vanilla_scores" in results[0]

    # --- Build report ---
    lines = []
    lines.append("# Perceptual Reframing for AI — Experiment Results")
    lines.append("")
    lines.append("> **Core claim:** The shift is a change in representation, not a change in information.")
    lines.append("> Same model, same knowledge, different frame — different output.")
    lines.append("")

    # Executive summary (only if scores exist)
    if has_scores:
        lines.append("## Executive Summary")
        lines.append("")
        lines.append("| Problem | Vanilla Reframing Score | Enhanced Reframing Score | Vanilla Correctness | Enhanced Correctness | Improvement |")
        lines.append("|---------|----------------------|------------------------|--------------------|--------------------|-------------|")

        total_v_rf = 0
        total_r_rf = 0
        count = 0

        for r in results:
            if "vanilla_scores" not in r:
                continue
            v_rf = _reframing_score(r["vanilla_scores"])
            r_rf = _reframing_score(r["reframed_scores"])
            v_c = _avg_score(r["vanilla_scores"], "correctness")
            r_c = _avg_score(r["reframed_scores"], "correctness")
            improvement = round(r_rf - v_rf, 2)
            sign = "+" if improvement > 0 else ""
            lines.append(
                f"| {r['problem_title']} | {v_rf} | {r_rf} | {v_c} | {r_c} | {sign}{improvement} |"
            )
            total_v_rf += v_rf
            total_r_rf += r_rf
            count += 1

        if count:
            avg_v = round(total_v_rf / count, 2)
            avg_r = round(total_r_rf / count, 2)
            avg_imp = round(avg_r - avg_v, 2)
            sign = "+" if avg_imp > 0 else ""
            lines.append(f"| **Average** | **{avg_v}** | **{avg_r}** | | | **{sign}{avg_imp}** |")
        lines.append("")

    # Per-problem narratives
    lines.append("---")
    lines.append("")
    lines.append("## Problem-by-Problem Analysis")
    lines.append("")

    for r in results:
        paths_display = ", ".join(PATH_LABELS.get(p, p) for p in r["paths_applied"])
        cat_display = CATEGORY_LABELS.get(r["category"], r["category"])

        lines.append(f"### {r['problem_title']}")
        lines.append(f"**Category:** {cat_display} | **Paths:** {paths_display}")
        lines.append("")

        # Theory connection
        lines.append(f"**Theory:** {r['theory_connection']}")
        lines.append("")

        # Lock-in: vanilla response (best run by reframing score if scored)
        lines.append("#### 1. Lock-In — The Vanilla Response")
        lines.append(f"*Expected failure:* {r['expected_vanilla_failure']}")
        lines.append("")
        vanilla_text = r["vanilla"][0]["response"]  # Use first run
        lines.append("```")
        lines.append(_truncate(vanilla_text))
        lines.append("```")
        lines.append("")

        # The path
        lines.append(f"#### 2. The Reframing Strategy")
        lines.append(f"Applied: **{paths_display}**")
        lines.append("")

        # Restructuring: reframed response
        lines.append("#### 3. Restructuring — The Reframed Response")
        lines.append(f"*Success criteria:* {r['success_criteria']}")
        lines.append("")
        reframed_text = r["reframed"][0]["response"]
        lines.append("```")
        lines.append(_truncate(reframed_text))
        lines.append("```")
        lines.append("")

        # Scores comparison (if available)
        if has_scores and "vanilla_scores" in r:
            lines.append("#### 4. Score Comparison")
            lines.append("")
            lines.append("| Dimension | Vanilla | Reframed | Delta |")
            lines.append("|-----------|---------|----------|-------|")
            for dim in SCORING_DIMENSIONS:
                v = _avg_score(r["vanilla_scores"], dim)
                rf = _avg_score(r["reframed_scores"], dim)
                delta = round(rf - v, 2)
                sign = "+" if delta > 0 else ""
                lines.append(f"| {dim.replace('_', ' ').title()} | {v} | {rf} | {sign}{delta} |")
            lines.append("")

        lines.append("---")
        lines.append("")

    # Footer
    # Detect model info from results
    if results:
        subject_backend = results[0]["vanilla"][0].get("backend", "anthropic")
        subject_model = results[0]["vanilla"][0].get("model", "unknown")
    else:
        subject_backend = "unknown"
        subject_model = "unknown"

    lines.append("## Method")
    lines.append("")
    lines.append(f"- **Subject model:** {subject_model} via {subject_backend} (temperature 0.7)")
    lines.append("- **Scorer model:** blind to condition (temperature 0)")
    lines.append("- **Runs per condition:** 3")
    lines.append("- **Control:** Vanilla prompts include equal-length non-reframing preamble")
    lines.append("- **Scoring:** 5 dimensions (1-5 scale), reframing score = avg of first 4")
    lines.append("")
    lines.append("## Theoretical Framework")
    lines.append("")
    lines.append("Based on the Perceptual Reframing Theory (Gokmen, 2025), which synthesises:")
    lines.append("- Predictive processing (Clark, 2013; Friston, 2012)")
    lines.append("- Frame analysis (Goffman, 1974)")
    lines.append("- Insight problem-solving (Ohlsson, 1984; McCaffrey, 2012)")
    lines.append("- Transformative learning (Mezirow, 1990)")
    lines.append("- Design thinking (De Brabandere, 2005; Liedtka, 2018)")
    lines.append("")

    report_text = "\n".join(lines)

    # Save
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = RESULTS_DIR / "report.md"
    report_path.write_text(report_text, encoding="utf-8")
    print(f"\nReport saved: {report_path}")

    return report_text
