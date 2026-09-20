# PhysicsLens

Natural-language physics visualization for high-school students, built around
**predict–observe–explain**: a student states a belief, the tool renders
their prediction as a ghost beside the real physics, and names exactly where
and why they diverge — mapped to a real syllabus unit and gated by role via
Cedar.

Full context: **[CLAUDE.md](./CLAUDE.md)** (repo conventions, required tech,
architecture) and **[PLAN.md](./PLAN.md)** (the product spec, module split,
timeline, demo script).

## Status

Repo skeleton only, as of this commit — structure, the shared contract, and
per-module stubs are in place; no scene is fully wired end-to-end yet. All 6
canonical scenes have their misconception + syllabus content drafted
(`/content`); frontend/backend/infra all still need real implementations.

## Repo structure

```
/frontend   Module 1 — rendering engine, ghost overlay, depth lenses
/backend    Module 2 — Strands agent, Lambda handler, SAM template
/infra      Module 3 — Cedar policies, OpenSearch + LocalStack
/content    Module 4 — misconception catalogue, syllabus map, demo script
/shared     the scene-spec contract + scene registry — all four modules read
            this; changing it needs a heads-up to the other three (CLAUDE.md)
```

Each folder has its own README with setup commands and its first deliverable
per PLAN.md.

## Quickstart

```bash
# infra (LocalStack + OpenSearch) — ship/start this first, everyone depends on it
cd infra && docker-compose up

# frontend — renders from mock JSON, no backend needed yet
cd frontend && npm install && npm run dev

# backend — needs SAM CLI + AWS CLI + Ollama installed first (see backend/README.md)
cd backend && pip install -r requirements.txt && sam build && sam local start-api --docker-network localstack
```

**Toolchain gap on this machine as of the initial scaffold:** SAM CLI, AWS
CLI, and Ollama are not yet installed — needed before Module 2's backend
commands will run. Node, Docker, and Java are present.

## Conventions (from CLAUDE.md)

- Commits: `[module] short description`
- Branches: `module/<name>/<feature>`
- New scene types touch all four modules — add to `/shared/scene-registry.json`
  first
- No new top-level dependencies without a heads-up
- Every scene needs a complete **quad**: renderer (frontend) + Strands tool
  (backend) + Cedar role/search entry (infra) + curriculum entry (content)
