"""Sanity check: the mock fixtures the frontend already renders from must
validate against the same schema the backend enforces — this is the thing
that keeps Module 1 and Module 2 from drifting apart silently.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from validate import validate_scene_spec  # noqa: E402

FRONTEND_MOCKS = Path(__file__).resolve().parents[2] / "frontend" / "src" / "mocks"


def test_frontend_mocks_are_valid_scene_specs():
    mock_files = list(FRONTEND_MOCKS.glob("*.json"))
    assert mock_files, f"no mock fixtures found in {FRONTEND_MOCKS}"

    for mock_file in mock_files:
        spec = json.loads(mock_file.read_text())
        ok, error = validate_scene_spec(spec)
        assert ok, f"{mock_file.name} failed schema validation: {error}"


def test_content_catalogue_covers_full_registry():
    registry = json.loads(
        (Path(__file__).resolve().parents[2] / "shared" / "scene-registry.json").read_text()
    )
    catalogue = json.loads(
        (Path(__file__).resolve().parents[2] / "content" / "misconceptions.json").read_text()
    )
    registry_ids = {scene["id"] for scene in registry["scenes"]}
    catalogue_ids = {entry["sceneType"] for entry in catalogue["scenes"]}
    assert registry_ids == catalogue_ids
