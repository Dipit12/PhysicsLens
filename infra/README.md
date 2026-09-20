# /infra — Module 3

Cedar, OpenSearch, and the LocalStack environment everyone runs against. Pure
infra — no curriculum writing here (that's Module 4). Ship the local env
first; the team is blocked without it (PLAN.md).

## Run

```bash
cd infra
docker-compose up
```

Brings up:
- **LocalStack** on `:4566` — the backend's `sam local start-api
  --docker-network localstack` targets this.
- **OpenSearch** on `:9200` — load `opensearch/index-template.json` then index
  one document per scene from `/shared/scene-registry.json` +
  `/content/misconceptions.json`.

## Files

- `docker-compose.yml` — one-command local env.
- `cedar/schema.cedarschema.json` + `cedar/policies/lens-access.cedar` — the
  three-lens gating policy (student/major/teacher). **Scaffold only** — confirm
  syntax against current Cedar docs/CLI before wiring into an actual Lambda
  authorizer; Cedar's schema format has moved across versions.
- `opensearch/index-template.json` — mapping for the scene-retrieval index the
  backend's semantic search calls into.

## First deliverable (PLAN.md)

A `student` session is denied the formal lens while a `major` session is
allowed, demoable via a script; full local stack up with one command for the
whole team.

## Corretto note

OpenSearch's Docker image bundles its own JVM — you only need Corretto
installed locally if you end up running OpenSearch as a bare process instead
of through `docker-compose` (CLAUDE.md lists Corretto as "implicit").
