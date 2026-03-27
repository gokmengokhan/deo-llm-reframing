"""Cross-model scoring — Claude Sonnet 4.6 and GPT-4.1 as independent blind judges.

Re-scores all existing results from all subject models using external scorers.
This addresses the self-scoring limitation by providing cross-family validation.
"""

import asyncio
import json
import os
import re
from pathlib import Path

import anthropic
import httpx
from openai import AsyncOpenAI

from .config import RAW_DIR, RESULTS_DIR, SCORING_DIMENSIONS
from .scorer import SCORER_SYSTEM, SCORER_RUBRIC, _extract_json

# External scorer models
CLAUDE_SCORER = "claude-sonnet-4-20250514"
OPENAI_SCORER = "gpt-4.1"


async def _score_claude(client: anthropic.AsyncAnthropic, user_prompt: str) -> dict:
    """Score using Claude Sonnet 4.6."""
    for attempt in range(3):
        try:
            result = await client.messages.create(
                model=CLAUDE_SCORER,
                max_tokens=1024,
                temperature=0,
                system=SCORER_SYSTEM,
                messages=[{"role": "user", "content": user_prompt}],
            )
            return _extract_json(result.content[0].text)
        except Exception as e:
            if attempt < 2:
                print(f"retry ({e})...", end=" ", flush=True)
                await asyncio.sleep(5)
            else:
                print(f"FAILED ({e}), using neutral...", end=" ", flush=True)
                return {d: {"score": 3, "justification": "scorer error"} for d in SCORING_DIMENSIONS}


async def _score_openai(client: AsyncOpenAI, user_prompt: str) -> dict:
    """Score using GPT-4.1."""
    for attempt in range(3):
        try:
            result = await client.chat.completions.create(
                model=OPENAI_SCORER,
                max_tokens=1024,
                temperature=0,
                messages=[
                    {"role": "system", "content": SCORER_SYSTEM},
                    {"role": "user", "content": user_prompt},
                ],
            )
            return _extract_json(result.choices[0].message.content)
        except Exception as e:
            if attempt < 2:
                print(f"retry ({e})...", end=" ", flush=True)
                await asyncio.sleep(5)
            else:
                print(f"FAILED ({e}), using neutral...", end=" ", flush=True)
                return {d: {"score": 3, "justification": "scorer error"} for d in SCORING_DIMENSIONS}


def _build_scorer_prompt(problem_statement: str, success_criteria: str, response_text: str) -> str:
    return (
        f"## Problem\n{problem_statement}\n\n"
        f"## Success Criteria\n{success_criteria}\n\n"
        f"## Response to Evaluate\n{response_text}\n\n"
        f"## Scoring Rubric\n{SCORER_RUBRIC}"
    )


async def cross_score_model_results(model_dir: Path, scorer_name: str):
    """Score all results in a model directory with an external scorer."""
    raw_dir = model_dir / "raw"
    if not raw_dir.exists():
        print(f"  No raw dir: {raw_dir}")
        return

    claude_client = anthropic.AsyncAnthropic()
    openai_client = AsyncOpenAI()

    for json_path in sorted(raw_dir.glob("*.json")):
        result = json.loads(json_path.read_text())
        is_deo = result.get("study") == "deo"

        print(f"\n  {scorer_name} scoring: {result.get('problem_title', json_path.stem)}")

        # Determine conditions to score
        if is_deo:
            conditions = ["vanilla", "distance", "engagement", "deo"]
        else:
            conditions = ["vanilla", "reframed"]

        # Get problem statement and criteria
        first_condition = conditions[0]
        if first_condition not in result or not result[first_condition]:
            continue
        problem_statement = result[first_condition][0]["prompt"]
        success_criteria = result.get("success_criteria", "")

        for condition in conditions:
            if condition not in result:
                continue
            scores_key = f"{condition}_{scorer_name}_scores"
            scores = []
            for i, run in enumerate(result[condition]):
                print(f"    {condition} run {i+1}...", end=" ", flush=True)
                prompt = _build_scorer_prompt(problem_statement, success_criteria, run["response"])

                if scorer_name == "claude":
                    s = await _score_claude(claude_client, prompt)
                else:
                    s = await _score_openai(openai_client, prompt)

                scores.append(s)
                print("done")
                await asyncio.sleep(1)

            result[scores_key] = scores

        # Save back
        json_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"    Saved: {json_path.name}")


async def run_cross_scoring(model_dirs: list[str] | None = None):
    """Run cross-model scoring on all model results."""
    results_dir = RESULTS_DIR

    if model_dirs:
        dirs = [results_dir / d for d in model_dirs]
    else:
        dirs = [d for d in results_dir.iterdir() if d.is_dir() and (d / "raw").exists()]

    for model_dir in sorted(dirs):
        model_name = model_dir.name
        print(f"\n{'#'*60}")
        print(f"  Cross-scoring: {model_name}")
        print(f"{'#'*60}")

        for scorer_name in ["claude", "openai"]:
            print(f"\n  --- Scorer: {scorer_name} ---")
            await cross_score_model_results(model_dir, scorer_name)

    print("\n=== Cross-scoring complete ===")
