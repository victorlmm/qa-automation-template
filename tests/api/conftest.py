import pytest

from api_clients import ProductsClient


@pytest.fixture(scope="session")
def products_client(api_settings):
    client = ProductsClient(**api_settings)
    yield client
    client.close()
