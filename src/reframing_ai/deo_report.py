"""Study 2 report — DEO 4-condition comparison."""

import json
from .config import RAW_DIR, RESULTS_DIR, RUNS_PER_CONDITION, SCORING_DIMENSIONS
from .deo_runner import CONDITIONS, load_deo_results


def _avg(scores_list, dim):
    values = [s[dim]["score"] for s in scores_list if dim in s]
    return round(sum(values) / len(values), 2) if values else 0.0


def _rf_score(scores_list):
    dims = ["frame_diversity", "assumption_surfacing", "solution_novelty", "premise_questioning"]
    values = [s[d]["score"] for s in scores_list for d in dims if d in s]
    return round(sum(values) / len(values), 2) if values else 0.0


def _truncate(text, max_lines=25):
    lines = text.strip().split("\n")
    if len(lines) <= max_lines:
        return text.strip()
    return "\n".join(lines[:max_lines]) + f"\n\n*[... truncated, {len(lines)} lines total]*"


def generate_deo_report(problem_ids=None):
    results = load_deo_results(problem_ids)

    if not results:
        return "# No DEO results found."

    has_scores = "vanilla_scores" in results[0]

    lines = [
        "# Study 2: Distance-Engagement Oscillation (DEO)",
        "",
        "> **The unique claim:** Reframing requires oscillation between cognitive distance",
        "> (seeing the frame) and emotional engagement (feeling the shift). Neither alone suffices.",
        "> DEO is the mechanism that unifies all traditions of perceptual reframing.",
        "",
    ]

    # Executive summary
    if has_scores:
        lines += ["## Executive Summary", "",
            "| Problem | Vanilla | Distance | Engagement | DEO | DEO vs Distance |",
            "|---------|---------|----------|------------|-----|-----------------|"]

        totals = {c: 0 for c in CONDITIONS}
        count = 0

        for r in results:
            row = []
            for c in CONDITIONS:
                key = f"{c}_scores"
                if key in r:
                    rf = _rf_score(r[key])
                    totals[c] += rf
                    row.append(rf)
                else:
                    row.append("-")
            count += 1
            deo_v_dist = ""
            if isinstance(row[1], float) and isinstance(row[3], float):
                d = round(row[3] - row[1], 2)
                deo_v_dist = f"{'+' if d > 0 else ''}{d}"
            lines.append(
                f"| {r['problem_title']} | {row[0]} | {row[1]} | {row[2]} | {row[3]} | {deo_v_dist} |"
            )

        if count:
            avgs = {c: round(totals[c] / count, 2) for c in CONDITIONS}
            d = round(avgs["deo"] - avgs["distance"], 2)
            lines.append(
                f"| **Average** | **{avgs['vanilla']}** | **{avgs['distance']}** | "
                f"**{avgs['engagement']}** | **{avgs['deo']}** | **{'+' if d > 0 else ''}{d}** |"
            )
        lines.append("")

        # Test the prediction
        lines += ["### Prediction Test", ""]
        lines.append("The theory predicts: **DEO > Distance-only > Vanilla >= Engagement-only**")
        lines.append("")
        if count:
            ordering = sorted(CONDITIONS, key=lambda c: avgs[c], reverse=True)
            lines.append(f"Observed ordering: **{' > '.join(ordering)}** ({' > '.join(str(avgs[c]) for c in ordering)})")
        lines.append("")

    # Per-problem detail
    lines += ["---", "", "## Problem-by-Problem Analysis", ""]

    for r in results:
        lines += [f"### {r['problem_title']}", ""]
        if 'theory_prediction' in r:
            lines.append(f"**Theory prediction:** {r['theory_prediction']}")
        lines.append(f"**Theory:** {r.get('theory_connection', '')}")
        lines.append("")

        for c in CONDITIONS:
            label = {"vanilla": "Vanilla", "distance": "Distance-Only",
                     "engagement": "Engagement-Only", "deo": "DEO (Oscillation)"}[c]
            lines.append(f"#### {label}")
            if c in r and r[c]:
                lines.append("```")
                lines.append(_truncate(r[c][0]["response"]))
                lines.append("```")
            lines.append("")

        if has_scores:
            lines += ["#### Score Comparison", "",
                "| Dimension | Vanilla | Distance | Engagement | DEO |",
                "|-----------|---------|----------|------------|-----|"]
            for dim in SCORING_DIMENSIONS:
                row = []
                for c in CONDITIONS:
                    key = f"{c}_scores"
                    if key in r:
                        row.append(str(_avg(r[key], dim)))
                    else:
                        row.append("-")
                lines.append(f"| {dim.replace('_', ' ').title()} | {' | '.join(row)} |")
            lines.append("")

        lines += ["---", ""]

    # Method
    model = results[0]["vanilla"][0].get("model", "unknown") if results else "unknown"
    backend = results[0]["vanilla"][0].get("backend", "unknown") if results else "unknown"
    lines += [
        "## Method", "",
        f"- **Subject model:** {model} via {backend} (temperature 0.7)",
        "- **Conditions:** Vanilla (step-by-step), Distance-only (analytical reframing), "
        "Engagement-only (immersive, first-person), DEO (distance-engagement oscillation)",
        "- **DEO prompt structure:** ANALYSE (distance) -> FEEL (engagement) -> REFRAME (distance) -> ENVISION (engagement)",
        f"- **Runs per condition:** {RUNS_PER_CONDITION}",
        "- **Scoring:** 5 dimensions (1-5), blind to condition",
        "",
        "## Theoretical Basis",
        "",
        "The Distance-Engagement Oscillation (DEO) is the unique contribution of the",
        "Perceptual Reframing Theory (Gokmen, 2025). The claim: reframing operates through",
        "paradoxical oscillation between cognitive distance and emotional engagement.",
        "Neither alone is sufficient. Distance without engagement produces intellectual",
        "insight that doesn't stick. Engagement without distance produces emotional",
        "activation trapped within the current frame. The oscillation itself is the mechanism.",
        "",
    ]

    report = "\n".join(lines)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    path = RESULTS_DIR / "deo_report.md"
    path.write_text(report, encoding="utf-8")
    print(f"\nDEO report saved: {path}")
    return report
