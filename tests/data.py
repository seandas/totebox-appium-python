"""Test data. Values come from the Totebox app (data/Catalog.kt, LoginRules, CheckoutValidator)."""

VALID_EMAIL = "seand@example.com"
VALID_PASSWORD = "secret#42"  # 8+ characters, a number and a special character
LOCKED_EMAIL = "locked@totebox.app"

# Products and prices (dollars) from the catalog.
TOTE = "Canvas Tote Bag"            # $24.99
MUG = "Ceramic Travel Mug"          # $18.99
EARBUDS = "Wireless Earbuds"        # $59.99 (over the $50 free shipping line on its own)
PLANT = "Desk Plant"                # $14.99
PHONE_STAND = "Phone Stand"         # $9.99, the cheapest
CRASH_ITEM = "Crash test item"

SHIPPING_FEE = "$4.99"
FREE_SHIPPING = "Free"
MAX_QUANTITY = 10

# Shipping and payment
NAME = "Sean Tester"
ADDRESS = "1 Main Street"
CITY = "Springfield"
ZIP = "12345"
CARD_NUMBER = "4111111111111111"
CARD_EXPIRY = "12/30"
CARD_CVV = "123"

ORDER_NUMBER_PATTERN = r"^Order number: TB-\d{6}$"
