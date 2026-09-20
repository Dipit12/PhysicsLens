# /content — Module 4

The differentiator's substance, plus the integration/glue role (CLAUDE.md,
PLAN.md).

- **`misconceptions.json`** — the catalogue: for each scene, the named
  misconception, the correct model, and the plain-language callout. Consumed by
  `/backend/src/content_loader.py` to fill the `explanation` block of every scene
  spec, and by Module 3 as OpenSearch document metadata. All 6 scenes are
  drafted; sanity-check the physics before the demo.
- **`syllabus-map.md`** — the chosen syllabus (AP Physics 1) and its unit
  mapping.
- **`partyrock-prompt.md`** — the query→scene-spec extraction prompt,
  prototyped in PartyRock before being handed to Module 2. Not part of the
  running app.
- **`demo-script.md`** — the POE demo walkthrough and pre-demo checklist.

## Integration owner responsibilities (still open)

- [ ] Run the first end-to-end test once Module 1–3 have a scene each
- [ ] File issues at whichever module is blocking a quad
- [ ] Keep `/shared/scene-spec.schema.json` coordinated — you're the tiebreaker
      if two modules want to change it differently
