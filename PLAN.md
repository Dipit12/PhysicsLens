# PLAN.md

Build plan for PhysicsLens. Four modules, one owner each, one repo, one shared
contract.

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
- Query input UI + loading/error states, student vs. teacher visual mode
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

### Module 3 — Auth & Search Infra (`/infra`)
Owns: Cedar policies, OpenSearch, and the LocalStack environment everyone else
runs against. Purely infra — no curriculum writing here (that's Module 4).

- Cedar policy set: `student` role (basic scenes only), `teacher` role (all
  scenes + stretch features); policies live in `/infra/cedar/`
- OpenSearch: index scene template metadata (description, syllabus tags, example
  queries); wire up the semantic retrieval endpoint the backend calls
- LocalStack + OpenSearch docker-compose setup, documented so all four can run
  it locally with one command
- Owns the shared `docker-compose.yml` / local-env setup — the one piece
  everyone depends on, so ship this first and keep it stable
- **First deliverable:** Cedar policy correctly denies a `student`-role session
  from invoking a `teacher`-only tool, demoable via a simple script; the whole
  local stack (LocalStack + OpenSearch) comes up with one command for the team

### Module 4 — Curriculum, Prototyping & Integration (`/content`)
Owns: the actual differentiator, plus the job of gluing the other three
together. This module is as much "product" as infra — treat the writing with
the same care as the code.

- **Curriculum content:** for every scene, write a 2-3 sentence explanation +
  one common misconception it corrects, mapped to a real high-school syllabus
  unit — this feeds both Module 2 (agent prompt context) and Module 3
  (OpenSearch metadata)
- **PartyRock prototyping:** iterate on the query→scene-spec prompt in PartyRock
  early on Day 1, hand the finalized prompt to Module 2 to port into the agent
- **Integration owner:** runs the first end-to-end test once Modules 1-3 have
  their first deliverables, files issues against whichever module is blocking,
  keeps `/shared/scene-spec.schema.json` changes coordinated across all four
- **Demo script owner:** writes and rehearses the live demo flow, decides what
  gets cut if something's flaky close to demo time
- **First deliverable:** curriculum content drafted for the first 3 scene types,
  finalized PartyRock prompt handed to Module 2

## Timeline (adjust to your actual hackathon length)

**Day 1 morning — parallel scaffolding**
- All four: agree on `/shared/scene-spec.schema.json` and the first 3 scene
  types (pendulum, projectile, collision) before splitting off — this is the
  one conversation that must happen together
- Module 3 ships the local-env setup (LocalStack + OpenSearch via one command)
  early — everyone else needs it running to test against
- Each module starts its "first deliverable" above independently

**Day 1 afternoon — first deliverables due**
- Module 1: 2 scenes render from mock JSON
- Module 2: agent returns valid JSON for those 2 scenes
- Module 3: Cedar policy demo works standalone; local env runs for everyone
- Module 4: curriculum content drafted for first 3 scenes, PartyRock prompt
  finalized and handed off
- **Checkpoint (Module 4 runs this):** swap Module 1's mock JSON for Module 2's
  real API response — first real integration test

**Day 1 evening — integration + 3rd scene**
- Wire OpenSearch retrieval into the backend flow
- Add collision scene end-to-end across all four modules (this proves the
  "complete quad" pattern from CLAUDE.md works repeatably)
- Module 4 triages whatever broke in the first integration test

**Day 2 morning — polish + remaining scenes**
- Add 2-3 more scene types if time allows (spring, circular motion)
- Teacher vs. student mode visibly different in the UI
- Query history / search past visualizations (OpenSearch-backed)

**Day 2 afternoon — demo prep**
- Module 4 finalizes and rehearses the demo script
- Test on the actual demo machine/network, offline model fallback confirmed
- Cut anything flaky — a smaller reliable demo beats a bigger fragile one

## Definition of done, per scene type

A scene isn't done until all four are true:
- [ ] Renders correctly with sliders working (Module 1)
- [ ] Agent reliably routes 5+ differently-phrased queries to it (Module 2)
- [ ] Has a Cedar role assignment and a search index entry (Module 3)
- [ ] Has a curriculum explanation + misconception note (Module 4)

## Demo script (draft — Module 4 refines after integration)

1. Student asks a basic question ("why does a ball thrown up come back down
   slower than...") → scene renders, explanation shown
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
- **Schema drift** — if `/shared/scene-spec.schema.json` changes, all four
  modules need to know same-day, not discover it at integration time
- **Module 3's local-env setup is a single point of failure for the team** —
  keep it simple and working over feature-complete; a broken docker-compose
  blocks everyone, not just Module 3