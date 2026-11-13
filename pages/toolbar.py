from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage, rid, uia


class Toolbar(BasePage):
    """The toolbar shared by every store screen: cart icon with badge, and the ⋮ menu."""

    CART_ACTION = rid("cart_action")
    CART_BADGE = rid("cart_badge")
    OVERFLOW = (AppiumBy.ACCESSIBILITY_ID, "More options")  # AppCompat's own label

    def cart_badge_count(self, timeout=3):
        """The number on the cart badge, or 0 when the badge is hidden."""
        try:
            return int(self.find(self.CART_BADGE, timeout).text)
        except TimeoutException:
            return 0

    def open_cart(self):
        from pages.cart_page import CartPage

        self.click(self.CART_ACTION)
        page = CartPage(self.driver)
        page.wait_until_shown()
        return page

    def choose_menu_item(self, title):
        self.click(self.OVERFLOW)
        self.click(uia(f'new UiSelector().text("{title}")'))

    def open_home(self):
        from pages.products_page import ProductsPage

        self.choose_menu_item("Home")
        page = ProductsPage(self.driver)
        page.wait_until_loaded()
        return page

    def open_settings(self):
        from pages.settings_page import SettingsPage

        self.choose_menu_item("Settings")
        page = SettingsPage(self.driver)
        page.wait_until_shown()
        return page

    def open_saved_items(self):
        from pages.cart_page import CartPage

        self.choose_menu_item("Saved items")
        page = CartPage(self.driver)
        page.wait_until_shown()
        return page

    def log_out(self):
        from pages.login_page import LoginPage

        self.choose_menu_item("Log out")
        page = LoginPage(self.driver)
        page.wait_until_shown()
        return page

    def log_in_from_menu(self):
        """A guest's overflow menu shows 'Log in' instead of 'Log out'; the cart is kept."""
        from pages.login_page import LoginPage

        self.choose_menu_item("Log in")
        page = LoginPage(self.driver)
        page.wait_until_shown()
        return page
