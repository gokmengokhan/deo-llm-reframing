"""Study 2 scorer — blind scoring for DEO experiment."""

import asyncio
import json

import httpx

from .config import RAW_DIR, SCORER_BACKEND
from .deo_runner import CONDITIONS, load_deo_results
from .scorer import score_response


async def score_deo_results(problem_ids=None):
    """Score all DEO results."""
    results = load_deo_results(problem_ids)

    for result in results:
        print(f"\n  Scoring: {result['problem_title']}")

        problem_statement = result["vanilla"][0]["prompt"]
        success_criteria = result["success_criteria"]

        async with httpx.AsyncClient() as client:
            for condition in CONDITIONS:
                scores = []
                for i, run in enumerate(result[condition]):
                    print(f"    {condition} run {i+1}...", end=" ", flush=True)
                    s = await score_response(
                        client, problem_statement, success_criteria, run["response"]
                    )
                    scores.append(s)
                    print("done")
                    await asyncio.sleep(4)
                result[f"{condition}_scores"] = scores

        path = RAW_DIR / f"deo_{result['problem_id']}.json"
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"    Saved scores: {path}")
