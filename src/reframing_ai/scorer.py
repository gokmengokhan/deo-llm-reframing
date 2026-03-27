"""Blind scorer — uses a separate model to evaluate responses without knowing the condition."""

import asyncio
import json
import re

import httpx

from .config import (
    ANTHROPIC_SCORER_MODEL,
    GROQ_API_KEY,
    GROQ_SCORER_MODEL,
    GROQ_URL,
    OLLAMA_URL,
    RAW_DIR,
    SCORER_BACKEND,
    SCORER_MAX_TOKENS,
    SCORER_MODEL,
    VLLM_SCORER_MODEL,
    VLLM_URL,
)

SCORER_SYSTEM = (
    "You are an expert evaluator assessing the quality of responses to problems. "
    "You will be given a problem statement, success criteria, and a response. "
    "Score the response on each dimension using the rubric provided. "
    "Return ONLY valid JSON, no other text."
)

SCORER_RUBRIC = """Score this response on each dimension (1-5):

**frame_diversity** — How many distinct frames/perspectives does the response consider?
  1 = single frame only
  2 = one frame with minor acknowledgment of alternatives
  3 = two distinct frames explored
  4 = three frames explored with comparison
  5 = four or more frames explored with synthesis

**assumption_surfacing** — Does the response identify and question hidden assumptions?
  1 = no assumptions identified
  2 = one obvious assumption noted
  3 = two assumptions identified and examined
  4 = three or more assumptions, some non-obvious
  5 = systematically surfaces and examines hidden assumptions

**solution_novelty** — Does the response produce solutions beyond the obvious first-order answer?
  1 = only the most conventional response
  2 = conventional response with minor variation
  3 = one non-obvious solution alongside conventional ones
  4 = multiple non-obvious solutions
  5 = genuinely unexpected viable solution that reframes the problem

**premise_questioning** — Does the response question whether the problem is well-posed?
  1 = accepts the problem exactly as stated
  2 = minor caveat but solves as stated
  3 = notes the problem framing may be limiting
  4 = explicitly questions the premise and explores alternatives
  5 = fundamentally reframes the question before answering

**correctness** — Is the response actually right and practically useful?
  1 = factually wrong or useless
  2 = partially correct but impractical
  3 = correct and reasonable
  4 = correct with good practical detail
  5 = excellent practical advice grounded in reality

Return JSON in this exact format:
{
  "frame_diversity": {"score": N, "justification": "..."},
  "assumption_surfacing": {"score": N, "justification": "..."},
  "solution_novelty": {"score": N, "justification": "..."},
  "premise_questioning": {"score": N, "justification": "..."},
  "correctness": {"score": N, "justification": "..."}
}"""


def _extract_json(text: str) -> dict:
    """Extract JSON from a response that may contain markdown fences or extra text."""
    text = text.strip()
    # Strip markdown code fences
    if "```" in text:
        match = re.search(r"```(?:json)?\s*\n?(.*?)```", text, re.DOTALL)
        if match:
            text = match.group(1).strip()
    # Try to parse the whole text first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Try to find a JSON object
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    # Fallback: return neutral scores if parsing fails completely
    print("JSON parse failed, using neutral scores...", end=" ", flush=True)
    return {
        "frame_diversity": {"score": 3, "justification": "parse error"},
        "assumption_surfacing": {"score": 3, "justification": "parse error"},
        "solution_novelty": {"score": 3, "justification": "parse error"},
        "premise_questioning": {"score": 3, "justification": "parse error"},
        "correctness": {"score": 3, "justification": "parse error"},
    }


async def _score_ollama(
    client: httpx.AsyncClient,
    user_prompt: str,
) -> dict:
    """Score using Ollama."""
    resp = await client.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": SCORER_MODEL,
            "messages": [
                {"role": "system", "content": SCORER_SYSTEM},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0,
                "num_predict": SCORER_MAX_TOKENS,
            },
        },
        timeout=300,
    )
    resp.raise_for_status()
    text = resp.json()["message"]["content"]
    return _extract_json(text)


async def _score_vllm(
    client: httpx.AsyncClient,
    user_prompt: str,
) -> dict:
    """Score using vLLM's OpenAI-compatible API."""
    resp = await client.post(
        f"{VLLM_URL}/v1/chat/completions",
        json={
            "model": VLLM_SCORER_MODEL,
            "messages": [
                {"role": "system", "content": SCORER_SYSTEM},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0,
            "max_tokens": SCORER_MAX_TOKENS,
        },
        timeout=300,
    )
    resp.raise_for_status()
    text = resp.json()["choices"][0]["message"]["content"]
    return _extract_json(text)


async def _score_groq(client, user_prompt):
    """Score using Groq's OpenAI-compatible API with retry on rate limit."""
    for attempt in range(5):
        resp = await client.post(
            f"{GROQ_URL}/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={
                "model": GROQ_SCORER_MODEL,
                "messages": [
                    {"role": "system", "content": SCORER_SYSTEM},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0,
                "max_tokens": SCORER_MAX_TOKENS,
            },
            timeout=300,
        )
        if resp.status_code == 429:
            wait = 15 * (attempt + 1)
            print(f"rate limited, waiting {wait}s...", end=" ", flush=True)
            await asyncio.sleep(wait)
            continue
        resp.raise_for_status()
        text = resp.json()["choices"][0]["message"]["content"]
        return _extract_json(text)
    resp.raise_for_status()  # final attempt, let it raise


async def _score_anthropic(user_prompt: str) -> dict:
    """Score using Anthropic API."""
    import anthropic

    client = anthropic.AsyncAnthropic()
    result = await client.messages.create(
        model=ANTHROPIC_SCORER_MODEL,
        max_tokens=SCORER_MAX_TOKENS,
        temperature=0,
        system=SCORER_SYSTEM,
        messages=[{"role": "user", "content": user_prompt}],
    )
    text = result.content[0].text
    return _extract_json(text)


async def score_response(
    client: httpx.AsyncClient,
    problem_statement: str,
    success_criteria: str,
    response_text: str,
) -> dict:
    """Score a single response blindly."""
    user_prompt = (
        f"## Problem\n{problem_statement}\n\n"
        f"## Success Criteria\n{success_criteria}\n\n"
        f"## Response to Evaluate\n{response_text}\n\n"
        f"## Scoring Rubric\n{SCORER_RUBRIC}"
    )

    if SCORER_BACKEND == "ollama":
        return await _score_ollama(client, user_prompt)
    elif SCORER_BACKEND == "vllm":
        return await _score_vllm(client, user_prompt)
    elif SCORER_BACKEND == "groq":
        return await _score_groq(client, user_prompt)
    else:
        return await _score_anthropic(user_prompt)


async def score_problem_results(problem_result: dict) -> dict:
    """Score all vanilla and reframed responses for one problem."""
    problem_statement = problem_result["vanilla"][0]["prompt"]
    success_criteria = problem_result["success_criteria"]

    print(f"\n  Scoring: {problem_result['problem_title']}")

    async with httpx.AsyncClient() as client:
        vanilla_scores = []
        for i, run in enumerate(problem_result["vanilla"]):
            print(f"    vanilla run {i+1}...", end=" ", flush=True)
            scores = await score_response(
                client, problem_statement, success_criteria, run["response"]
            )
            vanilla_scores.append(scores)
            print("done")
            await asyncio.sleep(4)

        reframed_scores = []
        for i, run in enumerate(problem_result["reframed"]):
            print(f"    reframed run {i+1}...", end=" ", flush=True)
            scores = await score_response(
                client, problem_statement, success_criteria, run["response"]
            )
            reframed_scores.append(scores)
            print("done")
            await asyncio.sleep(4)

    scored = {
        **problem_result,
        "vanilla_scores": vanilla_scores,
        "reframed_scores": reframed_scores,
    }

    # Overwrite with scores added
    output_path = RAW_DIR / f"{problem_result['problem_id']}.json"
    output_path.write_text(json.dumps(scored, indent=2, ensure_ascii=False))
    print(f"    Saved scores: {output_path}")

    return scored


async def score_all(problem_ids: list[str] | None = None) -> list[dict]:
    """Score all results on disk."""
    from .runner import load_results

    results = load_results(problem_ids)
    scored = []
    for result in results:
        if result.get("study") == "deo":
            continue  # Skip DEO files — use deo_scorer for those
        s = await score_problem_results(result)
        scored.append(s)
    return scored
