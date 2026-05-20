import finnhub
import datetime from datetime
from langchain.tools import tool

from configs import FINNHUB_API_KEY

client = finnhub.Client(api_key=FINNHUB_API_KEY)

@tool
def candle_retriever(ticker: str, timestamp: str, resolution: str = "1") -> dict | None:
    """
    Fetch the OHLCV candle at a specific timestamp using Finnhub.

    Args:
        ticker:     Stock ticker (e.g. "AAPL", "IBM")
        timestamp:  Target datetime string "YYYY-MM-DD HH:MM:SS"
        resolution: Candle width — 1, 5, 15, 30, 60, D, W, M

    Returns:
        A dict with open/high/low/close/volume for the matching candle, or None.
    """
    target_dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    target_unix = int(target_dt.timestamp())

    # Fetch a window around the target (±1 day gives enough candles to find the match)
    from_unix = target_unix - 86400   # 1 day before
    to_unix   = target_unix + 86400   # 1 day after

    res = client.stock_candles(ticker, resolution, from_unix, to_unix)

    if res.get("s") != "ok":
        print(f"No data returned. Status: {res.get('s')}")
        return None

    # Zip into list of candles and find the one matching our target timestamp
    candles = list(zip(res["t"], res["o"], res["h"], res["l"], res["c"], res["v"]))

    for t, o, h, l, c, v in candles:
        if t == target_unix:
            return {
                "ticker":    ticker,
                "timestamp": datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M:%S"),
                "open":      o,
                "high":      h,
                "low":       l,
                "close":     c,
                "volume":    v,
            }

    # If exact match not found, show the nearest available timestamps
    print(f"No exact candle at {timestamp}. Nearest available:")
    for t, *_ in candles[:5]:
        print(f"  {datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')}")
    return None
    