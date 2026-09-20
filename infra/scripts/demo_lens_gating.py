#!/usr/bin/env python3
"""First deliverable for Module 3: student is denied the formal lens; major is allowed.

    cd infra
    python3.12 -m venv .venv && .venv/bin/pip install -r requirements.txt
    .venv/bin/python scripts/demo_lens_gating.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cedar_authz import (  # noqa: E402
    LENSES,
    ROLES,
    is_authoring_allowed,
    is_lens_allowed,
    validate_policy_set,
)


def main() -> int:
    validate_policy_set()
    print("Cedar policy set validated against schema.\n")
    header = f"{'role':<10} {'intuition':<12} {'formal':<12} {'authorPrompt':<12}"
    print(header)
    print("-" * len(header))

    decisions: dict[str, dict[str, bool]] = {}
    for role in ROLES:
        row = {lens: is_lens_allowed(role, lens) for lens in LENSES}
        row["author"] = is_authoring_allowed(role)
        decisions[role] = row
        print(
            f"{role:<10} "
            f"{_label(row['intuition']):<12} "
            f"{_label(row['formal']):<12} "
            f"{_label(row['author']):<12}"
        )

    ok = (
        decisions["student"]["intuition"]
        and not decisions["student"]["formal"]
        and not decisions["student"]["author"]
        and decisions["major"]["intuition"]
        and decisions["major"]["formal"]
        and not decisions["major"]["author"]
        and decisions["teacher"]["intuition"]
        and decisions["teacher"]["formal"]
        and decisions["teacher"]["author"]
    )
    print()
    if ok:
        print("PASS: student denied formal lens; major allowed; teacher can author.")
        return 0
    print("FAIL: lens-gating decisions do not match PLAN.md.")
    return 1


def _label(allowed: bool) -> str:
    return "ALLOW" if allowed else "DENY"


if __name__ == "__main__":
    raise SystemExit(main())
