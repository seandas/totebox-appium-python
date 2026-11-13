import time

import pytest

from tests.data import TOTE, VALID_EMAIL, VALID_PASSWORD


@pytest.mark.regression
def test_settings_shows_the_logged_in_account(shop):
    settings = shop.open_settings()

    assert settings.account_text() == f"Logged in as {VALID_EMAIL}"
    assert settings.version_text().startswith("Version ")


@pytest.mark.regression
def test_settings_shows_guest_mode(guest_shop):
    settings = guest_shop.open_settings()

    assert settings.account_text() == "Browsing as a guest"


@pytest.mark.regression
def test_network_speed_can_be_changed(shop):
    settings = shop.open_settings()

    settings.choose_speed("fast")

    assert settings.is_speed_selected("fast")
    assert not settings.is_speed_selected("normal")


@pytest.mark.regression
def test_log_out_returns_to_the_login_screen(shop):
    login = shop.log_out()

    assert login.is_displayed()


@pytest.mark.regression
def test_home_menu_returns_to_products_from_settings(shop):
    settings = shop.open_settings()

    products = settings.open_home()

    assert products.is_displayed()
    assert TOTE in products.visible_names()


@pytest.mark.regression
def test_guest_menu_shows_log_in_and_keeps_cart(guest_shop):
    guest_shop.add_to_cart(TOTE)

    login = guest_shop.log_in_from_menu()
    products = login.log_in(VALID_EMAIL, VALID_PASSWORD)

    assert products.cart_badge_count() == 1
    assert products.open_cart().has_line(TOTE)


@pytest.mark.regression
def test_network_speed_affects_load_times(shop):
    settings = shop.open_settings()
    settings.choose_speed("fast")
    login = settings.log_out()
    start_fast = time.monotonic()
    products = login.log_in(VALID_EMAIL, VALID_PASSWORD)
    fast_elapsed = time.monotonic() - start_fast

    settings = products.open_settings()
    settings.choose_speed("slow")
    login = settings.log_out()
    start_slow = time.monotonic()
    products = login.log_in(VALID_EMAIL, VALID_PASSWORD)
    slow_elapsed = time.monotonic() - start_slow

    assert products.is_displayed()
    assert slow_elapsed > fast_elapsed + 3.0, (
        f"Expected slow ({slow_elapsed:.2f}s) to be noticeably slower than fast ({fast_elapsed:.2f}s)"
    )
