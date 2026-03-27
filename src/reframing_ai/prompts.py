"""Prompt builders for vanilla and reframing conditions.

The vanilla condition gets an equal-length non-reframing preamble ("Think step
by step") so that token count is not a confound.
"""

from .problems import Problem

SYSTEM_PROMPT = (
    "You are a helpful assistant. Think carefully about the problem presented "
    "and provide a thorough, well-reasoned response."
)

VANILLA_PREAMBLE = (
    "Think about this problem step by step. Consider the key factors involved, "
    "weigh the options carefully, and provide your best recommendation.\n\n"
)


def build_vanilla(problem: Problem) -> str:
    """Build the vanilla (control) prompt — step-by-step preamble + problem."""
    return VANILLA_PREAMBLE + problem.vanilla_prompt


def build_reframed(problem: Problem) -> str:
    """Build the reframing-enhanced prompt — reframing preamble + problem."""
    return problem.reframing_preamble + problem.vanilla_prompt
