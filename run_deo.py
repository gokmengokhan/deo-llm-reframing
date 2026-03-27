"""CLI entry point for Study 2: DEO experiment.

Usage:
    uv run python run_deo.py                         # run all DEO problems + score + report
    uv run python run_deo.py --problem deo_hiring     # single problem
    uv run python run_deo.py --score-only             # re-score existing results
    uv run python run_deo.py --report-only            # regenerate report
    uv run python run_deo.py --list                   # list DEO problems
"""

import argparse
import asyncio
import sys

from dotenv import load_dotenv

load_dotenv()

from src.reframing_ai.deo_runner import get_deo_problems, DEO_PROBLEMS_BY_ID
from src.reframing_ai.deo_runner import run_deo_experiment
from src.reframing_ai.deo_scorer import score_deo_results
from src.reframing_ai.deo_report import generate_deo_report


def main():
    parser = argparse.ArgumentParser(description="Study 2: DEO Mechanism Experiment")
    parser.add_argument("--problem", type=str, nargs="+", help="Run specific DEO problem(s) by ID")
    parser.add_argument("--score-only", action="store_true")
    parser.add_argument("--report-only", action="store_true")
    parser.add_argument("--no-score", action="store_true")
    parser.add_argument("--no-report", action="store_true")
    parser.add_argument("--runs", type=int, default=None)
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()

    if args.list:
        print("\nDEO Problems:\n")
        for p in get_deo_problems():
            print(f"  {p.id}")
        return

    problem_ids = args.problem
    if problem_ids:
        for pid in problem_ids:
            if pid not in DEO_PROBLEMS_BY_ID:
                print(f"Error: unknown DEO problem '{pid}'")
                print(f"Available: {', '.join(DEO_PROBLEMS_BY_ID.keys())}")
                sys.exit(1)

    if args.report_only:
        generate_deo_report(problem_ids)
        return

    if args.score_only:
        asyncio.run(score_deo_results(problem_ids))
        if not args.no_report:
            generate_deo_report(problem_ids)
        return

    run_kwargs = {}
    if args.runs:
        run_kwargs["n_runs"] = args.runs

    asyncio.run(run_deo_experiment(problem_ids, **run_kwargs))

    if not args.no_score:
        print("\n--- Scoring ---")
        asyncio.run(score_deo_results(problem_ids))

    if not args.no_report:
        print("\n--- Generating Report ---")
        generate_deo_report(problem_ids)


if __name__ == "__main__":
    main()
