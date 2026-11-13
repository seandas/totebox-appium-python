from selenium.common.exceptions import NoSuchElementException

from pages.base_page import a11y, rid, uia
from pages.toolbar import Toolbar


class ProductsPage(Toolbar):
    LIST = rid("products_list")
    LOADING = rid("products_loading")
    SORT_SPINNER = rid("sort_spinner")
    PRODUCT_NAME = rid("product_name")
    PRODUCT_PRICE = rid("product_price")

    def wait_until_loaded(self):
        """The list appears after a short simulated network delay."""
        self.is_gone(self.LOADING, timeout=20)
        self.find(self.LIST)
        self.find(self.PRODUCT_NAME)

    def is_displayed(self, timeout=None):
        return self.is_visible(self.LIST, timeout)

    # --- reading the list ---------------------------------------------------------------

    def visible_names(self):
        """Names of the rows currently on screen, top to bottom."""
        return [e.text for e in self.driver.find_elements(*self.PRODUCT_NAME)]

    def visible_prices(self):
        """Prices of the rows currently on screen, in dollars, top to bottom."""
        return [float(e.text.lstrip("$")) for e in self.driver.find_elements(*self.PRODUCT_PRICE)
                if e.text.startswith("$")]

    def has_product(self, name):
        """True if the product is anywhere in the list (scrolls to look for it)."""
        try:
            self.scroll_to_text("products_list", name)
            return True
        except NoSuchElementException:
            return False

    # --- actions ------------------------------------------------------------------------

    def sort_by(self, option):
        self.click(self.SORT_SPINNER)
        self.click(uia(f'new UiSelector().text("{option}")'))
        return self

    def add_to_cart(self, name):
        self.scroll_to_text("products_list", name)
        self.click(a11y(f"Add {name} to cart"))
        return self

    def save_for_later(self, name):
        self.scroll_to_text("products_list", name)
        self.click(a11y(f"Save {name} for later"))
        return self

    def open_details(self, name):
        from pages.product_detail_page import ProductDetailPage

        self.scroll_to_text("products_list", name)
        self.click(uia(f'new UiSelector().resourceId("{self.PRODUCT_NAME[1]}").text("{name}")'))
        page = ProductDetailPage(self.driver)
        page.wait_until_shown()
        return page
