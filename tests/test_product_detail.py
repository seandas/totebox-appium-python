import pytest

from tests.data import MAX_QUANTITY, TOTE


@pytest.fixture
def details(guest_shop):
    return guest_shop.open_details(TOTE)


@pytest.mark.smoke
def test_details_show_the_selected_product(details):
    assert details.name() == TOTE
    assert details.quantity() == 1


@pytest.mark.regression
def test_quantity_stepper_stays_between_1_and_max(details):
    assert details.quantity() == 1
    assert not details.is_minus_enabled(), "The − button should be disabled at 1"

    details.increase(MAX_QUANTITY - 1)
    assert details.quantity() == MAX_QUANTITY
    assert not details.is_plus_enabled(), f"The + button should be disabled at {MAX_QUANTITY}"


@pytest.mark.regression
def test_add_to_cart_shows_snackbar_that_opens_cart(details):
    details.increase(2).add_to_cart()

    assert details.snackbar_text() == f"Added 3 × {TOTE} to your cart"
    cart = details.view_cart_from_snackbar()
    assert cart.quantity_of(TOTE) == 3


@pytest.mark.regression
def test_cannot_add_more_than_the_limit(details):
    details.increase(MAX_QUANTITY - 1).add_to_cart()
    details.add_to_cart()

    assert details.snackbar_text() == f"You already have the limit of {MAX_QUANTITY} × {TOTE} in your cart"
