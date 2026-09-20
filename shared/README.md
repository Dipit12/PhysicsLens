# /shared

The only folder all four modules may need to touch. Two files:

- **`scene-spec.schema.json`** — the contract for what the backend returns and
  the frontend renders: `{ sceneType, params, prediction, explanation }`. Backend
  validates its own agent output against this before responding (see
  `/backend/src/validate.py`). Frontend types in `/frontend/src/types.ts` mirror it
  by hand — keep them in sync.
- **`scene-registry.json`** — the six canonical scenes and their per-module
  "quad" completion status (frontend renderer / backend tool / infra Cedar+search
  entry / content misconception+syllabus entry). Update your column when your part
  of a scene lands.

**Rule (from CLAUDE.md):** editing `scene-spec.schema.json` requires a heads-up to
the other three modules — it's an API contract, not a local file.
