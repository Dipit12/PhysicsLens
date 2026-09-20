from __future__ import annotations

import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from cedar_authz import (  # noqa: E402
    is_authoring_allowed,
    is_lens_allowed,
    validate_policy_set,
)


def test_policies_validate_against_schema():
    validate_policy_set()


@pytest.mark.parametrize(
    "role,lens,allowed",
    [
        ("student", "intuition", True),
        ("student", "formal", False),
        ("major", "intuition", True),
        ("major", "formal", True),
        ("teacher", "intuition", True),
        ("teacher", "formal", True),
    ],
)
def test_lens_gating(role: str, lens: str, allowed: bool):
    assert is_lens_allowed(role, lens) is allowed


@pytest.mark.parametrize(
    "role,allowed",
    [
        ("student", False),
        ("major", False),
        ("teacher", True),
    ],
)
def test_authoring_is_teacher_only(role: str, allowed: bool):
    assert is_authoring_allowed(role) is allowed
