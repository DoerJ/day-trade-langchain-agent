import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import csv
from langchain.tools import tool
from tests import MOCK_CANDLE

@tool
def save_candles_to_csv(candlestick, filename="candle_data.csv"):
    """
    Appends candlestick data (dict or list of dicts) to a CSV file in /dataset.
    Args:
        candlestick: dict or list of dicts with keys 'open', 'close', 'high', 'low', 'volume', 'timestamp'.
        filename: CSV file name (default: 'candle_data.csv').
    Returns:
        The full path to the saved CSV file.
    """
    output_folder = os.path.join(os.path.dirname(__file__), '../dataset')
    os.makedirs(output_folder, exist_ok=True)
    csv_path = os.path.join(output_folder, filename)
    fieldnames = ["timestamp", "volume", "high", "low", "open", "close"]
    write_header = not os.path.exists(csv_path)

    if isinstance(candlestick, dict):
        # Append single candlestick
        mode = "a"
        candlesticks = [candlestick]
        write_header = not os.path.exists(csv_path)
    elif isinstance(candlestick, list):
        # Overwrite with list of candlesticks
        mode = "w"
        candlesticks = candlestick
        write_header = True
    else:
        raise ValueError("candlestick must be a dict or list of dicts")

    with open(csv_path, mode, newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        for candle in candlesticks:
            writer.writerow({k: candle[k] for k in fieldnames})
    return csv_path
