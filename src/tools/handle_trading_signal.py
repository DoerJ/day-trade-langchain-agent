import asyncio
import logging
from datetime import datetime
from enum import Enum
from langchain.tools import tool
import telegram

from src.configs import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def send_telegram_message(message: str) -> bool:
    """Send a message to the configured Telegram chat. Returns True on success."""
    try:
        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
        print(f"Sending Telegram message to chat ID {TELEGRAM_CHAT_ID}:\n{message}")
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message,
            parse_mode="HTML",
        )
        logger.info("Telegram message sent successfully.")
        return True
    except telegram.error.TelegramError as e:
        logger.error("Failed to send Telegram message: %s", e)
        return False


async def notify_trading_signal(
    signal: str,
    conf_score: float,
    asset: str = "Unknown"
) -> bool:
    """
    Send a trading signal notification to Telegram.

    Parameters
    ----------
    signal     : Signal.UP or Signal.DOWN (or the strings "UP" / "DOWN")
    asset      : ticker / instrument name, e.g. "BTC/USDT" or "AAPL"

    Returns True if the message was delivered successfully.
    """

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    direction = "BULLISH" if signal == "UP" else "BEARISH"

    lines = [
        "",
        f"<b>Asset :</b> {asset}",
        f"<b>Signal:</b> {signal} ({direction})",
        f"<b>Confidence score  :</b> {conf_score:.2%}",
        f"<b>Time  :</b> {timestamp}",
    ]

    message = "\n".join(lines)
    return await send_telegram_message(message)

@tool
def notify_signal_sync(
    signal: str,
    conf_score: float,
    asset: str = "Unknown"
) -> bool:
    """Synchronous wrapper around notify_trading_signal."""
    return asyncio.run(notify_trading_signal(signal, conf_score, asset))
