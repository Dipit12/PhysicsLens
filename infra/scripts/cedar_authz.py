"""Cedar authorizer for PhysicsLens depth lenses.

Backend (Module 2) can import `is_lens_allowed` once it wires a session role
into POST /predict. This module is the source of truth for the three-lens
gating in PLAN.md.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from cedarpy import Decision, is_authorized, validate_policies

INFRA_ROOT = Path(__file__).resolve().parents[1]
CEDAR_DIR = INFRA_ROOT / "cedar"
POLICY_PATH = CEDAR_DIR / "policies" / "lens-access.cedar"
SCHEMA_PATH = CEDAR_DIR / "schema.cedarschema.json"
ENTITIES_PATH = CEDAR_DIR / "entities.json"

ROLES = ("student", "major", "teacher")
LENSES = ("intuition", "formal")
SESSION_BY_ROLE = {
    "student": "student-session",
    "major": "major-session",
    "teacher": "teacher-session",
}


@lru_cache(maxsize=1)
def _policies() -> str:
    return POLICY_PATH.read_text()


@lru_cache(maxsize=1)
def _schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text())


@lru_cache(maxsize=1)
def _entities() -> list:
    return json.loads(ENTITIES_PATH.read_text())


def validate_policy_set() -> None:
    result = validate_policies(_policies(), _schema())
    if not result.validation_passed:
        errors = "; ".join(str(err) for err in result.errors)
        raise ValueError(f"Cedar policy set failed schema validation: {errors}")


def authorize(principal: str, action: str, resource: str, context: dict | None = None):
    request = {
        "principal": principal,
        "action": action,
        "resource": resource,
        "context": context or {},
    }
    return is_authorized(request, _policies(), _entities(), schema=_schema())


def is_lens_allowed(role: str, lens: str) -> bool:
    if role not in SESSION_BY_ROLE:
        raise ValueError(f"unknown role {role!r}; expected one of {ROLES}")
    session_id = SESSION_BY_ROLE[role]
    result = authorize(
        principal=f'PhysicsLens::Session::"{session_id}"',
        action='PhysicsLens::Action::"viewLens"',
        resource=f'PhysicsLens::Lens::"{lens}"',
    )
    return result.decision == Decision.Allow


def is_authoring_allowed(role: str) -> bool:
    if role not in SESSION_BY_ROLE:
        raise ValueError(f"unknown role {role!r}; expected one of {ROLES}")
    session_id = SESSION_BY_ROLE[role]
    result = authorize(
        principal=f'PhysicsLens::Session::"{session_id}"',
        action='PhysicsLens::Action::"authorPrompt"',
        resource='PhysicsLens::Lens::"author"',
    )
    return result.decision == Decision.Allow
