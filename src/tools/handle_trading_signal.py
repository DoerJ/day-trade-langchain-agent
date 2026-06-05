import asyncio
from datetime import datetime
from enum import Enum
from langchain.tools import tool
import telegram

from src.configs import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from src.utils.logger import Logger

logger = Logger(__name__)

async def send_telegram_message(message: str) -> bool:
    """Send a message to the configured Telegram chat. Returns True on success."""
    try:
        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
        logger.info(f"Sending Telegram message to chat ID {TELEGRAM_CHAT_ID}:\n{message}")
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

    # Normalize signal input and determine direction. Gracefully handle unknown values.
    signal_str = str(signal).upper() if signal is not None else ""
    if signal_str == "UP":
        direction = "BULLISH"
    elif signal_str == "DOWN":
        direction = "BEARISH"
    else:
        direction = "NEUTRAL"
        logger.warning("Unrecognized trading signal '%s' for asset %s", signal, asset)

    lines = [
        "",
        f"<b>Asset :</b> {asset}",
        f"<b>Signal:</b> {signal} ({direction})",
        f"<b>Confidence score  :</b> {conf_score:.2%}",
        f"<b>Time  :</b> {timestamp}",
    ]

    if direction == "NEUTRAL":
        lines.append("<b>Note:</b> Signal not recognized or not actionable. No trade recommended.")
        logger.info("Neutral signal for %s — skipping Telegram notification.", asset)
        return False

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
