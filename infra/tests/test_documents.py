from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from documents import build_retrieve_query, build_scene_documents  # noqa: E402

REQUIRED = {
    "sceneType",
    "displayName",
    "misconceptionTag",
    "syllabusUnit",
    "misconception",
    "examplePredictions",
}


def test_one_document_per_canonical_scene():
    docs = build_scene_documents()
    ids = [d["sceneType"] for d in docs]
    assert ids == [
        "free-fall",
        "projectile",
        "pendulum",
        "circular-motion",
        "elastic-collision",
        "spring-shm",
    ]
    for doc in docs:
        assert REQUIRED <= set(doc)
        assert doc["examplePredictions"]
        assert doc["misconception"]


def test_retrieve_query_targets_prediction_fields():
    query = build_retrieve_query("heavier ball falls faster", k=3)
    assert query["size"] == 3
    fields = query["query"]["multi_match"]["fields"]
    assert any(f.startswith("examplePredictions") for f in fields)
    assert any(f.startswith("misconceptionTag") for f in fields)
