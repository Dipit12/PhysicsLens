"""Validate an agent-produced scene spec against /shared/scene-spec.schema.json.

CLAUDE.md hard rule: the LLM never generates simulation code, only a spec —
this is the gate that enforces it. PLAN.md: on invalid output, reject and retry
once (see app.py).
"""
from __future__ import annotations

import json
from pathlib import Path

import jsonschema

_SCHEMA_PATH = Path(__file__).resolve().parents[2] / "shared" / "scene-spec.schema.json"
_schema = json.loads(_SCHEMA_PATH.read_text())


def validate_scene_spec(spec: dict) -> tuple[bool, str | None]:
    try:
        jsonschema.validate(spec, _schema)
        return True, None
    except jsonschema.ValidationError as exc:
        return False, exc.message
