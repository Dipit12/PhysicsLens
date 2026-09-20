#!/usr/bin/env python3
"""Create the physicslens-scenes index and load one document per canonical scene."""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from documents import INDEX_NAME, build_scene_documents, load_index_template  # noqa: E402
from opensearch_client import OpenSearchClient  # noqa: E402


def seed(client: OpenSearchClient) -> int:
    template = load_index_template()
    client.request("PUT", "/_index_template/physicslens-scenes", template)
    try:
        client.request("DELETE", f"/{INDEX_NAME}")
    except RuntimeError:
        pass
    client.request("PUT", f"/{INDEX_NAME}")
    docs = build_scene_documents()
    bulk_lines: list[str] = []
    for doc in docs:
        bulk_lines.append(json.dumps({"index": {"_index": INDEX_NAME, "_id": doc["sceneType"]}}))
        bulk_lines.append(json.dumps(doc))
    payload = ("\n".join(bulk_lines) + "\n").encode("utf-8")
    req_url = f"{client.base_url}/_bulk?refresh=true"
    import urllib.request

    req = urllib.request.Request(
        req_url,
        data=payload,
        headers={"Content-Type": "application/x-ndjson"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read())
    if result.get("errors"):
        raise RuntimeError(f"bulk index reported errors: {result}")
    count = client.request("GET", f"/{INDEX_NAME}/_count")
    return int(count.get("count", 0))


def wait_for_opensearch(client: OpenSearchClient, attempts: int = 60) -> None:
    for _ in range(attempts):
        if client.ping():
            return
        time.sleep(1)
    raise SystemExit(f"OpenSearch not reachable at {client.base_url}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--opensearch-url", default="http://localhost:9200")
    args = parser.parse_args()
    client = OpenSearchClient(args.opensearch_url)
    wait_for_opensearch(client)
    n = seed(client)
    print(f"Indexed {n} scenes into {INDEX_NAME} at {args.opensearch_url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
