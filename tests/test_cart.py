import pytest

from tests.data import EARBUDS, FREE_SHIPPING, MUG, SHIPPING_FEE, TOTE


@pytest.mark.smoke
def test_cart_totals_include_shipping_under_the_free_line(guest_shop):
    guest_shop.add_to_cart(TOTE)
    cart = guest_shop.open_cart()

    assert cart.subtotal() == "$24.99"
    assert cart.shipping() == SHIPPING_FEE
    assert cart.total() == "$29.98"
    assert cart.is_free_shipping_hint_shown()


@pytest.mark.regression
def test_quantity_buttons_update_line_and_totals(guest_shop):
    guest_shop.add_to_cart(TOTE)
    cart = guest_shop.open_cart()

    cart.increase(TOTE)
    assert cart.quantity_of(TOTE) == 2
    assert cart.subtotal() == "$49.98"
    assert cart.shipping() == SHIPPING_FEE  # still under $50

    cart.increase(TOTE)
    assert cart.quantity_of(TOTE) == 3
    assert cart.subtotal() == "$74.97"
    assert cart.shipping() == FREE_SHIPPING
    assert cart.total() == "$74.97"

    cart.decrease(TOTE)
    assert cart.quantity_of(TOTE) == 2
    assert cart.shipping() == SHIPPING_FEE


@pytest.mark.regression
def test_shipping_is_free_when_one_item_is_over_fifty_dollars(guest_shop):
    guest_shop.add_to_cart(EARBUDS)
    cart = guest_shop.open_cart()

    assert cart.shipping() == FREE_SHIPPING
    assert not cart.is_free_shipping_hint_shown(timeout=1)


@pytest.mark.regression
def test_removing_the_last_item_shows_the_empty_cart(guest_shop):
    guest_shop.add_to_cart(TOTE)
    cart = guest_shop.open_cart()

    cart.remove(TOTE)

    assert cart.is_empty()
    assert cart.text_of(cart.CART_EMPTY_TEXT) == "Your cart is empty"
    assert cart.cart_badge_count() == 0


@pytest.mark.regression
def test_removing_one_item_keeps_the_other(guest_shop):
    guest_shop.add_to_cart(TOTE)
    guest_shop.add_to_cart(MUG)
    cart = guest_shop.open_cart()

    cart.remove(TOTE)

    assert cart.has_line(MUG)
    assert not cart.has_line(TOTE, timeout=1)
    assert cart.subtotal() == "$18.99"


@pytest.mark.regression
def test_start_shopping_from_empty_cart_returns_to_products(guest_shop):
    cart = guest_shop.open_cart()
    assert cart.is_empty()

    products = cart.start_shopping()

    assert products.is_displayed()
    assert TOTE in products.visible_names()
