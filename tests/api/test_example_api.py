"""Example API tests. Delete or replace with your own."""

import pytest

from api_clients.schemas import ProductsResponse

pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_products_list_matches_contract(products_client):
    body = products_client.list_products()

    response = ProductsResponse.model_validate(body)
    assert response.responseCode == 200
    assert response.products, "Catalogue should not be empty"


@pytest.mark.regression
@pytest.mark.parametrize("term", ["top", "jean"])
def test_search_returns_results(products_client, term):
    response = ProductsResponse.model_validate(products_client.search(term))

    assert response.products, f"Expected results for '{term}'"
