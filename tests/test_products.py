import pytest

from tests.data import CRASH_ITEM, MUG, PHONE_STAND, TOTE
from config.capabilities import APP_PACKAGE

APP_RUNNING_IN_FOREGROUND = 4  # Appium's query_app_state code


@pytest.mark.smoke
def test_product_list_loads(guest_shop):
    names = guest_shop.visible_names()

    assert TOTE in names
    assert len(names) >= 3


@pytest.mark.regression
def test_sort_by_price_low_to_high(guest_shop):
    guest_shop.sort_by("Price (low to high)")

    prices = guest_shop.visible_prices()
    assert len(prices) >= 3
    assert prices == sorted(prices), f"Not ascending: {prices}"
    assert guest_shop.visible_names()[0] == PHONE_STAND  # the cheapest product


@pytest.mark.regression
def test_sort_by_price_high_to_low(guest_shop):
    guest_shop.sort_by("Price (high to low)")

    prices = guest_shop.visible_prices()
    assert prices == sorted(prices, reverse=True), f"Not descending: {prices}"


@pytest.mark.regression
def test_sort_by_name(guest_shop):
    guest_shop.sort_by("Price (low to high)")  # leave the default order first
    guest_shop.sort_by("Name (A to Z)")

    names = guest_shop.visible_names()
    assert names == sorted(names), f"Not alphabetical: {names}"


@pytest.mark.smoke
def test_add_to_cart_updates_badge(guest_shop):
    assert guest_shop.cart_badge_count() == 0

    guest_shop.add_to_cart(TOTE)
    assert guest_shop.snackbar_text() == f"Added 1 × {TOTE} to your cart"
    assert guest_shop.cart_badge_count() == 1

    guest_shop.add_to_cart(MUG)
    assert guest_shop.cart_badge_count() == 2


@pytest.mark.regression
def test_save_for_later_hides_product_from_list(guest_shop):
    guest_shop.save_for_later(TOTE)

    assert guest_shop.toast_text() == f"{TOTE} moved to Saved for later"
    assert not guest_shop.has_product(TOTE), "Saved product should leave the list"


@pytest.mark.regression
@pytest.mark.crash
def test_crash_test_item_crashes_the_app(guest_shop, driver):
    guest_shop.add_to_cart(CRASH_ITEM)

    # After the crash the app must no longer be in the foreground.
    assert guest_shop.is_gone(guest_shop.LIST, timeout=10), "Product list still on screen after the crash"
    assert driver.query_app_state(APP_PACKAGE) != APP_RUNNING_IN_FOREGROUND
