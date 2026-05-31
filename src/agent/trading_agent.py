from langchain.chains.base import Chain
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

from src.tools.format_candle_chart import format_candle_chart_from_csv
from src.tools.save_candles_to_csv import save_candles_to_csv
from src.tools.candle_retriever import candle_retriever
from src.tools.detect_pattern_from_chart import detect_pattern_from_chart
from src.tools.handle_trading_signal import notify_signal_sync
from src.tools.candle_retriever import candle_retriever
from src.tests import MOCK_CANDLE


# class TradingAnalysisChain(Chain):
#     input_keys = ["ticker", "market_status", "candle_text"]
#     output_keys = ["signal", "analysis"]

#     def __init__(self, llm, retriever, prompt_template: PromptTemplate):
#         super().__init__()
#         self.llm = llm
#         self.retriever = retriever
#         self.prompt_template = prompt_template

#     def _call(self, inputs: dict) -> dict:
#         ticker = inputs["ticker"]
#         market_status = inputs["market_status"]
#         candle_text = inputs["candle_text"]

#         retrieved_docs = self.retriever.get_relevant_documents(candle_text)
#         retrieved_text = "\n\n".join(
#             f"---\n{doc.page_content}" for doc in retrieved_docs
#         )

#         prompt = self.prompt_template.format(
#             ticker=ticker,
#             market_status=market_status,
#             candle_data=candle_text,
#             retrieved_docs=retrieved_text,
#         )

#         raw_answer = self.llm.predict(prompt)
#         normalized = raw_answer.strip().lower()
#         if "buy" in normalized:
#             signal = "buy"
#         elif "sell" in normalized:
#             signal = "sell"
#         else:
#             signal = "hold"

#         return {"signal": signal, "analysis": raw_answer}


class TradingAgent:
    def __init__(self, ticker):
        self.ticker = ticker
        self.chain = self.build_chain()

    def build_chain(self):
        """
        Custom chain for trading analysis.

        - Retrieve candlestick data at the current timestamp.
        - Append candlestick data to CSV file.
        - Format CSV data into a candlestick chart image.
        - Feed the image into a YOLO model to detect patterns.
        - Signal BUY/SELL/HOLD based on detected patterns through Telegram bot.
        """
        chain = (
            RunnablePassthrough.assign(
                # Retrieve candlestick data (mocked for now)
                candlestick_data=RunnableLambda(lambda x: candle_retriever.invoke({
                    "ticker": self.ticker
                }))
            )
            | RunnablePassthrough.assign(
                # Save candles to CSV and pass the CSV path forward
                candle_csv_path=RunnableLambda(lambda x: save_candles_to_csv.invoke({
                    "candlestick": x["candlestick_data"]["candles"]
                }))
            )
            | RunnablePassthrough.assign(
                # Generate chart from the CSV path
                candle_chart_path=RunnableLambda(lambda x: format_candle_chart_from_csv.invoke({
                    "csv_path": x["candle_csv_path"]
                }))
            )
            | RunnablePassthrough.assign(
                # Detect patterns from the chart
                signal=RunnableLambda(lambda x: detect_pattern_from_chart.invoke({
                    "chart_path": x["candle_chart_path"]
                }))
            )
            | RunnableLambda(lambda x: notify_signal_sync.invoke({
                "signal": x["signal"]["trend"],
                "conf_score": x["signal"]["conf_score"],  # Placeholder confidence score
                "asset": self.ticker
            }))
        )
        return chain


    def run(self, market_status="open"):
        print(f"Running analysis for {self.ticker}...")
        
        self.chain.invoke({
            # "candlestick_data": MOCK_CANDLE
        })
