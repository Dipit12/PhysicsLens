# /infra — Module 3

Cedar, OpenSearch, and the LocalStack environment everyone runs against. Pure
infra — no curriculum writing here (that's Module 4).

**Status: first deliverable complete.** A `student` session is denied the
formal lens while a `major` session is allowed (demo script below), and the
full local stack comes up with one command.

## One-command local env

```bash
cd infra
./up.sh
```

(`docker compose up --wait` is equivalent.) Brings up:

| Service | URL | Purpose |
|---|---|---|
| LocalStack | http://localhost:4566 | Lambda / API Gateway target for `sam local start-api --docker-network localstack` |
| OpenSearch | http://localhost:9200 | Scene index (`physicslens-scenes`) |
| retrieve | http://localhost:8081/retrieve | Top-k scene candidates for a NL prediction |

The retrieve container seeds OpenSearch on boot from `/shared/scene-registry.json`,
`/content/misconceptions.json`, and `opensearch/example-predictions.json`.

```bash
curl -s http://localhost:8081/retrieve \
  -H 'Content-Type: application/json' \
  -d '{"text":"a heavier ball falls faster than a light one"}'
```

Backend (Module 2) should call that endpoint to narrow a query to candidate
scenes before the Strands agent picks a tool.

## Cedar lens-gating demo (no Docker)

Needs Python 3.12+ on macOS (`cedarpy` wheels start at 3.11).

```bash
cd infra
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/demo_lens_gating.py
.venv/bin/pytest tests
```

Expected demo table:

```
role       intuition    formal       authorPrompt
student    ALLOW        DENY         DENY
major      ALLOW        ALLOW        DENY
teacher    ALLOW        ALLOW        ALLOW
```

`scripts/cedar_authz.py` is the import Module 2 can use (`is_lens_allowed(role, lens)`).

## Files

- `docker-compose.yml` / `up.sh` — one-command local env (network name: `localstack`)
- `cedar/schema.cedarschema.json` + `cedar/policies/lens-access.cedar` + `cedar/entities.json`
- `opensearch/index-template.json` — mapping for syllabus unit, misconception tag, example predictions
- `scripts/retrieve_server.py` — retrieval HTTP API + index seed
- `scripts/demo_lens_gating.py` — student vs major vs teacher

## Corretto note

OpenSearch's Docker image bundles its own JVM — you only need Corretto
installed locally if you run OpenSearch as a bare process instead of through
`docker compose` (CLAUDE.md lists Corretto as "implicit").
