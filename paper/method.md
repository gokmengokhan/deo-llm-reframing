# Method

## Overview

We conducted a single experiment to test whether Perceptual Reframing Theory (PRT), originally developed to explain how shifts in human perception enable creative problem-solving (Gokmen, 2025), can improve large language model (LLM) reasoning when translated into prompting strategies. The experiment uses a within-model, between-conditions design with four prompting conditions applied to 50 novel problems across three LLMs.

The experiment addresses two research questions through two analyses of the same data:

- **Analysis 1 — Path Effectiveness:** Do the nine theory-derived reframing paths improve LLM output quality when translated into prompting strategies? This compares the vanilla (control) condition against the path-guided (reframing) condition across all 50 problems.
- **Analysis 2 — DEO Mechanism:** Does Distance-Engagement Oscillation — systematically alternating between analytical detachment and immersive engagement — outperform either cognitive mode in isolation? This compares all four conditions across the 20 problems assigned exclusively to pure distance-mode paths, where the distance/engagement/DEO distinction is theoretically clean (see Path-Mode Classification).

The design is zero-shot, prompt-level intervention only. No fine-tuning, no retrieval augmentation, no tool use, and no change to model parameters or weights. The only experimental variable is the framing instruction prepended to the problem text. This directly operationalises PRT's core claim: *the shift is a change in representation, not a change in information* — the model receives identical factual content across all conditions.

---

## Participants (Subject Models)

Three open-weight, instruction-tuned LLMs served as subjects. All were accessed via the Groq API (Groq, Inc.) to ensure uniform inference conditions.

| Model | Groq identifier | Parameters | Architecture | Developer |
|-------|----------------|-----------|-------------|-----------|
| Llama 3.3 70B Instruct | `llama-3.3-70b-versatile` | 70B | Dense decoder-only transformer | Meta |
| Qwen3 32B | `qwen/qwen3-32b` | 32B | Dense decoder-only transformer | Alibaba |
| Llama 4 Scout 17B 16E Instruct | `meta-llama/llama-4-scout-17b-16e-instruct` | 17B active / 109B total | Mixture-of-experts (16 experts) | Meta |

No proprietary or closed-source models were used as subjects, ensuring full reproducibility. The three models were selected to vary along three dimensions: parameter count (70B, 32B, 17B active), training lineage (two Meta models, one Alibaba model), and architecture (two dense transformers, one mixture-of-experts). If the effects of reframing hold across all three, the result cannot be attributed to a single model family or architecture.

### Generation Parameters

All generation calls used the following parameters:
- **Temperature:** 0.7 (non-zero to introduce stochastic variation across runs)
- **Maximum output tokens:** 2,048
- **System prompt:** *"You are a helpful assistant. Think carefully about the problem presented and provide a thorough, well-reasoned response."*

The system prompt was held constant across all conditions to ensure that only the user-facing framing instruction varied.

---

## Experimental Conditions

Each problem was presented to each model under four conditions. The conditions form a 2×2 conceptual structure crossing the presence of analytical distance (absent vs. present) with the presence of immersive engagement (absent vs. present):

|  | No engagement | Engagement |
|--|--------------|------------|
| **No distance** | Vanilla (control) | Engagement-only |
| **Distance** | Distance-only | DEO (both) |

### Condition 1: Vanilla (Control)

The problem text was preceded by a generic step-by-step instruction:

> *"Think about this problem step by step. Consider the key factors involved, weigh the options carefully, and provide your best recommendation."*

This preamble matches the instructional register of the experimental conditions without providing any reframing intervention. It serves as the baseline against which all other conditions are compared.

### Condition 2: Distance-Only

The problem text was preceded by a theory-derived analytical reframing instruction specific to the type of perceptual lock-in the problem was designed to trigger. These instructions are third-person, abstract, and analytical. They implement one or more of the nine reframing paths from PRT, translated into natural language prompting strategies. Examples include:

- *"Before answering, do NOT use the word 'container' to describe these objects. Instead, describe each physical component by its material properties only..."* (Path 2: Decompose to Generic)
- *"List every assumption embedded in the way this problem is stated..."* (Path 1: Name the Frame)
- *"How would you guarantee the worst outcome? Describe the most counterproductive approach in detail, then invert it..."* (Path 5: Invert the Problem)

Each distance-only preamble was hand-crafted for the specific problem, rather than using a single generic template, to ensure that the reframing intervention targets the particular lock-in type each problem was designed to trigger.

### Condition 3: Engagement-Only

The problem text was preceded by an immersive, first-person instruction. The model was placed in the role of a specific named character within the scenario and asked what they feel, see, and need. These preambles contain no analytical distancing — no assumption-listing, no stepping back, no third-person abstraction. Example:

> *"You are the logistics coordinator for the disaster relief organisation. It is hour 6 of a 72-hour window. You are standing in the port yard watching 500 people arrive — families with children, elderly people, a mother holding an infant. [...] What do you feel when you look at those containers? What do you see?"*

This condition isolates the engagement component to test whether immersive perspective-taking alone improves reasoning, or whether it merely produces more vivid elaboration within the same frame.

### Condition 4: DEO (Distance-Engagement Oscillation)

The problem text was preceded by a four-step oscillation instruction that alternates between cognitive modes:

1. **ANALYSE** (distance): Analytical examination — decomposing assumptions, listing material properties, or inverting the problem. Uses the same reframing path as the distance-only condition for that problem.
2. **FEEL** (engagement): *"Now imagine you are [named character]... What does it feel like? What do you reach for — and why?"*
3. **REFRAME** (distance): *"Given what you discovered AND what you felt, what is the REAL question?"*
4. **ENVISION** (engagement): *"Describe vividly what it looks like if the reframed understanding is acted upon."*

The DEO condition operationalises the theory's core mechanism: the oscillation between seeing the frame (distance) and feeling the shift (engagement). Crucially, the REFRAME step synthesises insights from both modes — it asks the model to integrate the analytical decomposition from Step 1 with the felt experience from Step 2 — producing a re-representation that neither mode could achieve alone.

### Condition Coverage

Of the 50 problems, 46 support all four conditions (vanilla, distance, engagement, DEO). Four problems use a multi-turn follow-up mechanism rather than a preamble to deliver the reframing intervention (see Multi-Turn Problems below); because this mechanism is incompatible with the single-turn engagement and DEO preamble structure, these four are included in Analysis 1 (vanilla vs. distance) but excluded from Analysis 2 (four-condition comparison).

---

## Problem Design

### Construction Principles

Fifty problems were designed specifically for this experiment. Each problem targets a specific type of perceptual lock-in identified in the cognitive science literature and is constructed to:

1. **Trigger a predictable failure mode** in vanilla (step-by-step) prompting — i.e., the problem's surface framing should lead a model to "solve" it without questioning the embedded assumptions.
2. **Be novel** — avoid scenarios present in common LLM training and benchmark datasets (e.g., the candle problem, nine-dot problem, trolley problem) to reduce the likelihood that models have memorised reframing solutions.
3. **Be ecologically valid** — each problem includes a detailed scenario with specific numbers, names, organisational contexts, and constraints, resembling real-world decision-making situations rather than abstract puzzles.
4. **Have clear success criteria** — each problem specifies what a successful response looks like, enabling reliable scoring.

### Categories

The 50 problems span eight categories, each targeting a distinct type of perceptual lock-in:

| Category | *n* | Lock-in type | Key references |
|----------|-----|-------------|----------------|
| Functional fixedness | 6 | Object labels suppress alternative functions | Duncker, 1945; McCaffrey, 2012 |
| Framing traps | 6 | Anchoring to the frame embedded in the question | Tversky & Kahneman, 1981; Ledgerwood & Boydstun, 2014 |
| Einstellung (mental set) | 6 | Familiar methods block simpler solutions | Luchins, 1942; Dane, 2010 |
| False binary / assumption-laden | 7 | Accepting a false premise without questioning it | Ohlsson, 1984; Argyris & Schon, 1978 |
| Multi-turn reframing | 6 | Lock-in requiring temporal or reflective intervention | Wallas, 1926; Weick, 1995; Tulver et al., 2023 |
| Zero-sum framing | 6 | Distributive framing obscuring integrative solutions | Tversky & Kahneman, 1981; De Brabandere, 2005 |
| Anchoring traps | 6 | Irrelevant numeric anchors distorting reasoning | Kahneman, 2011; Clark, 2013 |
| Narrative lock-in | 7 | Dominant metaphors constraining the solution space | Goffman, 1974; Mezirow, 1990 |

### Reframing Path Mapping

Each problem's distance-only condition implements one or more of the nine reframing paths from PRT, translated into prompting language. Of the 50 problems, 36 activate multiple paths (typically two); the remaining 14 activate a single path. Path 6 (Premise Reflection) appears most frequently because questioning the problem's premise is relevant across all lock-in types.

| Path | Prompting translation | *n* problems |
|------|----------------------|-------------|
| Path 1: Name the Frame | *"List every assumption embedded in..."* | 18 |
| Path 2: Decompose to Generic | *"Describe by material properties, not function..."* | 10 |
| Path 3: Bridge Distant Analogy | *"Find structurally similar problems in different domains..."* | 9 |
| Path 4: Incubate / Reset | Multi-turn: *"Set aside your previous answer. Approach fresh."* | 2 |
| Path 5: Invert the Problem | *"How would you guarantee the worst outcome?"* | 11 |
| Path 6: Reflect on the Premise | *"Is this the right question? What is the problem behind the problem?"* | 23 |
| Path 7: Surprise as Signal | Multi-turn: *"What is most surprising about your own answer?"* | 3 |
| Path 8: Confidence Calibration | *"Rate confidence 1–10 for each claim. Reconsider claims below 7."* | 2 |
| Path 9: Step Outside | *"Answer from multiple named perspectives..."* | 8 |

*Note:* Counts exceed 50 because most problems activate multiple paths.

### Path-Mode Classification

Not all nine paths operate through the same cognitive mode. On closer analysis, the paths fall into three categories:

| Mode | Paths | Mechanism | *n* problems |
|------|-------|-----------|-------------|
| **Distance** | 1, 2, 3, 4, 5, 9 | Analytical detachment: decomposing, inverting, stepping back, bridging analogies | 22 |
| **Hybrid** | 6, 7 | Inherently dual-mode: premise reflection (Path 6) is a cognitive act that triggers Mälkki's (2010) edge emotions; surprise-as-signal (Path 7) is a felt prediction error that must be analytically interpreted | 26 |
| **Engagement** | 8 | Emotionally felt insight: confidence calibration surfaces uncertainty as a felt metacognitive signal rather than through analytical decomposition | 2 |

This classification has consequences for the experimental design. In Analysis 1 (vanilla vs. distance), all 50 problems are included regardless of path mode — the question is simply whether reframing paths improve output quality. However, in Analysis 2 (four-condition DEO comparison), path mode matters: for hybrid-path problems, the "distance" condition already partially activates engagement, blurring the boundary between conditions; for engagement-path problems, the "distance" condition is actually an engagement operation, and the DEO condition becomes engagement-followed-by-engagement rather than genuine oscillation. Analysis 2 is therefore restricted to the 20 problems assigned to pure distance-mode paths (see Analysis Plan).

### Multi-Turn Problems

Four of the six problems in the multi-turn category use a two-turn conversational mechanism rather than a single-turn preamble. In these problems, the reframing intervention is delivered as a follow-up message after the model has already committed to an initial response:

- **Path 4 — Incubate / Reset** (2 problems): The model first generates a response under vanilla prompting. A follow-up message then instructs: *"Set aside your previous answer entirely. Approach this completely fresh — as if you had never seen the problem before."* The second response is scored.
- **Path 7 — Surprise as Signal** (2 problems): The model first generates a response under vanilla prompting. A follow-up message then asks: *"What is the most surprising thing about your own answer? What assumption does that surprise reveal? Now revise your answer."* The second response is scored.

The remaining two multi-turn problems (implementing Path 8: Confidence Calibration) are structured as single-turn preambles and therefore support all four conditions.

---

## Theoretical Predictions

The Distance-Engagement Oscillation hypothesis generates a specific, falsifiable ordering of the four conditions:

**DEO > Distance-only > Vanilla ≥ Engagement-only**

This prediction follows from PRT's claim that (a) analytical distance is necessary to *see* the frame, (b) immersive engagement is necessary to *feel* the shift, and (c) neither alone is sufficient — the oscillation between the two is the mechanism that produces genuine re-representation.

The predicted ordering is unique to the oscillation hypothesis. Competing accounts from the traditions PRT synthesises would predict different orderings:

| Theory | Predicted ordering | Rationale |
|--------|--------------------|-----------|
| Ohlsson (cognitive restructuring) | Distance ≥ DEO > Engagement | Cognition drives insight; engagement is noise |
| Tulver et al. (emotional insight) | Engagement ≥ DEO > Distance | Affect drives lasting change |
| Kross & Ayduk (self-distancing) | Distance > DEO > Engagement | Distance is the active ingredient; adding engagement dilutes it |
| **PRT / DEO (this paper)** | **DEO > Distance > Vanilla ≥ Engagement** | **Oscillation is the mechanism; engagement alone = elaboration within the frame** |

The critical differentiating predictions are: (a) DEO outperforms distance-only (ruling out distance as the sole active ingredient), and (b) engagement-only underperforms distance-only (ruling out engagement as independently beneficial). If both hold across multiple models, the result cannot be explained by any single tradition and supports the oscillation hypothesis specifically.

---

## Runs and Sampling

Each problem-condition pair was run **five times** (temperature 0.7), yielding five independent responses per condition per problem per model. All reported scores are averages across the five runs, reducing the influence of single-sample variance.

### Total Generation Calls

| | Analysis 1 (50 problems × 2 conditions) | Analysis 2 (20 problems × 4 conditions) | Unique calls per model |
|--|----------------------------------------|----------------------------------------|----------------------|
| Generation calls | 500 | 400 | 900 |
| × 5 runs | 2,500 | 2,000 | 4,500 |

With three models, the experiment required **13,500 generation calls** in total for the primary analyses. An additional 26 problems support all four conditions but are excluded from Analysis 2 due to path-mode classification (see Path-Mode Classification); their data is retained for supplementary analysis. Multi-turn problems require two API calls per run (initial response + follow-up), adding a small number of additional calls to the totals above.

---

## Scoring

### Rubric

Each response was scored on five dimensions using a 1–5 scale with anchored descriptions at each point. The first four dimensions capture the qualities that PRT predicts should improve under reframing conditions; the fifth (correctness) serves as a quality control measure.

| Dimension | Description | 1 (low) | 5 (high) |
|-----------|-------------|---------|----------|
| **Frame diversity** | How many distinct frames or perspectives the response explores | Single frame only | Four or more frames explored with synthesis |
| **Assumption surfacing** | Whether hidden assumptions are identified and examined | No assumptions identified | Systematically surfaces and examines hidden assumptions |
| **Solution novelty** | Whether solutions go beyond the obvious first-order answer | Only the most conventional response | Genuinely unexpected viable solution that reframes the problem |
| **Premise questioning** | Whether the problem itself is questioned as well-posed | Accepts the problem exactly as stated | Fundamentally reframes the question before answering |
| **Correctness** | Whether the response is factually accurate and practically useful | Factually wrong or useless | Excellent practical advice grounded in reality |

The **reframing score** (primary dependent variable) is the unweighted mean of the first four dimensions: frame diversity, assumption surfacing, solution novelty, and premise questioning. **Correctness** is reported separately to verify that reframing does not degrade response quality — a critical concern, since an intervention that improves creativity at the expense of accuracy would not constitute genuine improvement.

### Scoring Protocol

Three independent scoring procedures were applied to every response, yielding three complete sets of scores per model:

**1. Self-scoring (within-family).** Each subject model scored its own outputs. Llama 3.3 70B scored all Llama responses; Qwen3 32B scored all Qwen responses; Llama 4 Scout scored all Scout responses. All self-scoring was performed via the Groq API at temperature 0 for determinism.

**2. Claude Sonnet cross-scoring (cross-family).** All responses from all three subject models were scored by Claude Sonnet 4 (Anthropic), accessed via the Anthropic API (`claude-sonnet-4-20250514`). Temperature 0.

**3. GPT-4.1 cross-scoring (cross-family).** All responses from all three subject models were scored by GPT-4.1 (OpenAI), accessed via the OpenAI API. Temperature 0.

The use of three independent scorers — one within-family (same model) and two cross-family (different model, different developer) — allows us to distinguish genuine effects from scorer-specific biases. If the same ordering (DEO > Distance > Engagement > Vanilla) holds across all three scorers for a given subject model, the result is unlikely to be an artefact of any single scorer's preferences.

### Blind Scoring

All scoring was performed blind to condition. Each scorer received:

1. The problem statement (identical across conditions)
2. The success criteria for the problem
3. The response to evaluate
4. The scoring rubric with anchored descriptions

The scorer did **not** receive: the condition label (vanilla, distance, engagement, or DEO), the framing preamble, or any indication of which condition produced the response. This ensures that scorers evaluated the quality of the response itself, not the quality of the prompt that produced it.

### Scorer Prompt Structure

The scorer received a structured evaluation prompt:

```
## Problem
[problem statement]

## Success Criteria
[success criteria for this problem]

## Response to Evaluate
[the model's response — no condition label]

## Scoring Rubric
[full rubric with 1–5 anchored descriptions for each dimension]
```

The scorer was instructed to return structured JSON with a numeric score and brief justification for each dimension:

```json
{
  "frame_diversity": {"score": N, "justification": "..."},
  "assumption_surfacing": {"score": N, "justification": "..."},
  "solution_novelty": {"score": N, "justification": "..."},
  "premise_questioning": {"score": N, "justification": "..."},
  "correctness": {"score": N, "justification": "..."}
}
```

### Fallback for Malformed Scoring Output

Responses that produced malformed JSON from the scorer were retried up to three times. If all retries failed, neutral scores (3 on all dimensions) were assigned to avoid data loss. The neutral score of 3 was chosen because it is the midpoint of the 1–5 scale, introducing no directional bias. The incidence of neutral fallbacks was tracked and is reported in the results.

### Self-Scoring Limitations

Self-scoring — using the same model family to evaluate its own outputs — is a recognised limitation. The model may favour responses that match its own generation patterns, or may lack the discriminative capacity to detect subtle differences between conditions. We mitigate this limitation through three mechanisms:

1. **Blind presentation** — condition labels are withheld from the scorer.
2. **Cross-family validation** — Claude Sonnet and GPT-4.1, trained by different organisations on different data, provide independent assessments. If all three scorers agree on the condition ordering, model-specific scoring bias cannot explain the result.
3. **Three subject models** — if the same pattern holds across Llama, Qwen, and Scout (each self-scoring independently), the consistency across model families further reduces the likelihood of a scorer-specific artefact.

---

## Analysis Plan

### Primary Dependent Variable

For each of the 50 problems, we compute the **reframing score** — the unweighted mean of frame diversity, assumption surfacing, solution novelty, and premise questioning — under each condition, averaged across the five runs. This yields one score per problem per condition per model per scorer. All inferential tests operate on these problem-level means (*n* = 50 for Analysis 1, *n* = 20 for Analysis 2).

### Analysis 1: Path Effectiveness (Vanilla vs. Reframing)

The primary comparison is a paired test across 50 problems (vanilla vs. path-guided reframing). All nine paths are included regardless of their mode classification, since the question is whether the reframing prompts improve output quality, not which cognitive mode drives the improvement. We first assess normality of the difference scores with the Shapiro-Wilk test. The primary inferential test is the **Wilcoxon signed-rank test** (two-sided), which does not assume normality; we additionally report the **paired *t*-test** as a parametric complement. Effect size is reported as **Cohen's *d*** for paired samples (mean difference divided by the standard deviation of the differences).

We report:

1. **Mean improvement** (reframing minus vanilla) across all 50 problems, per model and per scorer, with Wilcoxon *p*-values and Cohen's *d*.
2. **Per-category improvement** — mean improvement within each of the eight lock-in categories, with within-category Wilcoxon tests and effect sizes.
3. **Per-path effectiveness** — mean improvement for each of the nine reframing paths, with Wilcoxon tests where sample size permits (*n* ≥ 6).
4. **Consistency across models** — whether the direction and magnitude of improvement hold across Llama 70B, Qwen 32B, and Scout 17B.
5. **Consistency across scorers** — whether self-scoring, Claude, and GPT-4.1 agree on the direction and relative magnitude.
6. **Correctness comparison** — paired *t*-test on correctness scores to verify that the reframing condition does not degrade response quality.

### Analysis 2: DEO Mechanism (Four-Condition Comparison)

Analysis 2 is restricted to the **20 problems assigned exclusively to pure distance-mode paths** (Paths 1–5 and 9). This restriction ensures that the four conditions — vanilla, distance, engagement, and DEO — correspond to theoretically distinct cognitive operations:

- **Vanilla** = no reframing mode
- **Distance** = genuine analytical detachment (decomposing, inverting, stepping back)
- **Engagement** = genuine immersive engagement (first-person perspective-taking)
- **DEO** = genuine oscillation between distance and engagement

For hybrid-path problems (Paths 6, 7), the distance condition already partially activates engagement, blurring the distance/engagement boundary. For engagement-path problems (Path 8), the distance condition is an engagement operation, and the DEO condition collapses into engagement-followed-by-engagement rather than true oscillation. Including these problems would contaminate the test of the oscillation hypothesis. The full set of 46 DEO-eligible problems (including hybrid and engagement paths) is reported as supplementary analysis.

For each of the 20 qualifying problems, we compute the reframing score under all four conditions. The omnibus test is the **Friedman test** (non-parametric repeated measures across four conditions). Where the Friedman test is significant, we conduct **post-hoc pairwise Wilcoxon signed-rank tests** for all six condition pairs, with **Holm-Bonferroni correction** for multiple comparisons within each model × scorer combination.

The primary tests are:

1. **Ordering test** — does the observed mean ordering match the predicted DEO > Distance > Engagement > Vanilla?
2. **DEO advantage** — is the pairwise difference between DEO and distance-only significant after Holm-Bonferroni correction? This is the critical test for the oscillation hypothesis.
3. **Engagement deficit** — is distance-only significantly greater than engagement-only? This rules out the alternative hypothesis that engagement is independently beneficial.
4. **Cross-model consistency** — does the ordering hold for all three models?
5. **Cross-scorer consistency** — does the ordering hold for all three scorers (self, Claude, GPT-4.1)?

Effect sizes (Cohen's *d*) are reported for all pairwise comparisons. We classify effects as small (|*d*| ≥ 0.2), medium (|*d*| ≥ 0.5), large (|*d*| ≥ 0.8), or very large (|*d*| ≥ 1.2).

The combination of (2) and (3) is the critical differentiating test. If DEO > Distance AND Distance > Engagement (both significant after correction), the result rules out both "distance is sufficient" and "engagement is independently helpful" explanations, supporting the oscillation hypothesis specifically.

### Software and Verification

All analyses were implemented in Python (NumPy, SciPy) and independently verified in R (base `stats` package with `wilcox.test`, `friedman.test`, `shapiro.test`, and `p.adjust` with `method = "holm"`). The two implementations produced concordant results across all 9 model × scorer combinations.

---

## Reproducibility

All code, problem definitions (including the full text of all 50 problems with all four condition preambles), prompt templates, scoring rubrics, and complete raw results (including full response texts, token counts, and individual scorer justifications) are available at [repository URL]. The experiment can be replicated using the Groq API with the model identifiers specified above, or any OpenAI-compatible inference endpoint serving the same models. Total cost for the complete experiment (three models, all conditions, five runs, three scorers) was approximately $15–20 USD (Groq API for generation and self-scoring; Anthropic API for Claude cross-scoring; OpenAI API for GPT-4.1 cross-scoring).
