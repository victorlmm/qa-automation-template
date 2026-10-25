"""Environment-aware configuration.

Resolution order (later wins):
1. config/environments/<env>.toml   (committed, no secrets)
2. Environment variables / .env     (secrets and one-off overrides)

The environment is chosen with `pytest --env=staging` or `TEST_ENV=staging`.
"""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ENVIRONMENTS_DIR = Path(__file__).parent / "environments"
DEFAULT_ENV = "qa"


@dataclass(frozen=True)
class Settings:
    env: str
    base_url: str
    api_base_url: str
    api_timeout: float
    api_retries: int
    viewport_width: int
    viewport_height: int
    log_level: str
    block_hosts: tuple[str, ...] = ()
    # Secrets: only ever from environment variables / .env
    api_token: str | None = None
    test_user_email: str | None = None
    test_user_password: str | None = None


def available_environments() -> list[str]:
    return sorted(p.stem for p in ENVIRONMENTS_DIR.glob("*.toml"))


def load_settings(env: str | None = None) -> Settings:
    load_dotenv()
    env = (env or os.getenv("TEST_ENV") or DEFAULT_ENV).lower()
    path = ENVIRONMENTS_DIR / f"{env}.toml"
    if not path.exists():
        raise ValueError(f"Unknown environment '{env}'. Available: {', '.join(available_environments())}")

    with open(path, "rb") as fh:
        data = tomllib.load(fh)
    api = data.get("api", {})
    browser = data.get("browser", {})

    return Settings(
        env=env,
        base_url=os.getenv("BASE_URL", data["base_url"]).rstrip("/"),
        api_base_url=os.getenv("API_BASE_URL", data["api_base_url"]).rstrip("/"),
        api_timeout=float(os.getenv("API_TIMEOUT", api.get("timeout_seconds", 15))),
        api_retries=int(os.getenv("API_RETRIES", api.get("retries", 2))),
        viewport_width=int(browser.get("viewport_width", 1440)),
        viewport_height=int(browser.get("viewport_height", 900)),
        log_level=os.getenv("LOG_LEVEL", data.get("logging", {}).get("level", "INFO")).upper(),
        block_hosts=tuple(browser.get("block_hosts", [])),
        api_token=os.getenv("API_TOKEN") or None,
        test_user_email=os.getenv("TEST_USER_EMAIL") or None,
        test_user_password=os.getenv("TEST_USER_PASSWORD") or None,
    )
