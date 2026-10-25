"""Base class for every Page Object.

Subclasses set `path` and declare their locators in `__init__`.
Paths are relative: the browser context already knows the base URL of the
selected environment.
"""

from __future__ import annotations

import re

from playwright.sync_api import Locator, Page, expect

from core.logger import get_logger


class BasePage:
    path: str = "/"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.log = get_logger(type(self).__name__)

    # ---------- navigation ----------
    def open(self, query: str = ""):
        url = f"{self.path}{query}"
        self.log.info("Opening %s", url)
        self.page.goto(url)
        return self

    @property
    def title(self) -> str:
        return self.page.title()

    def reload(self):
        self.page.reload()
        return self

    # ---------- interactions ----------
    def click(self, locator: Locator) -> None:
        self.log.debug("Click %s", locator)
        locator.click()

    def fill(self, locator: Locator, value: str, *, secret: bool = False) -> None:
        self.log.debug("Fill %s with %s", locator, "****" if secret else value)
        locator.fill(value)

    def accept_next_dialog(self) -> None:
        """Accept the next JS alert/confirm instead of letting it block the test."""
        self.page.once("dialog", lambda dialog: dialog.accept())

    # ---------- assertions ----------
    def should_be_open(self) -> None:
        expect(self.page).to_have_url(re.compile(re.escape(self.path)))
