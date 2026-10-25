from playwright.sync_api import Page

from core.ui import BasePage


class LoginPage(BasePage):
    """Example page object. Locators live here, never in tests."""

    path = "/login"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.email = page.locator("[data-qa='login-email']")
        self.password = page.locator("[data-qa='login-password']")
        self.submit = page.locator("[data-qa='login-button']")
        self.error_message = page.locator("form[action='/login'] p")

    def login(self, email: str, password: str) -> None:
        self.fill(self.email, email)
        self.fill(self.password, password, secret=True)
        self.click(self.submit)
