"""Appium session configuration for the Totebox Android app.

Everything is overridable through environment variables, so the same suite can
point at another device or a different build without code changes.

    APPIUM_SERVER_URL   default http://127.0.0.1:4723
    ANDROID_DEVICE_NAME default emulator-5554
    ANDROID_UDID        optional, pin a specific device
    ANDROID_APP_PATH    default apps/totebox-debug.apk (installed at session start)
"""

import os
from pathlib import Path

from appium.options.android import UiAutomator2Options

ROOT = Path(__file__).resolve().parent.parent

APPIUM_SERVER_URL = os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723")

APP_PACKAGE = "com.seandas.totebox"
LAUNCH_ACTIVITY = ".ui.LoginActivity"  # the only exported (launcher) activity
APP_PATH = os.getenv("ANDROID_APP_PATH", str(ROOT / "apps" / "totebox-debug.apk"))


def build_options():
    options = UiAutomator2Options()
    options.device_name = os.getenv("ANDROID_DEVICE_NAME", "emulator-5554")
    if os.getenv("ANDROID_UDID"):
        options.udid = os.getenv("ANDROID_UDID")
    if os.getenv("ANDROID_PLATFORM_VERSION"):
        options.platform_version = os.getenv("ANDROID_PLATFORM_VERSION")

    # Install the APK when we have it; otherwise launch the copy already on the device.
    if Path(APP_PATH).exists():
        options.app = APP_PATH
    options.app_package = APP_PACKAGE
    options.app_activity = LAUNCH_ACTIVITY
    options.app_wait_activity = "*"

    options.no_reset = True  # tests restart the app themselves (see tests/conftest.py)
    options.auto_grant_permissions = True
    options.disable_window_animation = True
    options.new_command_timeout = 300
    return options
