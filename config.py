# config.py
import os

# 🔐 Get values from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("25017900"))
API_HASH = os.getenv("3830600881a164826e60f2806b28e666")

# ✅ Make sure to set these values before running the bot
# Example (for local testing):
# export BOT_TOKEN="your_bot_token"
# export API_ID=1234567
# export API_HASH="your_api_hash"
