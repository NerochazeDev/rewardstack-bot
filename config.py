import os

# Bot token (set in environment variables)
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Admin Telegram ID
ADMIN_CHAT_ID = int(os.environ.get("ADMIN_CHAT_ID", "0"))

# Booster plans
PLANS = {
    0: {"daily": 5, "min_withdraw": 50},
    10: {"daily": 10, "min_withdraw": 100},
    15: {"daily": 15, "min_withdraw": 150},
    30: {"daily": 20, "min_withdraw": 200},
    50: {"daily": 40, "min_withdraw": 400},
}
