"""Global fixtures and hooks. Available to every test without importing."""

from __future__ import annotations

import re

import pytest

from config import Settings, load_settings
from config.settings import available_environments
from core.logger import configure_logging, get_logger

log = get_logger("conftest")


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default=None,
        help=f"Target environment: {', '.join(available_environments())} (default: TEST_ENV or qa)",
    )


def pytest_configure(config):
    settings = load_settings(config.getoption("--env"))
    config._qa_settings = settings
    configure_logging(settings.log_level)
    log.info("Running against '%s' → %s", settings.env, settings.base_url)


def pytest_report_header(config):
    s = config._qa_settings
    return f"environment: {s.env} | base_url: {s.base_url} | api: {s.api_base_url}"


# ---------------------------------------------------------------- settings


@pytest.fixture(scope="session")
def settings(pytestconfig) -> Settings:
    return pytestconfig._qa_settings


# ---------------------------------------------------------------- browser
# pytest-playwright provides `page`, `context` and `browser`. These overrides
# feed them the selected environment's configuration.


@pytest.fixture(scope="session")
def base_url(settings) -> str:
    return settings.base_url


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, settings):
    return {
        **browser_context_args,
        "viewport": {"width": settings.viewport_width, "height": settings.viewport_height},
        "ignore_https_errors": settings.env != "prod",
    }


@pytest.fixture(autouse=True)
def _block_third_party_hosts(request, settings):
    """Abort requests to hosts listed in `browser.block_hosts` (UI tests only)."""
    if settings.block_hosts and "page" in request.fixturenames:
        pattern = re.compile("|".join(re.escape(host) for host in settings.block_hosts))
        request.getfixturevalue("context").route(pattern, lambda route: route.abort())
    yield


# ---------------------------------------------------------------- API


@pytest.fixture(scope="session")
def api_settings(settings) -> dict:
    """Common keyword arguments for any BaseApiClient subclass."""
    return {
        "base_url": settings.api_base_url,
        "token": settings.api_token,
        "timeout": settings.api_timeout,
        "retries": settings.api_retries,
    }
