#!/usr/bin/env python3
"""HTTP retrieval endpoint the backend calls to narrow a NL query to candidate scenes.

    POST /retrieve  {"text": "heavier ball falls faster", "k": 3}
    GET  /retrieve?q=heavier+ball+falls+faster&k=3

BM25 over misconception tags + example predictions. Seeds the index on boot
if OpenSearch is empty, so `docker compose up` is the whole local env.
"""
from __future__ import annotations

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))

from documents import INDEX_NAME, build_retrieve_query  # noqa: E402
from opensearch_client import OpenSearchClient  # noqa: E402
from seed_index import seed, wait_for_opensearch  # noqa: E402

OPENSEARCH_URL = os.environ.get("OPENSEARCH_URL", "http://localhost:9200")
PORT = int(os.environ.get("RETRIEVE_PORT", "8081"))
client = OpenSearchClient(OPENSEARCH_URL)


def retrieve(text: str, k: int = 3) -> dict:
    text = (text or "").strip()
    if not text:
        return {"error": "missing 'text'"}
    k = max(1, min(int(k), 6))
    body = build_retrieve_query(text, k)
    result = client.request("POST", f"/{INDEX_NAME}/_search", body)
    hits = result.get("hits", {}).get("hits", [])
    candidates = []
    for hit in hits:
        src = hit.get("_source") or {}
        candidates.append(
            {
                "sceneType": src.get("sceneType"),
                "displayName": src.get("displayName"),
                "misconceptionTag": src.get("misconceptionTag"),
                "syllabusUnit": src.get("syllabusUnit"),
                "misconception": src.get("misconception"),
                "score": hit.get("_score"),
            }
        )
    return {"query": text, "candidates": candidates}


class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, payload: dict) -> None:
        raw = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self._send(200, {"ok": True, "opensearch": client.ping()})
            return
        if parsed.path != "/retrieve":
            self._send(404, {"error": "not found"})
            return
        qs = parse_qs(parsed.query)
        text = (qs.get("q") or qs.get("text") or [""])[0]
        k = int((qs.get("k") or ["3"])[0])
        payload = retrieve(text, k)
        self._send(400 if "error" in payload else 200, payload)

    def do_POST(self) -> None:  # noqa: N802
        if self.path.rstrip("/") != "/retrieve":
            self._send(404, {"error": "not found"})
            return
        length = int(self.headers.get("Content-Length") or 0)
        body = json.loads(self.rfile.read(length) or b"{}")
        payload = retrieve(body.get("text") or "", body.get("k") or 3)
        self._send(400 if "error" in payload else 200, payload)

    def log_message(self, fmt: str, *args) -> None:
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


def main() -> int:
    wait_for_opensearch(client)
    count = seed(client)
    print(f"OpenSearch ready; indexed {count} scenes", flush=True)
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"retrieve listening on :{PORT}", flush=True)
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
