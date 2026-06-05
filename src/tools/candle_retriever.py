import requests
import time
from langchain.tools import tool

from src.configs import YAHOO_FINANCE_QUERY_API
from src.utils.logger import Logger

logger = Logger(__name__)

@tool
def candle_retriever(ticker: str) -> dict:
	"""
	Retrieve the current day's candlestick data for the given ticker from Yahoo Finance.

	Args:
		ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT')

	Returns:
		A dict with open, high, low, close, volume, and timestamps for the current day.
		Returns None if data is unavailable.
	"""
	# Get today's midnight and now as UNIX timestamps
	now = int(time.time())
	today = time.localtime(now)
	midnight = int(time.mktime((today.tm_year, today.tm_mon, today.tm_mday, 0, 0, 0, 0, 0, -1)))

	url = f"{YAHOO_FINANCE_QUERY_API}/{ticker}"
	params = {
		"period1": midnight,
		"period2": now,
		"interval": "1m",
		"includePrePost": "false"
	}
	headers = {
		"User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.0.3705;)"
	}
	try:
		resp = requests.get(url, params=params, headers=headers, timeout=10)
		resp.raise_for_status()
		data = resp.json()
		chart = data.get("chart", {})
		result = chart.get("result", [{}])[0]
		indicators = result.get("indicators", {})
		quote = indicators.get("quote", [{}])[0]
		timestamps = result.get("timestamp", [])
		if not timestamps or not quote:
			return None
		candles = []
		for i, t in enumerate(timestamps):
			candle = {
				"timestamp": t,
				"datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t)),
				"open": quote["open"][i] if "open" in quote else None,
				"high": quote["high"][i] if "high" in quote else None,
				"low": quote["low"][i] if "low" in quote else None,
				"close": quote["close"][i] if "close" in quote else None,
				"volume": quote["volume"][i] if "volume" in quote else None
			}
			candles.append(candle)
		return {
			"ticker": ticker,
			"candles": candles
		}
	except Exception as e:
		logger.error(f"Error retrieving Yahoo Finance candles: {e}")
		return None


# import finnhub
# from datetime import datetime
# from langchain.tools import tool

# from configs import FINNHUB_API_KEY

# client = finnhub.Client(api_key=FINNHUB_API_KEY)

# @tool
# def candle_retriever(ticker: str, resolution: str = "1") -> dict:
#     """
#     Fetch the OHLCV candle at a specific timestamp using finnhub-python.

#     Args:
#         ticker:     Stock ticker (e.g. "AAPL", "IBM")
#         timestamp:  Target datetime string "YYYY-MM-DD HH:MM:SS"
#         resolution: Candle width — "1" for 1-minute, "5" for 5-min, etc.

#     Returns:
#         A dict with open/high/low/close/volume for the matching candle, or None if not found.
#     """
#     try:
#         timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         target_dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
#         target_unix = int(target_dt.timestamp())

#         # Fetch a window around the target (±1 hour gives enough candles to find the match)
#         from_unix = target_unix - 3600   # 1 hour before
#         to_unix   = target_unix + 3600   # 1 hour after

#         res = client.stock_candles(ticker, resolution, from_unix, to_unix)

#         if res.get("s") != "ok":
#             print(f"No data returned. Status: {res.get('s')}")
#             return None

#         # Zip into list of candles and find the one matching our target timestamp
#         candles = list(zip(res["t"], res["o"], res["h"], res["l"], res["c"], res["v"]))

#         for t, o, h, l, c, v in candles:
#             if t == target_unix:
#                 return {
#                     "ticker":    ticker,
#                     "timestamp": datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M:%S"),
#                     "open":      o,
#                     "high":      h,
#                     "low":       l,
#                     "close":     c,
#                     "volume":    v,
#                 }

#         # If exact match not found, show the nearest available timestamps
#         print(f"No exact candle at {timestamp}. Nearest available:")
#         for t, *_ in candles[:5]:
#             print(f"  {datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')}")
#         return None
#     except Exception as e:
#         print(f"Error retrieving candle: {e}")
#         return None