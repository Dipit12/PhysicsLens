"""POST /predict — natural-language physics belief -> validated scene spec.

See /shared/scene-spec.schema.json for the contract, PLAN.md for the
first-deliverable curl example this handler must satisfy.
"""
from __future__ import annotations

import json

from agent import run_prediction_agent
from validate import validate_scene_spec


def handler(event, context):
    body = json.loads(event.get("body") or "{}")
    text = (body.get("text") or "").strip()
    if not text:
        return _response(400, {"error": "missing 'text' field"})

    spec = run_prediction_agent(text)
    ok, error = validate_scene_spec(spec)

    if not ok:
        spec = run_prediction_agent(text, retry_hint=error)
        ok, error = validate_scene_spec(spec)
        if not ok:
            return _response(422, {"error": f"agent output failed validation twice: {error}"})

    return _response(200, spec)


def _response(status_code: int, payload: dict):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(payload),
    }
