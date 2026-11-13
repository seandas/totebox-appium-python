from appium.webdriver.common.appiumby import AppiumBy

from config.capabilities import APP_PACKAGE
from pages.base_page import a11y, rid, uia
from pages.toolbar import Toolbar


def _in_row(product, field_id):
    """A field inside the cart row of one product.

    XPath is the last resort and is needed here: rows have no ID of their own and the
    quantity/price fields are siblings of the name, not children. The expression finds the
    row by its product name, then the nearest ancestor that contains the wanted field.
    """
    name = f'//*[@resource-id="{APP_PACKAGE}:id/cart_item_name" and @text="{product}"]'
    field = f"{APP_PACKAGE}:id/{field_id}"
    return (AppiumBy.XPATH, f'{name}/ancestor::*[.//*[@resource-id="{field}"]][1]//*[@resource-id="{field}"]')


class CartPage(Toolbar):
    CART_TAB = uia('new UiSelector().textStartsWith("Cart (")')
    SAVED_TAB = uia('new UiSelector().textStartsWith("Saved for later (")')

    CART_LIST = rid("cart_list")
    CART_EMPTY_TEXT = rid("cart_empty_text")
    START_SHOPPING = rid("start_shopping_button")
    SUBTOTAL = rid("cart_subtotal")
    SHIPPING = rid("cart_shipping")
    TOTAL = rid("cart_total")
    FREE_SHIPPING_HINT = rid("free_shipping_hint")
    CHECKOUT = rid("checkout_button")

    SAVED_LIST = rid("saved_list")
    SAVED_EMPTY_TEXT = rid("saved_empty_text")

    def wait_until_shown(self):
        self.find(self.CART_TAB)

    # --- cart tab -----------------------------------------------------------------------

    def line_names(self):
        return [e.text for e in self.driver.find_elements(*rid("cart_item_name"))]

    def has_line(self, product, timeout=3):
        return self.is_visible(uia(f'new UiSelector().resourceId("{APP_PACKAGE}:id/cart_item_name").text("{product}")'), timeout)

    def quantity_of(self, product):
        return int(self.text_of(_in_row(product, "cart_item_qty")))

    def line_total_of(self, product):
        return self.text_of(_in_row(product, "cart_item_line_total"))

    def increase(self, product):
        self.click(a11y(f"Increase quantity of {product}"))
        return self

    def decrease(self, product):
        self.click(a11y(f"Decrease quantity of {product}"))
        return self

    def remove(self, product):
        self.click(a11y(f"Remove {product} from cart"))
        return self

    def save_for_later(self, product):
        self.click(a11y(f"Save {product} for later"))
        return self

    def subtotal(self):
        return self.text_of(self.SUBTOTAL)

    def shipping(self):
        return self.text_of(self.SHIPPING)

    def total(self):
        return self.text_of(self.TOTAL)

    def is_empty(self, timeout=5):
        return self.is_visible(self.CART_EMPTY_TEXT, timeout)

    def start_shopping(self):
        from pages.products_page import ProductsPage

        self.click(self.START_SHOPPING)
        page = ProductsPage(self.driver)
        page.wait_until_loaded()
        return page

    def is_free_shipping_hint_shown(self, timeout=2):
        return self.is_visible(self.FREE_SHIPPING_HINT, timeout)

    def checkout(self):
        from pages.checkout_page import CheckoutPage

        self.click(self.CHECKOUT)
        page = CheckoutPage(self.driver)
        page.wait_until_shown()
        return page

    def checkout_as_guest(self):
        """A guest is sent to the login screen first; their cart is kept."""
        from pages.login_page import LoginPage

        self.click(self.CHECKOUT)
        page = LoginPage(self.driver)
        page.wait_until_shown()
        return page

    # --- saved for later tab ------------------------------------------------------------

    def open_saved_tab(self):
        self.click(self.SAVED_TAB)
        return self

    def open_cart_tab(self):
        self.click(self.CART_TAB)
        return self

    def saved_names(self):
        return [e.text for e in self.driver.find_elements(*rid("saved_item_name"))]

    def has_saved(self, product, timeout=3):
        return self.is_visible(uia(f'new UiSelector().resourceId("{APP_PACKAGE}:id/saved_item_name").text("{product}")'), timeout)

    def is_saved_empty(self, timeout=5):
        return self.is_visible(self.SAVED_EMPTY_TEXT, timeout)

    def move_to_cart(self, product):
        self.click(a11y(f"Move {product} to cart"))
        return self

    def delete_saved(self, product):
        self.click(a11y(f"Delete {product} from saved items"))
        return self

    def tab_titles(self):
        return self.text_of(self.CART_TAB), self.text_of(self.SAVED_TAB)
