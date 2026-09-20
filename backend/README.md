# /backend — Module 2

Strands agent + SAM Lambda wrapping it. Test the agent standalone before
wiring in Cedar/OpenSearch (PLAN.md).

## Setup

SAM CLI and AWS CLI aren't installed on this machine yet — install before
running the commands below:

```bash
brew install aws-sam-cli awscli   # macOS
pip install -r requirements.txt
```

Also install Ollama for offline-safe local dev (PLAN.md): https://ollama.com,
then `ollama pull llama3.1` (or swap the model id in `src/agent.py`).

## Run

```bash
sam build
sam local start-api --docker-network localstack   # once /infra's LocalStack is up
```

Manual agent test without SAM, once Ollama is running:

```bash
cd src && python -c "from agent import run_prediction_agent; print(run_prediction_agent('a heavier ball falls faster than a light one'))"
```

Target curl (PLAN.md first deliverable):

```bash
curl localhost:3000/predict -d '{"text":"heavy ball falls faster than light ball"}'
```

## Files

- `src/app.py` — Lambda handler: parse request, call the agent, validate,
  retry once on invalid output (PLAN.md), respond.
- `src/agent.py` — the Strands agent + one `@tool` per scene. Only `free_fall`
  and `pendulum` exist so far — **add the remaining 4 scenes here**, matching
  `/shared/scene-spec.schema.json`'s per-scene param shapes exactly.
- `src/validate.py` — schema gate. CLAUDE.md hard rule: the LLM never
  generates simulation code, only a spec — this is what enforces that.
- `src/content_loader.py` — pulls the `explanation` block from Module 4's
  `/content/misconceptions.json` so the agent doesn't have to invent it.
- `tests/test_schema_roundtrip.py` — run with `pytest` from `/backend`; checks
  the frontend's mock fixtures and the content catalogue stay in sync with the
  shared schema/registry.

## First deliverable (PLAN.md)

`curl .../predict -d '{"text":"heavy ball falls faster than light ball"}'`
returns valid JSON carrying both the free-fall scene *and* the extracted
(wrong) prediction, for ≥2 scenes.
