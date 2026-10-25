from playwright.sync_api import Page

from core.ui import BasePage


class ProductsPage(BasePage):
    path = "/products"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.search_input = page.locator("#search_product")
        self.search_button = page.locator("#submit_search")
        self.section_title = page.locator(".features_items h2.title")
        self.product_names = page.locator(".features_items .productinfo p")

    def search(self, term: str) -> None:
        self.fill(self.search_input, term)
        self.click(self.search_button)

    def get_product_names(self) -> list[str]:
        return [name.strip() for name in self.product_names.all_inner_texts()]
