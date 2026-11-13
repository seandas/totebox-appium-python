from pages.base_page import BasePage, field_error, field_helper, rid


class LoginPage(BasePage):
    TITLE = rid("app_title")
    EMAIL = rid("email_input")
    PASSWORD = rid("password_input")
    LOGIN_BUTTON = rid("login_button")
    GUEST_BUTTON = rid("guest_button")
    GENERIC_ERROR = rid("login_error")  # login failed / account locked
    CHECKOUT_MESSAGE = rid("checkout_login_message")  # only when arriving from checkout
    PROGRESS = rid("login_progress")

    EMAIL_ERROR = field_error("email_layout")
    PASSWORD_ERROR = field_error("password_layout")
    EMAIL_HELPER = field_helper("email_layout")
    PASSWORD_HELPER = field_helper("password_layout")

    def wait_until_shown(self):
        self.find(self.LOGIN_BUTTON)

    def is_displayed(self, timeout=None):
        return self.is_visible(self.LOGIN_BUTTON, timeout)

    def enter_credentials(self, email, password):
        self.send_keys(self.EMAIL, email)
        self.send_keys(self.PASSWORD, password)
        return self

    def submit(self):
        if self.driver.is_keyboard_shown():
            self.driver.hide_keyboard()
        self.click(self.LOGIN_BUTTON)
        return self

    def log_in(self, email, password):
        """Log in and wait for the product list."""
        from pages.products_page import ProductsPage

        self.enter_credentials(email, password).submit()
        products = ProductsPage(self.driver)
        products.wait_until_loaded()
        return products

    def log_in_to_checkout(self, email, password):
        """Log in when redirected from guest checkout, returning to the checkout screen."""
        from pages.checkout_page import CheckoutPage

        self.enter_credentials(email, password).submit()
        checkout = CheckoutPage(self.driver)
        checkout.wait_until_shown()
        return checkout

    def continue_as_guest(self):
        from pages.products_page import ProductsPage

        self.click(self.GUEST_BUTTON)
        products = ProductsPage(self.driver)
        products.wait_until_loaded()
        return products

    def email_error(self, timeout=5):
        return self.text_of(self.EMAIL_ERROR, timeout)

    def password_error(self, timeout=5):
        return self.text_of(self.PASSWORD_ERROR, timeout)

    def generic_error(self, timeout=10):
        """The error under the form after a login that reached the (fake) server."""
        return self.text_of(self.GENERIC_ERROR, timeout)
