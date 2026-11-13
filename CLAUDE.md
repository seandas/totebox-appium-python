# Automation conventions for this repo

Context for AI coding assistants. Follow these when generating or editing code here.

## Stack
- Python 3.10+, pytest, Appium Python Client 6.x, Appium 2/3 server, UiAutomator2 driver
- Android only. The app under test is **Totebox** (`com.seandas.totebox`), the Kotlin
  shopping app in `../Totebox`. Its APK is copied to `apps/totebox-debug.apk`.
- Session options are built in `config/capabilities.py` with `UiAutomator2Options`.
  No raw `desired_capabilities` dicts.

## Structure
- `pages/` page objects, one per screen. Store screens subclass `Toolbar` (cart icon,
  badge, ⋮ menu), which subclasses `BasePage`.
- `tests/` compose page-object methods; no raw `driver.find_element` in tests.
- `tests/conftest.py` owns the driver, app restart and failure artifacts. Don't duplicate it.
- `tests/data.py` holds all test data (accounts, products, card, expected strings).

## Locators
1. Never guess a locator. IDs come from the app's layouts (`../Totebox/app/src/main/res/layout`)
   or a real UI dump (`adb shell uiautomator dump`, Appium Inspector).
2. Order of preference: resource ID via `rid("name")`, accessibility label via `a11y("...")`
   (rows' buttons carry labels like "Add Canvas Tote Bag to cart"), `uia(...)` UiSelector,
   XPath only as a last resort with a comment saying why.
3. Locators are class-level tuples on the page object.

## Synchronization
- Use `BasePage` helpers (explicit waits). No `time.sleep`, no implicit waits.
- The product list appears after a simulated network delay; use `wait_until_loaded()`.
- `is_visible` / `is_gone` return booleans; pass a short `timeout` for negative checks.

## Tests
- One behavior per test, independent of order. The app is killed and relaunched
  fresh (logged out, empty cart) before every test by the `driver` fixture.
- Fixtures: `login_page`, `guest_shop`, `shop` (logged in).
- Mark tests `smoke`, `regression`, and `crash` (the deliberate crash item).
- Assertions must prove the behavior, not just that a screen exists.

## Avoid
- `find_element_by_*`, `MobileBy`, `TouchAction`, `/wd/hub`. Use W3C actions or `mobile:` commands.
