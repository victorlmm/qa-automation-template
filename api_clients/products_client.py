from typing import Any

from core.api import BaseApiClient


class ProductsClient(BaseApiClient):
    """Example service client: only endpoint methods, no assertions."""

    def list_products(self) -> dict[str, Any]:
        return self.get("productsList").json()

    def search(self, term: str) -> dict[str, Any]:
        return self.post("searchProduct", data={"search_product": term}).json()
