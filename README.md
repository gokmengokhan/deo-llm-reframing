# Distance-Engagement Oscillation in LLM Prompting

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19252225.svg)](https://doi.org/10.5281/zenodo.19252225)

Replication materials for the paper:

> **Gokmen, G. (2026).** *Does AI Dream of Electric Sheep? Testing Distance-Engagement Oscillation as a Prompting Framework for Creative Reframing in Large Language Models.*

## What this study tests

Perceptual Reframing Theory (PRT; Gokmen, submitted) identifies nine cognitive paths through which humans shift perception during creative problem-solving, and proposes Distance-Engagement Oscillation (DEO) as the mechanism that makes those shifts durable. This study translates the theory into LLM prompting strategies and tests two questions:

1. **Do reframing paths improve LLM reasoning?** (Analysis 1: vanilla vs. path-guided prompting across 50 problems)
2. **Does oscillation between distance and engagement outperform either mode alone?** (Analysis 2: four-condition comparison across 20 pure-distance-path problems)

## Key findings

The predicted ordering **DEO > Distance > Engagement > Vanilla** held across all 3 models and all 3 scorers (9/9 combinations, all p < .001). Effect sizes were very large (Cohen's d = 1.29-1.63 for Analysis 1).

## Experiment design

- **50 novel problems** across 8 categories of perceptual lock-in
- **3 open-weight LLMs**: Llama 3.3 70B, Qwen3 32B, Llama 4 Scout 17B-16E
- **4 conditions**: vanilla (control), distance-only, engagement-only, DEO (oscillation)
- **5 runs per condition** (temperature 0.7) averaged to reduce variance
- **3 independent scorers**: self-scoring + Claude Sonnet 4 + GPT-4.1 (all blind to condition)
- **5-dimension rubric**: frame diversity, assumption surfacing, solution novelty, premise questioning, correctness
- All generation via Groq API; zero-shot, prompt-level intervention only

## Repository structure

```
deo-llm-reframing/
├── src/reframing_ai/
│   ├── problems.py          # 50 problem definitions with all condition preambles
│   ├── deo_problems.py      # 10 DEO-specific problem configurations
│   ├── runner.py             # Study 1 execution engine
│   ├── deo_runner.py         # Study 2 execution engine
│   ├── scorer.py             # Self-scoring logic
│   ├── cross_scorer.py       # Claude/GPT-4.1 cross-scoring
│   ├── config.py             # API and model configuration
│   └── ...                   # Report generation, prompts
│
├── results/                  # Raw experiment outputs (307 JSON files)
│   ├── llama/raw/            # Llama 3.3 70B responses + scores
│   ├── qwen/raw/             # Qwen3 32B responses + scores
│   └── llama4scout/raw/      # Llama 4 Scout responses + scores
│
├── paper/
│   ├── study1_data.csv       # Flattened data for analysis
│   ├── study2_data.csv       # Four-condition data
│   ├── stats_results.md      # Full statistical results
│   ├── figures/              # Publication figures (PNG + PDF)
│   └── tables/               # Summary tables
│
├── run_experiment.py         # Run Study 1 (vanilla vs. reframing)
├── run_deo.py                # Run Study 2 (four-condition DEO)
├── run_full.py               # Run both studies across multiple models
├── run_stats.py              # Statistical analysis (Python)
├── run_cross_score.py        # Cross-model scoring
├── export_for_r.py           # Export data for R verification
├── generate_figures.py       # Publication figures
└── verify_stats.R            # Independent R verification of all statistics
```

## Reproducing the experiment

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- API keys for Groq, Anthropic, and OpenAI

### Setup

```bash
git clone https://github.com/gokmengokhan/deo-llm-reframing.git
cd deo-llm-reframing
cp .env.example .env
# Edit .env with your API keys
uv sync
```

### Run experiments

```bash
# Study 1: vanilla vs. reframing (single model)
uv run python run_experiment.py

# Study 2: four-condition DEO comparison
uv run python run_deo.py

# Both studies across all models
uv run python run_full.py --models llama qwen llama4scout

# Cross-score with Claude and GPT-4.1
uv run python run_cross_score.py
```

### Run analysis

```bash
# Statistical analysis (Python)
uv run python run_stats.py

# Export for R verification
uv run python export_for_r.py

# Independent R verification
Rscript verify_stats.R

# Generate publication figures
uv run python generate_figures.py
```

### Cost estimate

The full experiment (3 models, 4 conditions, 5 runs, 3 scorers) costs approximately $15-20 USD across the Groq, Anthropic, and OpenAI APIs.

## Data format

Each JSON file in `results/` contains:
- Problem metadata (id, category, theory connection, success criteria)
- Full LLM responses for each condition (5 runs each)
- Blind scores from each scorer (5 dimensions + correctness with justifications)
- Token counts and generation times

The `paper/*.csv` files contain the same data flattened for statistical analysis, with one row per model-problem-condition-scorer-run combination.

## Citation

If you use this dataset or methodology, please cite:

```bibtex
@misc{gokmen2026deo,
  title={Does {AI} Dream of Electric Sheep? Testing Distance-Engagement Oscillation in {LLM} Creative Reframing},
  author={G{\"o}kmen, G{\"o}khan},
  year={2026},
  doi={10.5281/zenodo.19252225},
  url={https://zenodo.org/records/19252225},
  publisher={Zenodo}
}
```

## License

CC BY 4.0. See [LICENSE](LICENSE).
