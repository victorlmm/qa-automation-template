"""Reusable HTTP client for API tests.

Gives every service client the same behaviour: base URL, bearer auth,
timeouts, automatic retries on transient errors, and request/response logging.
Service-specific clients subclass it and only add endpoint methods.
"""

from __future__ import annotations

from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from core.logger import get_logger

# Retry only what is safe and transient. 4xx responses are real answers.
_RETRY_STATUSES = (429, 502, 503, 504)


class BaseApiClient:
    def __init__(self, base_url: str, *, token: str | None = None, timeout: float = 15, retries: int = 2) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.log = get_logger(type(self).__name__)

        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})
        if token:
            self.set_token(token)

        retry = Retry(
            total=retries,
            backoff_factor=0.5,
            status_forcelist=_RETRY_STATUSES,
            allowed_methods=frozenset({"GET", "HEAD", "OPTIONS", "PUT", "DELETE"}),
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def set_token(self, token: str) -> None:
        self.session.headers["Authorization"] = f"Bearer {token}"

    def request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        url = f"{self.base_url}/{path.lstrip('/')}"
        kwargs.setdefault("timeout", self.timeout)
        self.log.debug("→ %s %s params=%s", method, url, kwargs.get("params"))
        response = self.session.request(method, url, **kwargs)
        self.log.debug("← %s %s (%.0f ms)", response.status_code, url, response.elapsed.total_seconds() * 1000)
        return response

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("DELETE", path, **kwargs)

    def close(self) -> None:
        self.session.close()
