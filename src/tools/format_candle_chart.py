import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")

import mplfinance as mpf
from langchain.tools import tool

from src.utils.logger import Logger
logger = Logger(__name__)

@tool
def format_candle_chart_from_csv(csv_path: str):
    """
    Reads OHLCV data from a CSV file and generates a candlestick chart saved as PNG.
    """
    logger.info(f"Formatting candle chart from CSV.")
    # 1. Load CSV
    df = pd.read_csv(csv_path)

    # 2. Parse and set timestamp as index (required by mplfinance)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp")
    df.index.name = "Date"

    # 3. Rename columns to match mplfinance expectations (capital first letter)
    df = df.rename(columns={
        "open":   "Open",
        "close":  "Close",
        "high":   "High",
        "low":    "Low",
        "volume": "Volume"
    })

    # 4. Sort oldest → newest (required)
    df = df.sort_index()

    logger.info(f"Candle chart data loaded and formatted. Number of candles: {len(df)}")
    # 5. Plot and save as PNG
    output_folder = os.path.join(os.path.dirname(__file__), '../dataset')
    os.makedirs(output_folder, exist_ok=True)
    out_path = os.path.join(output_folder, 'candle_chart.png')
    mpf.plot(
        df,
        type="candle",
        style="charles",        # black/white candles — best for the YOLO model
        volume=True,             # include volume bars at the bottom
        figsize=(40.96, 40.96), # 20.48 inches * 100 dpi = 2048px
        savefig=dict(
            fname=out_path,
            dpi=100,            # 20.48 inches * 100 dpi = 2048px
            bbox_inches="tight"
        )
    )
    logger.info(f"Candle chart saved.")
    return out_path