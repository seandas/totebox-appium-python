from pages.base_page import BasePage, rid


class ProductDetailPage(BasePage):
    NAME = rid("detail_name")
    PRICE = rid("detail_price")
    QTY_VALUE = rid("qty_value")
    QTY_MINUS = rid("qty_minus")
    QTY_PLUS = rid("qty_plus")
    ADD_TO_CART = rid("add_to_cart_button")

    def wait_until_shown(self):
        self.find(self.ADD_TO_CART)

    def name(self):
        return self.text_of(self.NAME)

    def quantity(self):
        return int(self.text_of(self.QTY_VALUE))

    def increase(self, times=1):
        for _ in range(times):
            self.click(self.QTY_PLUS)
        return self

    def is_plus_enabled(self):
        return self.find(self.QTY_PLUS).is_enabled()

    def is_minus_enabled(self):
        return self.find(self.QTY_MINUS).is_enabled()

    def decrease(self, times=1):
        for _ in range(times):
            self.click(self.QTY_MINUS)
        return self

    def add_to_cart(self):
        self.click(self.ADD_TO_CART)
        return self

    def view_cart_from_snackbar(self):
        from pages.cart_page import CartPage

        self.click(self.SNACKBAR_ACTION)
        page = CartPage(self.driver)
        page.wait_until_shown()
        return page
