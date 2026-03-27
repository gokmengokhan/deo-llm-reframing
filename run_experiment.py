"""CLI entry point for the Perceptual Reframing for AI experiment.

Usage:
    uv run python run_experiment.py                        # run all problems + score + report
    uv run python run_experiment.py --problem shipping_containers  # single problem
    uv run python run_experiment.py --score-only           # re-score existing results
    uv run python run_experiment.py --report-only          # regenerate report from scored results
    uv run python run_experiment.py --list                 # list available problems
"""

import argparse
import asyncio
import sys

from dotenv import load_dotenv

load_dotenv()

from src.reframing_ai.problems import ALL_PROBLEMS, PROBLEMS_BY_ID
from src.reframing_ai.runner import run_experiment
from src.reframing_ai.scorer import score_all
from src.reframing_ai.report import generate_report


def main():
    parser = argparse.ArgumentParser(
        description="Perceptual Reframing for AI — Experiment Runner"
    )
    parser.add_argument(
        "--problem",
        type=str,
        nargs="+",
        help="Run specific problem(s) by ID",
    )
    parser.add_argument(
        "--score-only",
        action="store_true",
        help="Only score existing results (skip running the experiment)",
    )
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="Only regenerate the report from scored results",
    )
    parser.add_argument(
        "--no-score",
        action="store_true",
        help="Run experiment but skip scoring",
    )
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Run experiment but skip report generation",
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=None,
        help="Override number of runs per condition",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available problems and exit",
    )
    args = parser.parse_args()

    # List mode
    if args.list:
        print("\nAvailable problems:\n")
        for p in ALL_PROBLEMS:
            paths = ", ".join(p.paths_applied)
            print(f"  {p.id:<25} {p.category:<25} {paths}")
        return

    # Validate problem IDs
    problem_ids = args.problem
    if problem_ids:
        for pid in problem_ids:
            if pid not in PROBLEMS_BY_ID:
                print(f"Error: unknown problem '{pid}'")
                print(f"Available: {', '.join(PROBLEMS_BY_ID.keys())}")
                sys.exit(1)

    # Report-only mode
    if args.report_only:
        print("Regenerating report from existing results...")
        generate_report(problem_ids)
        return

    # Score-only mode
    if args.score_only:
        print("Scoring existing results...")
        asyncio.run(score_all(problem_ids))
        if not args.no_report:
            generate_report(problem_ids)
        return

    # Full run
    run_kwargs = {}
    if args.runs:
        run_kwargs["n_runs"] = args.runs

    asyncio.run(run_experiment(problem_ids, **run_kwargs))

    if not args.no_score:
        print("\n--- Scoring ---")
        asyncio.run(score_all(problem_ids))

    if not args.no_report:
        print("\n--- Generating Report ---")
        generate_report(problem_ids)


if __name__ == "__main__":
    main()
