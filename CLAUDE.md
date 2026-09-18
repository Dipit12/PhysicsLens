# CLAUDE.md

Context for Claude Code when working in this repo. Read this before making changes.

## What we're building

**PhysicsLens** (working name) — a natural-language physics visualization engine for
high-school students. A student types a question in plain English ("why doesn't a
spinning top fall over?") and gets back an interactive, physically-accurate
visualization (animation + live graph + equation overlay), built from a curated
library of concept scenes — not freeform generated code.

**Differentiator:** this is an *educational* tool, not an engineering simulator.
Every scene pairs with a short misconception-correcting explanation tied to the
high-school syllabus. Teachers and students get different access levels (enforced
via Cedar), and the product's real IP is the curated scene + explanation library,
not the LLM routing layer.

**Hard rule:** the LLM never generates simulation code. It only *selects* a scene
template and *extracts* parameters into a validated JSON spec. This keeps demos
reliable and keeps scope sane for a hackathon.

## Required tech (all must appear, some load-bearing, some supporting)

| Tech | Role | Load-bearing? |
|---|---|---|
| Strands Agents SDK | NL query → scene template selection + param extraction (tool calls) | Yes |
| Cedar | Authorizes which scene tools a session/role may invoke | Yes |
| SAM CLI + LocalStack | Serverless API (Lambda), runs fully on localhost for demo reliability | Yes |
| OpenSearch | Semantic retrieval over scene template library + query history log | Supporting |
| PartyRock | Used *once*, pre-build, to prototype the query→scene-spec prompt. Not part of the running app. | Prototyping only |
| Corretto | JVM runtime for local OpenSearch node | Implicit |
| Firecracker | Sandboxes any future custom-expression execution (stretch goal, not core demo) | Stretch only |

## Architecture (high level)

```
Browser (Canvas/Three.js renderer)
   |  POST /query { text }
   v
SAM/LocalStack API (Lambda)
   |
   +--> OpenSearch: retrieve top-3 candidate scene templates
   |
   +--> Cedar: is this session authorized to use these tools?
   |
   +--> Strands Agent: pick best template, extract params -> { sceneType, params }
   |
   v
Response: { sceneType, params, explanation }
   |
   v
Browser renders: animation + synced graph + equation overlay
```

The frontend never talks to the agent directly — it only ever receives a validated
`{ sceneType, params, explanation }` JSON object and renders it. This is the
contract that keeps modules independent (see PLAN.md).

## Repo structure (module boundaries — one repo, four owned folders)

```
/frontend          -- rendering engine, scene components, UI (Module 1)
/backend           -- Strands agent, Lambda handlers, SAM template (Module 2)
/infra             -- Cedar policies, OpenSearch + LocalStack setup (Module 3)
/content           -- curriculum content, PartyRock prompt prototyping,
                       demo script + integration ownership (Module 4)
/shared            -- the scene spec JSON schema and scene registry — the ONLY
                       files all four modules may need to touch; edit via PR
                       and notify the other three
```

## The scene spec contract (in `/shared/scene-spec.schema.json`)

This is the interface between backend, frontend, and content. Treat it as an API
contract: changing it requires a heads-up to the other three modules.

```json
{
  "sceneType": "pendulum",
  "params": { "length": 2.0, "angle": 45, "gravity": 9.8 },
  "explanation": {
    "summary": "...",
    "misconception": "...",
    "equation": "T = 2\\pi\\sqrt{L/g}"
  }
}
```

## Conventions

- **Commits:** `[module] short description` (e.g. `[frontend] add pendulum scene renderer`)
- **Branches:** `module/<name>/<feature>` (e.g. `frontend/priya/pendulum-scene`)
- **New scene types:** adding one touches all four modules — coordinate before
  starting, add it to `/shared/scene-registry.json` first so everyone knows it's coming
- **No new top-level dependencies** without a quick heads-up in the group chat —
  we're on a clock
- **Every scene template needs a complete quad:** a renderer (frontend), a
  Strands tool definition (backend), a Cedar role assignment + search index entry
  (infra), and a curriculum explanation entry (content) — incomplete quads block
  the demo, flag early

## Non-goals (v1)

- Freeform code generation from the LLM
- 3D scenes beyond 1-2 stretch cases (gyroscope)
- User accounts / persistence beyond session-level Cedar roles
- Firecracker sandboxing live in the demo (architecture-only unless time allows)

## Commands (fill in once scaffolded)

```bash
# Backend (from /backend)
sam build && sam local start-api --docker-network localstack

# Frontend (from /frontend)
npm run dev

# Infra (from /infra)
docker-compose up  # LocalStack + OpenSearch
```