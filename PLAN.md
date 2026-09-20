# PLAN.md — PhysicsLens

A **predict–observe–explain** physics engine that confronts the canonical
misconceptions in a fixed high-school / intro syllabus, with a depth toggle for
high-schoolers vs. physics majors. Four modules, one owner each, one repo.

---

## The problem we're actually solving

Students don't just "lack intuition" — they hold specific, stubborn wrong models
that normal teaching never dislodges, because it never makes them confront their
own prediction. Physics Education Research (the Force Concept Inventory and
decades of follow-up) has catalogued these misconceptions precisely. The
evidence-based fix is **Predict–Observe–Explain (POE)**: commit to a prediction,
then watch reality contradict it.

**So the core interaction is not "ask → see." It is "predict → confront":**

1. Student states a scenario *and their belief* in natural language
   ("a heavier ball falls faster than a light one")
2. The agent extracts **both** the scenario and the predicted outcome
3. The tool renders both — a "ghost" of the student's prediction beside the real
   physics — and highlights the moment they diverge
4. It names the misconception (from the PER catalogue) and ties it to a syllabus
   unit

## Two audiences, one engine (why Cedar matters here)

The same scene renders through different **lenses** by role:

| Role | Lens | Sees |
|---|---|---|
| Student (high school) | Intuition | ghost-vs-real, energy bars, force vectors, plain-language misconception callout |
| Physics major | Formal | + phase-space portrait, approximation toggles (e.g. small-angle on/off), governing equation, limiting cases |
| Teacher | Author | + create a POE prompt, pick which misconception to target, all scenes unlocked |

Cedar gates which lens a session unlocks. This is the demo's "wow" beat: the same
query, three depths, authorization deciding what you get.

## Differentiator, in one sentence

Not "an AI that draws physics" — **an AI that makes you commit to a wrong
prediction and then shows you exactly where and why physics disagrees, mapped to
your syllabus and calibrated to your level.**

---

## Scope: the canonical scenes (pick ~6 for the demo, from a fixed syllabus)

Each is chosen because it has a *famous, documented* misconception to target.

| Scene | Misconception it confronts | Physics-major depth layer |
|---|---|---|
| Free fall (two masses) | "heavier falls faster" | air resistance on/off, terminal velocity |
| Projectile arc | "velocity is zero at the top" / "force points along motion" | drag → no closed form, numerical vs ideal |
| Pendulum | "heavier bob swings faster" | small-angle approx on/off, phase portrait, period–amplitude |
| Circular motion | "there's an outward force" | centripetal vs centrifugal frames |
| Elastic collision | "the heavier object always wins" | momentum vs KE, centre-of-mass frame |
| Spring / SHM | "energy gets used up" | phase-space ellipse, damping regimes |

Adding a scene = a complete **quad** across all four modules (see below).

---

## Module split (pick one each)

### Module 1 — Visualization & Prediction Engine (`/frontend`)
The rendering layer, including the ghost-prediction overlay and the depth lenses.
Build against mock scene-spec JSON from day one; do not wait on the backend.

- Canvas 2D animation loop (`requestAnimationFrame`, a physics step-function per
  scene: free-fall, projectile, pendulum, circular, collision, spring)
- **Ghost overlay:** render the student's predicted outcome as a translucent
  second object/path beside the real one, with a "divergence marker" at the frame
  they part ways
- **Depth lenses:** an intuition renderer (energy bars, vectors, plain callout)
  and a formal renderer (phase-space canvas, equation via KaTeX, approximation
  toggle) sharing one physics state
- Sliders for each scene's exposed params; student/major/teacher UI modes
- **First deliverable:** free-fall + pendulum rendering from hand-written mock
  JSON, including a hardcoded ghost overlay, before the backend exists

### Module 2 — Agent & Backend (`/backend`)
Turn a natural-language *prediction* into a validated scene spec. Test the agent
standalone before wiring in Cedar/OpenSearch.

- Strands agent (Ollama for offline-safe dev; confirm Bedrock swap before demo)
- One `@tool` per scene — but the tool extracts **scenario + predicted outcome**,
  not just parameters (this is the richer, differentiating agent task)
- SAM template: `POST /predict` Lambda handler wrapping the agent
- `sam local start-api` against LocalStack
- Output always validated against `/shared/scene-spec.schema.json`; on invalid
  output, reject and retry once
- **First deliverable:** `curl .../predict -d '{"text":"heavy ball falls faster
  than light ball"}'` returns valid JSON carrying both the free-fall scene *and*
  the extracted (wrong) prediction, for ≥2 scenes

### Module 3 — Auth, Search & Local Env (`/infra`) ✅ completed
Cedar, OpenSearch, and the LocalStack environment everyone runs against. Pure
infra — no curriculum writing here (that's Module 4). Ship the local env first;
the team is blocked without it.

- Cedar policy set gating the **three depth lenses**: student → intuition only;
  major → + formal lens; teacher → + authoring. Policies in `/infra/cedar/`
- OpenSearch: index each scene by syllabus unit, misconception tag, and example
  predictions; expose the semantic-retrieval endpoint the backend calls to narrow
  a query to candidate scenes
- LocalStack + OpenSearch `docker-compose`, one-command up, documented
- **First deliverable (done):** a `student` session is denied the formal lens
  while a `major` session is allowed (`infra/scripts/demo_lens_gating.py`);
  `infra/up.sh` brings LocalStack + OpenSearch + `/retrieve` up in one command.
  OpenSearch is seeded with all 6 canonical scenes (syllabus unit,
  misconception tag, example predictions). Backend should call
  `POST http://localhost:8081/retrieve`.

### Module 4 — Curriculum, Misconceptions & Integration (`/content`)
The differentiator's substance, plus the glue role. Treat the writing as
seriously as the code — this is what makes it an *education* tool, not a toy.

- **Misconception catalogue:** for each scene, the named misconception (grounded
  in FCI/PER), the correct model, and the plain-language callout — feeds Module 2
  (agent context) and Module 3 (OpenSearch metadata)
- **Syllabus map:** tie every scene to a real unit of ONE chosen syllabus (AP
  Physics 1 / CBSE 11-12 / A-level — decide Day 1)
- **PartyRock prototyping:** iterate the "extract scenario + prediction" prompt in
  PartyRock early, hand the stable version to Module 2
- **Integration owner:** runs the first end-to-end test, files issues at the
  blocking module, keeps `/shared/scene-spec.schema.json` coordinated
- **Demo script owner:** writes/rehearses the POE demo, decides what to cut
- **First deliverable:** misconception + syllabus entries for the first 3 scenes;
  finalized PartyRock prompt handed to Module 2

---

## The scene spec contract (`/shared/scene-spec.schema.json`)

The interface between all four modules. Note it now carries the *prediction*, not
just the scene — this is the schema change that makes POE work.

```json
{
  "sceneType": "free-fall",
  "params": { "massA": 5.0, "massB": 0.1, "dragEnabled": false },
  "prediction": {
    "claim": "heavier object lands first",
    "expectedOutcome": "massA reaches ground before massB"
  },
  "explanation": {
    "misconception": "Heavier objects fall faster (FCI item 1).",
    "correctModel": "In vacuum, all masses fall at the same rate.",
    "syllabusUnit": "AP Physics 1 — Unit 1: Kinematics",
    "equation": "d = \\tfrac{1}{2} g t^2"
  }
}
```

---

## Timeline (adjust to your hackathon length)

**Day 1 morning — align, then split**
- All four agree on: the chosen syllabus, the first 3 scenes, and
  `/shared/scene-spec.schema.json` (including the `prediction` block). This is the
  one meeting that must happen together.
- Module 3 ships the one-command local env immediately.

**Day 1 afternoon — first deliverables**
- M1: free-fall + pendulum render from mock JSON with ghost overlay
- M2: agent returns valid scene + extracted prediction for 2 scenes
- M3: Cedar denies student the formal lens; local env up for everyone ✅
- M4: misconception + syllabus entries for 3 scenes; PartyRock prompt handed off
- **Checkpoint (M4 runs it):** swap M1's mock for M2's real `/predict` response

**Day 1 evening — first full POE loop**
- Wire OpenSearch retrieval into the backend
- Get ONE scene fully working end-to-end: query → prediction extracted → ghost vs
  real rendered → misconception shown → Cedar-gated depth. This proves the whole
  loop before scaling it.

**Day 2 morning — scale scenes + lenses**
- Add remaining scenes as complete quads
- Formal lens (phase space, approximation toggle) working for ≥2 scenes
- Teacher authoring mode if time allows

**Day 2 afternoon — demo prep**
- M4 rehearses the demo on the actual machine; offline model fallback confirmed
- Cut anything flaky — a tight POE loop on 3 scenes beats a shaky 6

## Definition of done, per scene (the "quad")
- [ ] Renders, with ghost overlay + working sliders, in both lenses (M1)
- [ ] Agent extracts scenario + prediction across 5+ phrasings (M2)
- [x] Cedar lens-gating + OpenSearch index entry (M3)
- [ ] Named misconception + correct model + syllabus unit (M4)

## Demo script (draft — M4 refines)
1. **Predict:** as a student, type a belief — "a heavier ball falls faster."
2. **Observe:** the ghost (student's prediction) and real physics run together;
   they land at the same time; divergence marker highlights the student was wrong.
3. **Explain:** the named misconception + correct model + syllabus unit appear.
4. **Depth via auth:** switch to physics-major role → Cedar unlocks the formal
   lens; the same pendulum now shows its phase portrait and a small-angle toggle
   that visibly breaks period-independence at large amplitude.
5. **Live curveball:** let a judge phrase a belief in their own words → OpenSearch
   narrows candidates, the agent picks the right scene.
6. Close on the architecture slide: Firecracker as the production sandbox for
   teacher-authored custom force laws.

## Risks
- **Prediction extraction is harder than parameter extraction** — the agent must
  catch the *belief*, not just the scenario. Test against many phrasings early.
- **Ghost overlay is the visual payoff** — if it's unclear, the whole POE point is
  lost. Prioritize making divergence obvious over adding scenes.
- **Firecracker needs KVM** — confirm hardware or keep it architecture-only.
- **Schema now carries `prediction`** — any change to it hits all four modules
  same-day; coordinate through M4.
- **M3's local env is a team-wide single point of failure** — simple and stable
  beats feature-complete.