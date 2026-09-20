"""Strands agent: NL physics belief -> {sceneType, params, prediction, explanation}.

One @tool per scene type (see /shared/scene-registry.json). Each tool extracts
BOTH the scenario parameters AND the student's predicted outcome — the richer
extraction task that makes predict-observe-explain work (PLAN.md), not just
parameter extraction.

Model: Ollama for offline-safe dev; confirm the Bedrock swap before the demo
(PLAN.md, Module 2's "confirm Bedrock swap before demo").

NOTE: the exact Strands Agents SDK call shape (Agent(...), tool_results, etc.)
below is a best-effort scaffold — confirm it against the current docs at
https://strandsagents.com before relying on it; the SDK is young and moves
fast. The @tool function signatures and _build_spec plumbing are the stable
part of this file.
"""
from __future__ import annotations

from typing import TypedDict

from strands import Agent, tool
from strands.models.ollama import OllamaModel

from content_loader import load_explanation


class ScenePrediction(TypedDict):
    sceneType: str
    params: dict
    prediction: dict
    explanation: dict


def _build_spec(scene_type: str, params: dict, claim: str, expected_outcome: str) -> ScenePrediction:
    return {
        "sceneType": scene_type,
        "params": params,
        "prediction": {"claim": claim, "expectedOutcome": expected_outcome},
        "explanation": load_explanation(scene_type),
    }


@tool
def free_fall(massA: float, massB: float, dragEnabled: bool, claim: str, expectedOutcome: str) -> ScenePrediction:
    """Extract a free-fall (two masses) scenario plus the student's predicted outcome."""
    return _build_spec("free-fall", {"massA": massA, "massB": massB, "dragEnabled": dragEnabled}, claim, expectedOutcome)


@tool
def pendulum(length: float, angle: float, gravity: float, smallAngleApprox: bool, claim: str, expectedOutcome: str) -> ScenePrediction:
    """Extract a pendulum scenario plus the student's predicted outcome."""
    params = {"length": length, "angle": angle, "gravity": gravity, "smallAngleApprox": smallAngleApprox}
    return _build_spec("pendulum", params, claim, expectedOutcome)


# TODO(Module 2): projectile, circular_motion, elastic_collision, spring_shm —
# same pattern. Param names/types must match the `if/then` block for that
# sceneType in /shared/scene-spec.schema.json exactly, or validate.py rejects
# the output.

_TOOLS = [free_fall, pendulum]

_SYSTEM_PROMPT = """\
You are extracting structured data from a high-school student's physics belief.
Pick ONE scene tool that matches what they described, and call it with:
  - the scenario parameters (reasonable defaults for anything unstated)
  - claim: the student's belief, in their own words
  - expectedOutcome: what that belief implies will happen, phrased so it can be
    checked against the real simulation
Never generate simulation code. Never invent a misconception — that comes from
a fixed catalogue elsewhere. Only extract scenario + prediction.
See /content/partyrock-prompt.md for phrasings this was prototyped against.
"""


def _build_agent() -> Agent:
    model = OllamaModel(model_id="llama3.1")  # TODO: swap for a BedrockModel before the demo
    return Agent(model=model, tools=_TOOLS, system_prompt=_SYSTEM_PROMPT)


def run_prediction_agent(text: str, retry_hint: str | None = None) -> dict:
    agent = _build_agent()
    prompt = text if not retry_hint else f"{text}\n\n(Previous attempt was invalid: {retry_hint}. Fix and retry.)"
    result = agent(prompt)
    tool_results = getattr(result, "tool_results", None)
    if not tool_results:
        return {}
    return tool_results[-1]
