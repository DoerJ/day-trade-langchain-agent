import time
from src.configs import TICKER, AGENT_LOOP_SECONDS
from src.agent.trading_agent import TradingAgent

def main():
    print(f"Starting trading agent for {TICKER}")
    # Initialize the trading agent with the specified ticker
    agent = TradingAgent(ticker=TICKER)

    agent.run()

    # while True:
    #     try:
    #         print(f"\n=== Agent Loop Start: {time.ctime()} ===")
    #         agent.run()
    #     except Exception as e:
    #         print(f"Error during analysis: {e}")

    #     time.sleep(AGENT_LOOP_SECONDS)

if __name__ == "__main__":
    main()