from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.capabilities import APP_PACKAGE

DEFAULT_TIMEOUT = 15


def rid(name):
    """Locator for one of the app's resource IDs, e.g. rid("login_button")."""
    return (AppiumBy.ID, f"{APP_PACKAGE}:id/{name}")


def uia(selector):
    """Locator from a UiSelector expression (preferred over XPath)."""
    return (AppiumBy.ANDROID_UIAUTOMATOR, selector)


def a11y(label):
    """Locator for an accessibility label (content-desc)."""
    return (AppiumBy.ACCESSIBILITY_ID, label)


class BasePage:
    """Explicit-wait helpers shared by every page object. No sleeps, no implicit waits."""

    def __init__(self, driver, timeout=DEFAULT_TIMEOUT):
        self.driver = driver
        self.timeout = timeout

    def _wait(self, timeout=None):
        return WebDriverWait(self.driver, timeout or self.timeout)

    def find(self, locator, timeout=None):
        """Wait until the element is visible and return it."""
        return self._wait(timeout).until(EC.visibility_of_element_located(locator))

    def click(self, locator, timeout=None):
        self._wait(timeout).until(EC.element_to_be_clickable(locator)).click()

    def send_keys(self, locator, text, timeout=None):
        element = self.find(locator, timeout)
        element.clear()
        element.send_keys(text)

    def text_of(self, locator, timeout=None):
        return self.find(locator, timeout).text

    def is_visible(self, locator, timeout=None):
        """True if the element becomes visible within the timeout.

        Only a timeout counts as "not visible"; anything else (bad locator,
        dead session) is a real error and is allowed to raise.
        """
        try:
            self.find(locator, timeout)
            return True
        except TimeoutException:
            return False

    def is_gone(self, locator, timeout=None):
        """True once the element is absent or hidden within the timeout."""
        try:
            self._wait(timeout).until(EC.invisibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def scroll_to_id(self, name):
        """Scroll the first scrollable container until the resource ID is on screen."""
        self.driver.find_element(
            *uia(
                'new UiScrollable(new UiSelector().scrollable(true).instance(0))'
                f'.scrollIntoView(new UiSelector().resourceId("{APP_PACKAGE}:id/{name}"))'
            )
        )

    def scroll_to_text(self, list_id, text):
        """Scroll a list (by resource ID) until a row with this exact text is on screen."""
        self.driver.find_element(
            *uia(
                f'new UiScrollable(new UiSelector().resourceId("{APP_PACKAGE}:id/{list_id}"))'
                f'.scrollIntoView(new UiSelector().text("{text}"))'
            )
        )

    # --- messages that appear briefly -------------------------------------------------

    TOAST = (AppiumBy.XPATH, "//android.widget.Toast")  # toasts have no ID or content-desc
    SNACKBAR_TEXT = rid("snackbar_text")  # Material Snackbar's own ID
    SNACKBAR_ACTION = rid("snackbar_action")

    def toast_text(self, timeout=5):
        """Text of the toast currently showing. Toasts are found by class only."""
        return self._wait(timeout).until(EC.presence_of_element_located(self.TOAST)).text

    def snackbar_text(self, timeout=5):
        return self.find(self.SNACKBAR_TEXT, timeout).text


def field_error(layout_id):
    """Error text of a Material TextInputLayout (by the layout's ID).

    The error TextView only has Material's generic ID, shared by every field, so it
    is located as a child of the field's own layout.
    """
    return uia(
        f'new UiSelector().resourceId("{APP_PACKAGE}:id/{layout_id}")'
        f'.childSelector(new UiSelector().resourceId("{APP_PACKAGE}:id/textinput_error"))'
    )


def field_helper(layout_id):
    """Helper text of a Material TextInputLayout (hidden while the field shows an error)."""
    return uia(
        f'new UiSelector().resourceId("{APP_PACKAGE}:id/{layout_id}")'
        f'.childSelector(new UiSelector().resourceId("{APP_PACKAGE}:id/textinput_helper_text"))'
    )
