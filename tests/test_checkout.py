import re

import pytest

from pages.order_complete_page import OrderCompletePage
from tests import data
from tests.data import TOTE


@pytest.fixture
def checkout(shop):
    """Logged in, one tote in the cart, on the checkout screen."""
    shop.add_to_cart(TOTE)
    return shop.open_cart().checkout()


def _fill_shipping(page):
    return page.enter_shipping(data.NAME, data.ADDRESS, data.CITY, data.ZIP)


@pytest.mark.smoke
def test_order_with_card_is_placed(checkout):
    assert checkout.order_total() == "Order total: $29.98"
    _fill_shipping(checkout).choose_card().enter_card(data.CARD_NUMBER, data.CARD_EXPIRY, data.CARD_CVV)

    done = checkout.place_order()

    assert re.match(data.ORDER_NUMBER_PATTERN, done.order_number())
    assert done.total() == "Total paid: $29.98"


@pytest.mark.smoke
def test_order_pay_on_delivery_is_placed(checkout):
    _fill_shipping(checkout).choose_pay_on_delivery()
    assert not checkout.is_card_section_shown(), "Card fields should be hidden for pay on delivery"

    done = checkout.place_order()

    assert done.total() == "Total due on delivery: $29.98"


@pytest.mark.regression
def test_continue_shopping_returns_to_the_store(checkout):
    _fill_shipping(checkout).choose_pay_on_delivery()

    products = checkout.place_order().continue_shopping()

    assert products.is_displayed()
    assert products.cart_badge_count() == 0, "The cart should be empty after an order"


@pytest.mark.regression
def test_half_swipe_does_not_place_the_order(checkout):
    _fill_shipping(checkout).choose_pay_on_delivery()

    checkout.swipe_to_place_order(fraction=0.5)

    assert not OrderCompletePage(checkout.driver).is_displayed(timeout=3), "A half swipe must not place the order"
    assert checkout.is_visible(checkout.SLIDER), "The slider should slide back"


@pytest.mark.regression
def test_empty_form_shows_all_errors_and_does_not_place_the_order(checkout):
    checkout.choose_card()
    checkout.swipe_to_place_order()

    checkout.scroll_to_id("name_input")
    assert checkout.error("name") == "Enter your full name"
    assert checkout.error("address") == "Enter your street address"
    assert checkout.error("city") == "Enter your city"
    assert checkout.error("zip") == "Enter your ZIP code"
    checkout.scroll_to_id("card_number_input")
    assert checkout.error("card_number") == "Enter your card number"
    assert checkout.error("card_cvv") == "Enter the CVV"


@pytest.mark.regression
@pytest.mark.parametrize(
    "zip_code",
    [pytest.param("1234", id="four-digits"), pytest.param("12a45", id="letter")],
)
# The field itself caps input at 5 characters, so "too long" cannot be entered.
def test_zip_must_be_five_digits(checkout, zip_code):
    _fill_shipping(checkout).enter_zip(zip_code).choose_pay_on_delivery()

    checkout.swipe_to_place_order()

    checkout.scroll_to_id("zip_input")
    assert checkout.error("zip") == "ZIP code must be 5 digits"


@pytest.mark.regression
@pytest.mark.parametrize(
    "number, expiry, cvv, field, message",
    [
        pytest.param("4111", "12/30", "123", "card_number", "Card number must be 16 digits", id="short-card-number"),
        pytest.param(data.CARD_NUMBER, "1230", "123", "card_expiry", "Use the format MM/YY", id="bad-expiry-format"),
        pytest.param(data.CARD_NUMBER, "01/20", "123", "card_expiry", "This card has expired", id="expired-card"),
        pytest.param(data.CARD_NUMBER, "12/30", "12", "card_cvv", "CVV must be 3 digits", id="short-cvv"),
    ],
)
def test_card_validation(checkout, number, expiry, cvv, field, message):
    _fill_shipping(checkout).choose_card().enter_card(number, expiry, cvv)

    checkout.swipe_to_place_order()

    assert checkout.error(field) == message
