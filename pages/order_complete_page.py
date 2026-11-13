from pages.base_page import BasePage, rid


class OrderCompletePage(BasePage):
    THANKS = rid("order_thanks")
    ORDER_NUMBER = rid("order_number")
    TOTAL = rid("order_total")
    CONTINUE = rid("continue_button")

    def wait_until_shown(self, timeout=20):
        self.find(self.THANKS, timeout)

    def is_displayed(self, timeout=None):
        return self.is_visible(self.THANKS, timeout)

    def order_number(self):
        return self.text_of(self.ORDER_NUMBER)

    def total(self):
        return self.text_of(self.TOTAL)

    def continue_shopping(self):
        from pages.products_page import ProductsPage

        self.click(self.CONTINUE)
        page = ProductsPage(self.driver)
        page.wait_until_loaded()
        return page
