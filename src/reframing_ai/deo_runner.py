"""Unified DEO runner — 4-condition experiment using Problem class directly."""

import asyncio
import json
import time

import httpx

from .config import (
    GROQ_API_KEY,
    GROQ_SUBJECT_MODEL,
    GROQ_URL,
    MAX_TOKENS,
    OLLAMA_URL,
    RAW_DIR,
    RUNS_PER_CONDITION,
    SUBJECT_BACKEND,
    SUBJECT_MODEL,
    TEMPERATURE,
    VLLM_SUBJECT_MODEL,
    VLLM_URL,
    ANTHROPIC_SUBJECT_MODEL,
)
from .problems import ALL_PROBLEMS, PROBLEMS_BY_ID, Problem
from .prompts import SYSTEM_PROMPT, VANILLA_PREAMBLE
from .runner import _call_openai_compat, _call_ollama, _call_anthropic, _resolve_model


CONDITIONS = ["vanilla", "distance", "engagement", "deo"]


def get_deo_problems():
    """Return all problems that have DEO preambles (excludes multi-turn)."""
    return [p for p in ALL_PROBLEMS if p.deo_preamble and p.engagement_preamble]


DEO_PROBLEMS_BY_ID = {p.id: p for p in get_deo_problems()}


def _build_prompt(problem: Problem, condition: str) -> str:
    if condition == "vanilla":
        return VANILLA_PREAMBLE + problem.vanilla_prompt
    elif condition == "distance":
        return problem.reframing_preamble + problem.vanilla_prompt
    elif condition == "engagement":
        return problem.engagement_preamble + problem.vanilla_prompt
    elif condition == "deo":
        return problem.deo_preamble + problem.vanilla_prompt
    raise ValueError(f"Unknown condition: {condition}")


async def _call_model(client, prompt):
    model = _resolve_model()
    if SUBJECT_BACKEND == "groq":
        return await _call_openai_compat(
            client, GROQ_URL, model, SYSTEM_PROMPT, prompt, TEMPERATURE, MAX_TOKENS, GROQ_API_KEY
        )
    elif SUBJECT_BACKEND == "ollama":
        return await _call_ollama(client, model, SYSTEM_PROMPT, prompt, TEMPERATURE, MAX_TOKENS)
    elif SUBJECT_BACKEND == "vllm":
        return await _call_openai_compat(
            client, VLLM_URL, model, SYSTEM_PROMPT, prompt, TEMPERATURE, MAX_TOKENS
        )
    else:
        return await _call_anthropic(client, model, SYSTEM_PROMPT, prompt, TEMPERATURE, MAX_TOKENS)


async def run_deo_problem(client, problem, n_runs=RUNS_PER_CONDITION):
    print(f"\n{'='*60}")
    print(f"  {problem.title}")
    print(f"{'='*60}")

    results_by_condition = {}

    for condition in CONDITIONS:
        print(f"\n  Condition: {condition}")
        runs = []
        for i in range(n_runs):
            print(f"    Run {i+1}/{n_runs}...", end=" ", flush=True)
            prompt = _build_prompt(problem, condition)
            start = time.monotonic()
            data = await _call_model(client, prompt)
            elapsed = time.monotonic() - start
            runs.append({
                "backend": SUBJECT_BACKEND,
                "model": _resolve_model(),
                "condition": condition,
                "run": i,
                "temperature": TEMPERATURE,
                "prompt": prompt,
                "response": data["response"],
                "input_tokens": data["input_tokens"],
                "output_tokens": data["output_tokens"],
                "elapsed_seconds": round(elapsed, 2),
            })
            print(f"done ({elapsed:.1f}s)")
            await asyncio.sleep(3)
        results_by_condition[condition] = runs

    result = {
        "study": "deo",
        "problem_id": problem.id,
        "problem_title": problem.title,
        "category": problem.category,
        "paths_applied": problem.paths_applied,
        "theory_connection": problem.theory_connection,
        "expected_vanilla_failure": problem.expected_vanilla_failure,
        "success_criteria": problem.success_criteria,
        **results_by_condition,
    }

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RAW_DIR / f"deo_{problem.id}.json"
    output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"  Saved: {output_path}")
    return result


async def run_deo_experiment(problem_ids=None, n_runs=RUNS_PER_CONDITION):
    problems = [DEO_PROBLEMS_BY_ID[pid] for pid in problem_ids] if problem_ids else get_deo_problems()
    model = _resolve_model()

    print(f"\nStudy 2: DEO Mechanism")
    print(f"  {len(problems)} problems x {n_runs} runs x 4 conditions")
    print(f"  Backend: {SUBJECT_BACKEND} | Model: {model}")

    async with httpx.AsyncClient() as client:
        results = []
        for problem in problems:
            results.append(await run_deo_problem(client, problem, n_runs))

    print(f"\nStudy 2 complete. {len(results)} problems processed.")
    return results


def load_deo_results(problem_ids=None):
    results = []
    if problem_ids:
        paths = [RAW_DIR / f"deo_{pid}.json" for pid in problem_ids]
    else:
        paths = sorted(RAW_DIR.glob("deo_*.json"))
    for p in paths:
        if p.exists():
            data = json.loads(p.read_text())
            if data.get("study") == "deo":
                results.append(data)
    return results
