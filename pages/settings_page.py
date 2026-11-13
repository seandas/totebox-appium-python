from pages.base_page import rid
from pages.toolbar import Toolbar


class SettingsPage(Toolbar):
    ACCOUNT = rid("settings_account")
    VERSION = rid("settings_version")
    SPEED_NORMAL = rid("speed_normal")
    SPEED_FAST = rid("speed_fast")
    SPEED_SLOW = rid("speed_slow")

    def wait_until_shown(self):
        self.find(self.ACCOUNT)

    def account_text(self):
        return self.text_of(self.ACCOUNT)

    def version_text(self):
        return self.text_of(self.VERSION)

    def choose_speed(self, speed):
        """speed: 'normal', 'fast' or 'slow'."""
        self.click(rid(f"speed_{speed}"))
        return self

    def is_speed_selected(self, speed):
        return self.find(rid(f"speed_{speed}")).get_attribute("checked") == "true"
