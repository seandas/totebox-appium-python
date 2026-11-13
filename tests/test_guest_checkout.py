import re

import pytest

from tests import data
from tests.data import TOTE


@pytest.mark.smoke
def test_guest_logs_in_at_checkout_keeps_cart_and_buys(guest_shop):
    guest_shop.add_to_cart(TOTE)
    cart = guest_shop.open_cart()

    login = cart.checkout_as_guest()
    assert login.is_visible(login.CHECKOUT_MESSAGE), "Login should explain that it is needed to check out"
    assert login.text_of(login.CHECKOUT_MESSAGE) == "Log in to check out. Your cart is saved."

    checkout = login.log_in_to_checkout(data.VALID_EMAIL, data.VALID_PASSWORD)
    assert checkout.order_total() == "Order total: $29.98", "The guest's cart should be kept"

    checkout.enter_shipping(data.NAME, data.ADDRESS, data.CITY, data.ZIP).choose_pay_on_delivery()
    done = checkout.place_order()
    assert re.match(data.ORDER_NUMBER_PATTERN, done.order_number())


@pytest.mark.regression
def test_back_from_checkout_login_returns_to_the_cart(guest_shop):
    guest_shop.add_to_cart(TOTE)
    cart = guest_shop.open_cart()
    cart.checkout_as_guest()

    cart.driver.back()

    assert cart.has_line(TOTE), "Going back should return to the cart with the item still in it"
