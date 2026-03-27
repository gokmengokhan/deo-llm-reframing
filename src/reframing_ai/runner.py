"""Experiment runner — calls Groq, Ollama, vLLM, or Anthropic API."""

import asyncio
import json
import time

import httpx

from .config import (
    ANTHROPIC_SUBJECT_MODEL,
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
)
from .problems import ALL_PROBLEMS, PROBLEMS_BY_ID, Problem
from .prompts import SYSTEM_PROMPT, build_reframed, build_vanilla


def _resolve_model() -> str:
    if SUBJECT_BACKEND == "anthropic":
        return ANTHROPIC_SUBJECT_MODEL
    if SUBJECT_BACKEND == "vllm":
        return VLLM_SUBJECT_MODEL
    if SUBJECT_BACKEND == "groq":
        return GROQ_SUBJECT_MODEL
    return SUBJECT_MODEL


async def _call_ollama(client, model, system, user_prompt, temperature, max_tokens):
    resp = await client.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False,
            "options": {"temperature": temperature, "num_predict": max_tokens},
        },
        timeout=300,
    )
    resp.raise_for_status()
    data = resp.json()
    return {
        "response": data["message"]["content"],
        "input_tokens": data.get("prompt_eval_count", 0),
        "output_tokens": data.get("eval_count", 0),
    }


async def _call_openai_compat(client, url, model, system, user_prompt, temperature, max_tokens, api_key=None):
    """Shared caller for OpenAI-compatible APIs (vLLM, Groq)."""
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    for attempt in range(5):
        resp = await client.post(
            f"{url}/chat/completions",
            headers=headers,
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": temperature,
                "max_tokens": max_tokens,
            },
            timeout=300,
        )
        if resp.status_code == 429:
            wait = 15 * (attempt + 1)
            print(f"rate limited, waiting {wait}s...", end=" ", flush=True)
            await asyncio.sleep(wait)
            continue
        break
    resp.raise_for_status()
    data = resp.json()
    choice = data["choices"][0]
    usage = data.get("usage", {})
    return {
        "response": choice["message"]["content"],
        "input_tokens": usage.get("prompt_tokens", 0),
        "output_tokens": usage.get("completion_tokens", 0),
    }


async def _call_vllm(client, model, system, user_prompt, temperature, max_tokens):
    return await _call_openai_compat(client, VLLM_URL, model, system, user_prompt, temperature, max_tokens)


async def _call_groq(client, model, system, user_prompt, temperature, max_tokens):
    return await _call_openai_compat(client, GROQ_URL, model, system, user_prompt, temperature, max_tokens, GROQ_API_KEY)


async def _call_anthropic(client, model, system, user_prompt, temperature, max_tokens):
    import anthropic
    aclient = anthropic.AsyncAnthropic()
    response = await aclient.messages.create(
        model=model, max_tokens=max_tokens, temperature=temperature,
        system=system, messages=[{"role": "user", "content": user_prompt}],
    )
    return {
        "response": response.content[0].text,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    }


_CALLERS = {
    "ollama": _call_ollama,
    "vllm": _call_vllm,
    "groq": _call_groq,
    "anthropic": _call_anthropic,
}


async def call_model(client, user_prompt, run_index):
    model = _resolve_model()
    caller = _CALLERS[SUBJECT_BACKEND]
    start = time.monotonic()
    data = await caller(client, model, SYSTEM_PROMPT, user_prompt, TEMPERATURE, MAX_TOKENS)
    elapsed = time.monotonic() - start
    return {
        "backend": SUBJECT_BACKEND,
        "model": model,
        "run": run_index,
        "temperature": TEMPERATURE,
        "prompt": user_prompt,
        "response": data["response"],
        "input_tokens": data["input_tokens"],
        "output_tokens": data["output_tokens"],
        "elapsed_seconds": round(elapsed, 2),
    }


async def call_model_multi_turn(client, first_prompt, followup_prompt, run_index):
    """Two-turn call: get first response, then send followup with conversation history."""
    model = _resolve_model()

    # Turn 1
    start = time.monotonic()
    if SUBJECT_BACKEND == "groq":
        data1 = await _call_openai_compat(
            client, GROQ_URL, model, SYSTEM_PROMPT, first_prompt, TEMPERATURE, MAX_TOKENS, GROQ_API_KEY
        )
    elif SUBJECT_BACKEND == "vllm":
        data1 = await _call_openai_compat(
            client, VLLM_URL, model, SYSTEM_PROMPT, first_prompt, TEMPERATURE, MAX_TOKENS
        )
    elif SUBJECT_BACKEND == "ollama":
        data1 = await _call_ollama(client, model, SYSTEM_PROMPT, first_prompt, TEMPERATURE, MAX_TOKENS)
    else:
        data1 = await _call_anthropic(client, model, SYSTEM_PROMPT, first_prompt, TEMPERATURE, MAX_TOKENS)

    await asyncio.sleep(2)

    # Turn 2 — include conversation history
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": first_prompt},
        {"role": "assistant", "content": data1["response"]},
        {"role": "user", "content": followup_prompt},
    ]

    if SUBJECT_BACKEND == "groq":
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
        for attempt in range(5):
            resp = await client.post(f"{GROQ_URL}/chat/completions", headers=headers,
                json={"model": model, "messages": messages, "temperature": TEMPERATURE, "max_tokens": MAX_TOKENS}, timeout=300)
            if resp.status_code == 429:
                wait = 15 * (attempt + 1)
                print(f"rate limited, waiting {wait}s...", end=" ", flush=True)
                await asyncio.sleep(wait)
                continue
            break
        resp.raise_for_status()
        data2_raw = resp.json()
        data2 = {"response": data2_raw["choices"][0]["message"]["content"],
                 "input_tokens": data2_raw.get("usage", {}).get("prompt_tokens", 0),
                 "output_tokens": data2_raw.get("usage", {}).get("completion_tokens", 0)}
    elif SUBJECT_BACKEND == "ollama":
        resp = await client.post(f"{OLLAMA_URL}/api/chat",
            json={"model": model, "messages": messages, "stream": False,
                  "options": {"temperature": TEMPERATURE, "num_predict": MAX_TOKENS}}, timeout=300)
        resp.raise_for_status()
        d = resp.json()
        data2 = {"response": d["message"]["content"],
                 "input_tokens": d.get("prompt_eval_count", 0), "output_tokens": d.get("eval_count", 0)}
    else:
        import anthropic
        aclient = anthropic.AsyncAnthropic()
        r = await aclient.messages.create(model=model, max_tokens=MAX_TOKENS, temperature=TEMPERATURE,
            system=SYSTEM_PROMPT, messages=[
                {"role": "user", "content": first_prompt},
                {"role": "assistant", "content": data1["response"]},
                {"role": "user", "content": followup_prompt},
            ])
        data2 = {"response": r.content[0].text,
                 "input_tokens": r.usage.input_tokens, "output_tokens": r.usage.output_tokens}

    elapsed = time.monotonic() - start

    return {
        "backend": SUBJECT_BACKEND,
        "model": model,
        "run": run_index,
        "temperature": TEMPERATURE,
        "prompt": first_prompt,
        "followup": followup_prompt,
        "turn1_response": data1["response"],
        "response": data2["response"],  # The final (reframed) response
        "input_tokens": data1["input_tokens"] + data2["input_tokens"],
        "output_tokens": data1["output_tokens"] + data2["output_tokens"],
        "elapsed_seconds": round(elapsed, 2),
    }


async def run_problem(client, problem, n_runs=RUNS_PER_CONDITION):
    print(f"\n{'='*60}")
    print(f"  {problem.title}")
    print(f"  Category: {problem.category}")
    print(f"  Paths: {', '.join(problem.paths_applied)}")
    print(f"{'='*60}")

    vanilla_results = []
    reframed_results = []

    for i in range(n_runs):
        print(f"  Run {i+1}/{n_runs} — vanilla...", end=" ", flush=True)
        v = await call_model(client, build_vanilla(problem), i)
        vanilla_results.append(v)
        print(f"done ({v['elapsed_seconds']}s)")

        # Groq rate limit: ~30 req/min, pace at 2s between calls
        await asyncio.sleep(1)

        if problem.reframing_followup:
            # Multi-turn: send vanilla first, then followup
            print(f"  Run {i+1}/{n_runs} — reframed (2-turn)...", end=" ", flush=True)
            r = await call_model_multi_turn(
                client, build_vanilla(problem), problem.reframing_followup, i
            )
        else:
            print(f"  Run {i+1}/{n_runs} — reframed...", end=" ", flush=True)
            r = await call_model(client, build_reframed(problem), i)
        reframed_results.append(r)
        print(f"done ({r['elapsed_seconds']}s)")

        if i < n_runs - 1:
            await asyncio.sleep(1)

    result = {
        "problem_id": problem.id,
        "problem_title": problem.title,
        "category": problem.category,
        "paths_applied": problem.paths_applied,
        "theory_connection": problem.theory_connection,
        "expected_vanilla_failure": problem.expected_vanilla_failure,
        "success_criteria": problem.success_criteria,
        "vanilla": vanilla_results,
        "reframed": reframed_results,
    }

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RAW_DIR / f"{problem.id}.json"
    output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"  Saved: {output_path}")
    return result


async def run_experiment(problem_ids=None, n_runs=RUNS_PER_CONDITION):
    model = _resolve_model()
    problems = [PROBLEMS_BY_ID[pid] for pid in problem_ids] if problem_ids else ALL_PROBLEMS

    print(f"\nRunning experiment: {len(problems)} problems x {n_runs} runs x 2 conditions")
    print(f"Backend: {SUBJECT_BACKEND} | Model: {model} | Temperature: {TEMPERATURE}")

    async with httpx.AsyncClient() as client:
        results = []
        for problem in problems:
            results.append(await run_problem(client, problem, n_runs))

    print(f"\nExperiment complete. {len(results)} problems processed.")
    return results


def load_results(problem_ids=None):
    results = []
    paths = [RAW_DIR / f"{pid}.json" for pid in problem_ids] if problem_ids else sorted(RAW_DIR.glob("*.json"))
    for p in paths:
        if p.exists():
            results.append(json.loads(p.read_text()))
    return results
