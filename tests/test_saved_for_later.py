import pytest

from tests.data import MUG, TOTE


@pytest.fixture
def cart_with_tote(guest_shop):
    guest_shop.add_to_cart(TOTE)
    return guest_shop.open_cart()


@pytest.mark.smoke
def test_save_for_later_moves_the_item_out_of_the_cart(cart_with_tote):
    cart = cart_with_tote

    cart.save_for_later(TOTE)

    assert cart.is_empty()
    assert cart.open_saved_tab().has_saved(TOTE)
    assert cart.tab_titles() == ("Cart (0)", "Saved for later (1)")


@pytest.mark.regression
def test_move_back_to_cart(cart_with_tote):
    cart = cart_with_tote
    cart.save_for_later(TOTE)
    cart.open_saved_tab().move_to_cart(TOTE)

    assert cart.is_saved_empty()
    assert cart.open_cart_tab().has_line(TOTE)


@pytest.mark.regression
def test_delete_saved_item(cart_with_tote):
    cart = cart_with_tote
    cart.save_for_later(TOTE)
    cart.open_saved_tab().delete_saved(TOTE)

    assert cart.is_saved_empty()
    assert cart.open_cart_tab().is_empty()


@pytest.mark.regression
def test_saved_product_returns_to_the_product_list_once_deleted(guest_shop):
    guest_shop.save_for_later(MUG)
    assert not guest_shop.has_product(MUG)

    saved = guest_shop.open_saved_items()
    saved.open_saved_tab().delete_saved(MUG)
    guest_shop.driver.back()

    guest_shop.wait_until_loaded()
    assert guest_shop.has_product(MUG)
