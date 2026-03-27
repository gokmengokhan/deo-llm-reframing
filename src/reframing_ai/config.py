"""Experiment configuration."""

import os
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = PROJECT_ROOT / "results"
RAW_DIR = RESULTS_DIR / "raw"

# Backend: "ollama", "vllm", "groq", or "anthropic"
SUBJECT_BACKEND = "groq"
SCORER_BACKEND = "groq"

# Groq (free, OpenAI-compatible)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_URL = "https://api.groq.com/openai/v1"
GROQ_SUBJECT_MODEL = "llama-3.3-70b-versatile"
GROQ_SCORER_MODEL = "llama-3.3-70b-versatile"

# Ollama (local)
SUBJECT_MODEL = "llama3.1:8b"
SCORER_MODEL = "llama3.1:8b"
OLLAMA_URL = "http://localhost:11434"

# vLLM (HPC)
VLLM_SUBJECT_MODEL = "Qwen/Qwen2.5-72B-Instruct"
VLLM_SCORER_MODEL = "Qwen/Qwen2.5-72B-Instruct"
VLLM_URL = "http://localhost:8000"

# Anthropic (paid)
ANTHROPIC_SUBJECT_MODEL = "claude-sonnet-4-20250514"
ANTHROPIC_SCORER_MODEL = "claude-opus-4-20250514"

# Experiment parameters
RUNS_PER_CONDITION = 5
TEMPERATURE = 0.7
MAX_TOKENS = 2048
SCORER_MAX_TOKENS = 1024

# Scoring dimensions
SCORING_DIMENSIONS = [
    "frame_diversity",
    "assumption_surfacing",
    "solution_novelty",
    "premise_questioning",
    "correctness",
]
