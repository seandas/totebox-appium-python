import pytest

from tests.data import LOCKED_EMAIL, VALID_EMAIL, VALID_PASSWORD


@pytest.mark.smoke
def test_valid_login_shows_products_and_welcome_toast(login_page):
    login_page.enter_credentials(VALID_EMAIL, VALID_PASSWORD).submit()

    assert login_page.toast_text() == f"Logged in as {VALID_EMAIL}"
    assert login_page.is_gone(login_page.LOGIN_BUTTON), "Login screen still shown after valid login"


@pytest.mark.smoke
def test_continue_as_guest_opens_products(login_page):
    products = login_page.continue_as_guest()

    assert products.is_displayed()
    assert "Canvas Tote Bag" in products.visible_names()


@pytest.mark.regression
def test_helper_text_is_shown_before_typing(login_page):
    assert "valid email" in login_page.text_of(login_page.EMAIL_HELPER)
    assert "8 characters" in login_page.text_of(login_page.PASSWORD_HELPER)


@pytest.mark.regression
def test_empty_form_shows_required_errors(login_page):
    login_page.submit()

    assert login_page.email_error() == "Enter your email"
    assert login_page.password_error() == "Enter your password"


@pytest.mark.regression
def test_invalid_email_is_rejected(login_page):
    login_page.enter_credentials("seand@example", VALID_PASSWORD).submit()

    assert login_page.email_error() == "Enter a valid email address"
    assert login_page.is_displayed(timeout=2), "Should stay on the login screen"


@pytest.mark.regression
@pytest.mark.parametrize(
    "password",
    [
        pytest.param("short#1", id="too-short"),
        pytest.param("password#!", id="no-number"),
        pytest.param("password123", id="no-special-character"),
    ],
)
def test_password_rules(login_page, password):
    login_page.enter_credentials(VALID_EMAIL, password).submit()

    assert "at least 8 characters" in login_page.password_error()
    assert login_page.is_displayed(timeout=2), "Should stay on the login screen"


@pytest.mark.regression
def test_locked_account_cannot_log_in(login_page):
    login_page.enter_credentials(LOCKED_EMAIL, VALID_PASSWORD).submit()

    assert login_page.generic_error() == "This account is locked. Please contact support."
    assert login_page.is_displayed(timeout=2)
