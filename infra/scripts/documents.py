"""Build OpenSearch documents from the shared registry + Module 4 catalogue.

Infra does not invent curriculum: misconception text comes from
/content/misconceptions.json. Example predictions are retrieval paraphrases
in /infra/opensearch/example-predictions.json.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = REPO_ROOT / "shared" / "scene-registry.json"
MISCONCEPTIONS_PATH = REPO_ROOT / "content" / "misconceptions.json"
EXAMPLES_PATH = REPO_ROOT / "infra" / "opensearch" / "example-predictions.json"
TEMPLATE_PATH = REPO_ROOT / "infra" / "opensearch" / "index-template.json"

INDEX_NAME = "physicslens-scenes"


def load_index_template() -> dict:
    return json.loads(TEMPLATE_PATH.read_text())


def build_scene_documents() -> list[dict]:
    registry = json.loads(REGISTRY_PATH.read_text())
    catalogue = {
        entry["sceneType"]: entry["explanation"]
        for entry in json.loads(MISCONCEPTIONS_PATH.read_text())["scenes"]
    }
    examples = json.loads(EXAMPLES_PATH.read_text())
    documents = []
    missing = []
    for scene in registry["scenes"]:
        scene_id = scene["id"]
        explanation = catalogue.get(scene_id)
        paraphrases = examples.get(scene_id)
        if not explanation or not paraphrases:
            missing.append(scene_id)
            continue
        documents.append(
            {
                "sceneType": scene_id,
                "displayName": scene["displayName"],
                "misconceptionTag": scene["misconceptionTag"],
                "syllabusUnit": scene["syllabusUnit"],
                "misconception": explanation["misconception"],
                "examplePredictions": paraphrases,
            }
        )
    if missing:
        raise ValueError(f"missing catalogue or example predictions for: {missing}")
    return documents


def build_retrieve_query(text: str, k: int = 3) -> dict:
    return {
        "size": k,
        "_source": [
            "sceneType",
            "displayName",
            "misconceptionTag",
            "syllabusUnit",
            "misconception",
        ],
        "query": {
            "multi_match": {
                "query": text,
                "fields": [
                    "examplePredictions^4",
                    "misconceptionTag^3",
                    "misconception^2",
                    "displayName^2",
                    "sceneType",
                    "syllabusUnit",
                ],
                "type": "best_fields",
                "fuzziness": "AUTO",
            }
        },
    }
