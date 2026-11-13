import re
from datetime import datetime
from pathlib import Path

import pytest
from appium import webdriver

from config.capabilities import APP_PACKAGE, APPIUM_SERVER_URL, LAUNCH_ACTIVITY, build_options
from pages.login_page import LoginPage
from tests.data import VALID_EMAIL, VALID_PASSWORD

ARTIFACTS_DIR = Path(__file__).resolve().parent.parent / "artifacts"


@pytest.fixture(scope="session")
def _session_driver():
    # One Appium session for the whole run: starting a session installs and launches
    # the app, which is the slowest step. Tests stay independent through `driver` below.
    driver = webdriver.Remote(APPIUM_SERVER_URL, options=build_options())
    yield driver
    driver.quit()


@pytest.fixture
def driver(request, _session_driver):
    """The shared session with the app freshly restarted.

    Totebox keeps its state (login, guest mode, cart, saved items) in memory only, so
    killing the process gives every test a clean, logged-out app.
    """
    _session_driver.terminate_app(APP_PACKAGE)
    # NEW_TASK | CLEAR_TASK: start the login screen in a fresh task rather than
    # letting Android resume whatever screen the killed app was last on.
    _session_driver.execute_script(
        "mobile: startActivity",
        {"intent": f"{APP_PACKAGE}/{LAUNCH_ACTIVITY}", "flags": "0x10008000"},
    )
    request.node._driver = _session_driver  # lets the failure hook below reach it
    return _session_driver


@pytest.fixture
def login_page(driver):
    """The app, just launched, on the login screen."""
    page = LoginPage(driver)
    page.wait_until_shown()
    return page


@pytest.fixture
def guest_shop(login_page):
    """The product list, browsing as a guest."""
    return login_page.continue_as_guest()


@pytest.fixture
def shop(login_page):
    """The product list, logged in."""
    return login_page.log_in(VALID_EMAIL, VALID_PASSWORD)


@pytest.hookimpl(wrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """On a failed test, save a screenshot, the UI hierarchy and the device log."""
    report = yield
    if report.when == "call" and report.failed:
        driver = getattr(item, "_driver", None)
        if driver is not None:
            _save_failure_artifacts(driver, item.nodeid)
    return report


def _save_failure_artifacts(driver, nodeid):
    ARTIFACTS_DIR.mkdir(exist_ok=True)
    name = re.sub(r"[^\w.-]+", "_", nodeid)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    base = ARTIFACTS_DIR / f"{name}-{stamp}"
    try:
        driver.save_screenshot(f"{base}.png")
        Path(f"{base}.xml").write_text(driver.page_source, encoding="utf-8")
        logcat = "\n".join(entry["message"] for entry in driver.get_log("logcat")[-300:])
        Path(f"{base}.log").write_text(logcat, encoding="utf-8")
        _attach_to_allure(base)
    except Exception as exc:  # never let artifact capture mask the real failure
        print(f"Could not save failure artifacts for {nodeid}: {exc}")


def _attach_to_allure(base):
    try:
        import allure
    except ImportError:
        return
    allure.attach.file(f"{base}.png", "Screenshot", allure.attachment_type.PNG)
    allure.attach.file(f"{base}.xml", "UI hierarchy", allure.attachment_type.XML)
    allure.attach.file(f"{base}.log", "Device log (last 300 lines)", allure.attachment_type.TEXT)
