#!/usr/bin/env bash
# One-command local env for the whole team (PLAN.md Module 3).
set -euo pipefail
cd "$(dirname "$0")"

echo "Starting LocalStack + OpenSearch + retrieve…"
docker compose up --wait --detach

echo
echo "Ready:"
echo "  LocalStack          http://localhost:4566"
echo "  OpenSearch          http://localhost:9200"
echo "  scene retrieval     http://localhost:8081/retrieve"
echo
echo "Cedar lens-gating demo (no Docker):"
echo "  python3.12 -m venv .venv && .venv/bin/pip install -r requirements.txt"
echo "  .venv/bin/python scripts/demo_lens_gating.py"
echo
echo "Smoke the retrieval endpoint:"
echo "  curl -s http://localhost:8081/retrieve -d '{\"text\":\"a heavier ball falls faster\"}'"
