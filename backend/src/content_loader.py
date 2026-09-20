"""Load the explanation payload Module 4 authored for each scene
(/content/misconceptions.json), keyed by sceneType.
"""
from __future__ import annotations

import json
from pathlib import Path
from functools import lru_cache

_PATH = Path(__file__).resolve().parents[2] / "content" / "misconceptions.json"


@lru_cache(maxsize=1)
def _catalogue() -> dict[str, dict]:
    data = json.loads(_PATH.read_text())
    return {entry["sceneType"]: entry["explanation"] for entry in data["scenes"]}


def load_explanation(scene_type: str) -> dict:
    try:
        return _catalogue()[scene_type]
    except KeyError as exc:
        raise KeyError(
            f"No misconceptions.json entry for sceneType={scene_type!r} — "
            "add one before wiring this scene (see /shared/scene-registry.json quad)."
        ) from exc
