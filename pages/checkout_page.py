from pages.base_page import BasePage, field_error, rid


class CheckoutPage(BasePage):
    NAME = rid("name_input")
    ADDRESS = rid("address_input")
    CITY = rid("city_input")
    ZIP = rid("zip_input")
    PAY_CARD = rid("pay_card")
    PAY_ON_DELIVERY = rid("pay_on_delivery")
    CARD_SECTION = rid("card_section")
    CARD_NUMBER = rid("card_number_input")
    CARD_EXPIRY = rid("card_expiry_input")
    CARD_CVV = rid("card_cvv_input")
    TOTAL = rid("checkout_total")
    SLIDER = rid("place_order_slider")
    SLIDER_THUMB = rid("swipe_thumb")

    ERRORS = {
        "name": field_error("name_layout"),
        "address": field_error("address_layout"),
        "city": field_error("city_layout"),
        "zip": field_error("zip_layout"),
        "card_number": field_error("card_number_layout"),
        "card_expiry": field_error("card_expiry_layout"),
        "card_cvv": field_error("card_cvv_layout"),
    }

    def wait_until_shown(self):
        self.find(self.NAME)

    def order_total(self):
        self.scroll_to_id("checkout_total")
        return self.text_of(self.TOTAL)

    # --- filling the form ---------------------------------------------------------------

    def enter_shipping(self, name, address, city, zip_code):
        self.send_keys(self.NAME, name)
        self.send_keys(self.ADDRESS, address)
        self.send_keys(self.CITY, city)
        self.send_keys(self.ZIP, zip_code)
        return self

    def enter_zip(self, zip_code):
        self.send_keys(self.ZIP, zip_code)
        return self

    def choose_card(self):
        self.scroll_to_id("pay_card")
        self.click(self.PAY_CARD)
        return self

    def choose_pay_on_delivery(self):
        self.scroll_to_id("pay_on_delivery")
        self.click(self.PAY_ON_DELIVERY)
        return self

    def enter_card(self, number, expiry, cvv):
        self.scroll_to_id("card_number_input")
        self.send_keys(self.CARD_NUMBER, number)
        self.scroll_to_id("card_expiry_input")
        self.send_keys(self.CARD_EXPIRY, expiry)
        self.send_keys(self.CARD_CVV, cvv)
        return self

    def is_card_section_shown(self, timeout=2):
        return self.is_visible(self.CARD_SECTION, timeout)

    # --- placing the order --------------------------------------------------------------

    def swipe_to_place_order(self, fraction=1.0):
        """Drag the slider's handle `fraction` of the way along the track.

        A plain swipe can miss the small handle, so the drag starts at the handle itself.
        Anything under about 80% slides back without placing the order.
        """
        self.scroll_to_id("place_order_slider")
        slider = self.find(self.SLIDER).rect
        thumb = self.find(self.SLIDER_THUMB).rect
        start_x = thumb["x"] + thumb["width"] // 2
        y = thumb["y"] + thumb["height"] // 2
        end_x = int(slider["x"] + slider["width"] * fraction) - 2
        self.driver.execute_script(
            "mobile: dragGesture",
            {"startX": start_x, "startY": y, "endX": end_x, "endY": y, "speed": 800},
        )
        return self

    def place_order(self):
        """A full swipe, then wait for the confirmation screen."""
        from pages.order_complete_page import OrderCompletePage

        self.swipe_to_place_order(1.0)
        page = OrderCompletePage(self.driver)
        page.wait_until_shown()
        return page

    def error(self, field, timeout=5):
        return self.text_of(self.ERRORS[field], timeout)

    def is_error_shown(self, field, timeout=2):
        return self.is_visible(self.ERRORS[field], timeout)
