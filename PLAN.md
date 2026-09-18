# PLAN.md

Build plan for PhysicsLens. Three modules, one owner each, one shared contract.
Pick your module below before writing any code.

## Module split (pick one each)

### Module 1 — Visualization Engine (`/frontend`)
Owns: the entire rendering layer. Nothing here depends on the agent being done —
build against mock scene-spec JSON from day one.

- Canvas 2D animation loop (`requestAnimationFrame`, physics step functions per
  scene type: pendulum, projectile, collision, spring)
- Synced live graph (energy/velocity/momentum vs. time)
- Equation overlay (KaTeX, live-substituted values)
- Slider controls per scene's exposed params
- Scene registry: a renderer + physics-step function per `sceneType`
- Query input UI + loading/error states
- **First deliverable:** 2 hardcoded scenes (pendulum, projectile) rendering
  correctly from a hand-written mock JSON, before the backend exists

### Module 2 — Agent & Backend (`/backend`)
Owns: turning a query into a valid scene spec. Build and test the agent standalone
before wiring in Cedar/OpenSearch.

- Strands agent setup (model provider: start on Ollama for offline-safe dev,
  confirm Bedrock swap works before demo day)
- One `@tool` per scene type — validates + returns structured params
- SAM template: `POST /query` Lambda handler, wraps the agent call
- `sam local start-api` running against LocalStack
- Response always validated against `/shared/scene-spec.schema.json` before
  returning — reject and retry once if the agent's output doesn't validate
- **First deliverable:** `curl localhost:3000/query -d '{"text":"pendulum swinging"}'`
  returns valid JSON matching the schema, using at least 2 scene tools

### Module 3 — Auth, Search & Curriculum (`/infra`)
Owns: Cedar policies, OpenSearch setup, and the actual educational content —
this is where the differentiator lives, treat the content work as seriously as
the infra work.

- Cedar policy set: `student` role (basic scenes only), `teacher` role (all
  scenes + stretch features); policies live in `/infra/cedar/`
- OpenSearch: index scene template metadata (description, syllabus tags, example
  queries); wire up semantic retrieval endpoint the backend calls
- LocalStack + OpenSearch docker-compose setup, documented so all three can run
  it locally
- **Curriculum content** (the actual differentiator): for every scene, write a
  2-3 sentence explanation + one common misconception it corrects, mapped to a
  real high-school syllabus unit
- PartyRock prompt prototyping happens here early (Day 1), ports into Module 2's
  agent prompt once stable
- **First deliverable:** Cedar policy correctly denies a `student`-role session
  from invoking a `teacher`-only tool, demoable via a simple script

## Timeline (adjust to your actual hackathon length)

**Day 1 morning — parallel scaffolding**
- All three: agree on `/shared/scene-spec.schema.json` and the first 3 scene
  types (pendulum, projectile, collision) before splitting off — this is the
  one conversation that must happen together
- Each module starts its "first deliverable" above independently

**Day 1 afternoon — first deliverables due**
- Module 1: 2 scenes render from mock JSON
- Module 2: agent returns valid JSON for those 2 scenes
- Module 3: Cedar policy demo works standalone, curriculum content drafted for
  first 3 scenes
- **Checkpoint:** swap Module 1's mock JSON for Module 2's real API response —
  first real integration test

**Day 1 evening — integration + 3rd scene**
- Wire OpenSearch retrieval into the backend flow
- Add collision scene end-to-end across all three modules (this proves the
  "triad" pattern from CLAUDE.md works repeatably)
- Fix whatever broke in the first integration test

**Day 2 morning — polish + remaining scenes**
- Add 2-3 more scene types if time allows (spring, circular motion)
- Teacher vs. student mode visibly different in the UI
- Query history / search past visualizations (OpenSearch-backed)

**Day 2 afternoon — demo prep**
- Write the demo script (below)
- Test on the actual demo machine/network, offline model fallback confirmed
- Cut anything flaky — a smaller reliable demo beats a bigger fragile one

## Definition of done, per scene type

A scene isn't done until all three are true:
- [ ] Renders correctly with sliders working (Module 1)
- [ ] Agent reliably routes 5+ differently-phrased queries to it (Module 2)
- [ ] Has a curriculum explanation + misconception note, and a Cedar role
      assignment (Module 3)

## Demo script (draft — refine after integration)

1. Student asks a basic question ("why does a ball thrown up come back down slower
   than... " etc.) → scene renders, explanation shown
2. Student tries a teacher-only query → Cedar denies it, UI explains why
3. Switch to teacher role → same query now works, advanced scene unlocks
4. Ask an ambiguous/oddly-phrased question live (judge-suggested) → show
   OpenSearch retrieval narrowing candidates, agent picking correctly
5. Close on the architecture slide: mention Firecracker sandboxing as the
   production hardening step for custom user-submitted expressions

## Risks to watch

- **Agent routing accuracy** on oddly-phrased queries — test against a wide
  question set early, don't discover failures during the live demo
- **Firecracker** needs KVM — confirm your dev machines support it before
  committing to a live demo of it; default to architecture-only if unsure
- **Schema drift** — if `/shared/scene-spec.schema.json` changes, all three
  modules need to know same-day, not discover it at integration time