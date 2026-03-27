"""Export experiment data to CSV for R verification."""

import csv
import json
from pathlib import Path

RESULTS_DIR = Path("results")
MODELS = ["llama", "qwen", "llama4scout"]
REFRAMING_DIMS = ["frame_diversity", "assumption_surfacing", "solution_novelty", "premise_questioning"]


def safe_score(score_dict, dim):
    if dim in score_dict and isinstance(score_dict[dim], dict):
        return score_dict[dim].get("score", 3)
    return 3


def reframing_score(score_dict):
    return sum(safe_score(score_dict, d) for d in REFRAMING_DIMS) / 4


def export_study1(out_path):
    rows = []
    for model in MODELS:
        raw = RESULTS_DIR / model / "raw"
        for p in sorted(raw.glob("*.json")):
            if p.name.startswith("deo_"):
                continue
            d = json.loads(p.read_text())
            pid = d["problem_id"]
            cat = d.get("category", "unknown")
            paths = "|".join(d.get("paths_applied", []))

            for cond, cond_key, score_suffixes in [
                ("vanilla", "vanilla", [("self", "_scores"), ("claude", "_claude_scores"), ("openai", "_openai_scores")]),
                ("distance", "reframed", [("self", "_scores"), ("claude", "_claude_scores"), ("openai", "_openai_scores")]),
            ]:
                for scorer_name, suffix in score_suffixes:
                    scores_key = f"{cond_key}{suffix}"
                    if scores_key not in d:
                        continue
                    for run_i, s in enumerate(d[scores_key]):
                        rows.append({
                            "model": model,
                            "problem_id": pid,
                            "category": cat,
                            "paths": paths,
                            "condition": cond,
                            "scorer": scorer_name,
                            "run": run_i,
                            "reframing_score": round(reframing_score(s), 4),
                            "correctness": safe_score(s, "correctness"),
                            "frame_diversity": safe_score(s, "frame_diversity"),
                            "assumption_surfacing": safe_score(s, "assumption_surfacing"),
                            "solution_novelty": safe_score(s, "solution_novelty"),
                            "premise_questioning": safe_score(s, "premise_questioning"),
                        })

    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    print(f"Study 1: {len(rows)} rows -> {out_path}")


def export_study2(out_path):
    rows = []
    for model in MODELS:
        raw = RESULTS_DIR / model / "raw"
        for p in sorted(raw.glob("deo_*.json")):
            d = json.loads(p.read_text())
            pid = d.get("problem_id", p.stem)
            cat = d.get("category", "unknown")
            paths = "|".join(d.get("paths_applied", []))

            for cond in ["vanilla", "distance", "engagement", "deo"]:
                for scorer_name, suffix in [("self", ""), ("claude", "_claude"), ("openai", "_openai")]:
                    scores_key = f"{cond}{suffix}_scores"
                    if scores_key not in d:
                        continue
                    for run_i, s in enumerate(d[scores_key]):
                        rows.append({
                            "model": model,
                            "problem_id": pid,
                            "category": cat,
                            "paths": paths,
                            "condition": cond,
                            "scorer": scorer_name,
                            "run": run_i,
                            "reframing_score": round(reframing_score(s), 4),
                            "correctness": safe_score(s, "correctness"),
                            "frame_diversity": safe_score(s, "frame_diversity"),
                            "assumption_surfacing": safe_score(s, "assumption_surfacing"),
                            "solution_novelty": safe_score(s, "solution_novelty"),
                            "premise_questioning": safe_score(s, "premise_questioning"),
                        })

    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    print(f"Study 2: {len(rows)} rows -> {out_path}")


if __name__ == "__main__":
    export_study1("paper/study1_data.csv")
    export_study2("paper/study2_data.csv")
