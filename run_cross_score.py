"""Run cross-model scoring with Claude Sonnet 4.6 and GPT-4.1.

Usage:
    uv run python run_cross_score.py                    # score all model results
    uv run python run_cross_score.py --models llama     # score specific model
"""

import argparse
import asyncio

from dotenv import load_dotenv
load_dotenv()

from src.reframing_ai.cross_scorer import run_cross_scoring


def main():
    parser = argparse.ArgumentParser(description="Cross-model scoring")
    parser.add_argument("--models", nargs="+", help="Model dirs to score (e.g., llama qwen)")
    args = parser.parse_args()

    asyncio.run(run_cross_scoring(args.models))


if __name__ == "__main__":
    main()
