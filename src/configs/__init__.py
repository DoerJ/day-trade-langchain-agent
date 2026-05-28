import os
from dotenv import load_dotenv
load_dotenv()

AGENT_LOOP_SECONDS = int(os.getenv("AGENT_LOOP_SECONDS", 5))
TICKER = os.getenv("TICKER")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")