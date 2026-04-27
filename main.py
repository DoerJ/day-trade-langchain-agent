import time
from configs import TICKER, AGENT_LOOP_SECONDS

# from agent.trading_agent import TradingAgent

def main():
    print(f"Starting trading agent for {TICKER}")
    # agent = TradingAgent(ticker=TICKER)

    while True:
        try:
            print(f"\n=== Agent Loop Start: {time.ctime()} ===")
        except Exception as e:
            print(f"Error during analysis: {e}")

        time.sleep(AGENT_LOOP_SECONDS)

if __name__ == "__main__":
    main()