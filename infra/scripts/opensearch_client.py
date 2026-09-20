"""Minimal OpenSearch HTTP client (stdlib only — no extra top-level deps)."""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any


class OpenSearchClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def request(self, method: str, path: str, body: Any | None = None) -> Any:
        data = None
        headers = {"Accept": "application/json"}
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(
            f"{self.base_url}{path}",
            data=data,
            headers=headers,
            method=method,
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read()
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"OpenSearch {method} {path} failed ({exc.code}): {detail}") from exc

    def ping(self) -> bool:
        try:
            self.request("GET", "/")
            return True
        except (RuntimeError, urllib.error.URLError):
            return False
