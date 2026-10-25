"""Example UI tests. Delete or replace with your own."""

import pytest
from playwright.sync_api import Page, expect

from pages import LoginPage, ProductsPage
from utils.data_factory import new_person

pytestmark = pytest.mark.ui


@pytest.mark.smoke
def test_products_page_loads(page: Page):
    products = ProductsPage(page).open()

    products.should_be_open()
    expect(products.section_title).to_have_text("All Products")


@pytest.mark.regression
def test_search_shows_matching_products(page: Page):
    products = ProductsPage(page).open()
    products.search("Jeans")

    expect(products.section_title).to_have_text("Searched Products")
    assert any("jeans" in name.lower() for name in products.get_product_names())


@pytest.mark.regression
def test_login_with_unknown_user_shows_error(page: Page):
    person = new_person()
    login = LoginPage(page).open()
    login.login(person["email"], person["password"])

    expect(login.error_message).to_have_text("Your email or password is incorrect!")
