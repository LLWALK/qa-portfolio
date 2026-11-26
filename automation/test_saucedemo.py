import pytest
from playwright.sync_api import Page, expect

URL = "https://www.saucedemo.com"


def login(page, username):
    page.goto(URL)
    page.fill("#user-name", username)
    page.fill("#password", "secret_sauce")
    page.click("#login-button")


@pytest.mark.parametrize("username", ["standard_user", "problem_user"])
def test_every_item_can_be_added_to_cart(page: Page, username):
    login(page, username)

    broken = []
    items = page.locator(".inventory_item")
    for i in range(items.count()):
        item = items.nth(i)
        name = item.locator(".inventory_item_name").inner_text()
        button = item.locator("button")

        button.click()

        # A working button changes from "Add to cart" to "Remove"
        if button.inner_text() != "Remove":
            broken.append(name)

    assert not broken, f"These items could not be added to the cart: {broken}"

@pytest.mark.parametrize("username", ["standard_user", "problem_user"])
def test_every_item_can_be_removed_from_cart(page: Page, username):
    login(page, username)

    broken = []
    items = page.locator(".inventory_item")
    for i in range(items.count()):
        item = items.nth(i)
        name = item.locator(".inventory_item_name").inner_text()
        button = item.locator("button")

        button.click()   # add it
        if button.inner_text() != "Remove":
            continue     # skip products that can't even be added

        button.click()              # remove it

        if button.inner_text() != "Add to cart":
            broken.append(name)

    assert not broken, f"These items could not be removed from the cart: {broken}"
