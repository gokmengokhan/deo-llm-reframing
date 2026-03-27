"""Run the complete experiment: Study 1 + Study 2, across multiple models.

Usage:
    uv run python run_full.py                    # both studies, default model
    uv run python run_full.py --models llama qwen # both studies, both models
"""

import argparse
import asyncio
import shutil
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

from src.reframing_ai import config
from src.reframing_ai.config import RAW_DIR, RESULTS_DIR
from src.reframing_ai.runner import run_experiment
from src.reframing_ai.scorer import score_all
from src.reframing_ai.report import generate_report
from src.reframing_ai.deo_runner import run_deo_experiment
from src.reframing_ai.deo_scorer import score_deo_results
from src.reframing_ai.deo_report import generate_deo_report


MODELS = {
    "llama": {
        "subject": "llama-3.3-70b-versatile",
        "scorer": "llama-3.3-70b-versatile",
    },
    "qwen": {
        "subject": "qwen/qwen3-32b",
        "scorer": "qwen/qwen3-32b",
    },
    "llama4scout": {
        "subject": "meta-llama/llama-4-scout-17b-16e-instruct",
        "scorer": "meta-llama/llama-4-scout-17b-16e-instruct",
    },
}


def set_model(model_key):
    """Override the Groq model in config."""
    m = MODELS[model_key]
    config.GROQ_SUBJECT_MODEL = m["subject"]
    config.GROQ_SCORER_MODEL = m["scorer"]


def archive_results(model_key):
    """Move results to a model-specific directory."""
    dest = RESULTS_DIR / model_key
    dest.mkdir(parents=True, exist_ok=True)

    # Copy raw results
    raw_dest = dest / "raw"
    if raw_dest.exists():
        shutil.rmtree(raw_dest)
    shutil.copytree(RAW_DIR, raw_dest)

    # Copy reports
    for report in RESULTS_DIR.glob("*.md"):
        shutil.copy2(report, dest / report.name)

    print(f"\nResults archived to: {dest}")


def main():
    parser = argparse.ArgumentParser(description="Full experiment runner")
    parser.add_argument(
        "--models",
        nargs="+",
        choices=list(MODELS.keys()),
        default=["llama"],
        help="Models to test (default: llama)",
    )
    parser.add_argument("--study", choices=["1", "2", "both"], default="both")
    parser.add_argument("--no-score", action="store_true")
    args = parser.parse_args()

    for model_key in args.models:
        set_model(model_key)
        model_name = MODELS[model_key]["subject"]
        print(f"\n{'#'*60}")
        print(f"  MODEL: {model_name}")
        print(f"{'#'*60}")

        # Clear previous raw results for clean run
        if RAW_DIR.exists():
            shutil.rmtree(RAW_DIR)
        RAW_DIR.mkdir(parents=True)

        if args.study in ("1", "both"):
            print(f"\n=== Study 1: Path Effectiveness ({model_name}) ===")
            asyncio.run(run_experiment())
            if not args.no_score:
                print("\n--- Scoring Study 1 ---")
                asyncio.run(score_all())
            print("\n--- Study 1 Report ---")
            generate_report()

        if args.study in ("2", "both"):
            print(f"\n=== Study 2: DEO Mechanism ({model_name}) ===")
            asyncio.run(run_deo_experiment())
            if not args.no_score:
                print("\n--- Scoring Study 2 ---")
                asyncio.run(score_deo_results())
            print("\n--- Study 2 Report ---")
            generate_deo_report()

        archive_results(model_key)

    print("\n" + "=" * 60)
    print("  ALL DONE")
    print("=" * 60)
    for model_key in args.models:
        print(f"  {model_key}: results/{model_key}/")


if __name__ == "__main__":
    main()
