from langchain.chains.base import Chain
from langchain.prompts import PromptTemplate


class TradingAnalysisChain(Chain):
    input_keys = ["ticker", "market_status", "candle_text"]
    output_keys = ["signal", "analysis"]

    def __init__(self, llm, retriever, prompt_template: PromptTemplate):
        super().__init__()
        self.llm = llm
        self.retriever = retriever
        self.prompt_template = prompt_template

    def _call(self, inputs: dict) -> dict:
        ticker = inputs["ticker"]
        market_status = inputs["market_status"]
        candle_text = inputs["candle_text"]

        retrieved_docs = self.retriever.get_relevant_documents(candle_text)
        retrieved_text = "\n\n".join(
            f"---\n{doc.page_content}" for doc in retrieved_docs
        )

        prompt = self.prompt_template.format(
            ticker=ticker,
            market_status=market_status,
            candle_data=candle_text,
            retrieved_docs=retrieved_text,
        )

        raw_answer = self.llm.predict(prompt)
        normalized = raw_answer.strip().lower()
        if "buy" in normalized:
            signal = "buy"
        elif "sell" in normalized:
            signal = "sell"
        else:
            signal = "hold"

        return {"signal": signal, "analysis": raw_answer}


class TradingAgent:
    def __init__(self, ticker, llm, retriever):
        self.ticker = ticker
        self.chain = self.build_chain(llm, retriever)

    def build_chain(self, llm, retriever):
        """
        Build a custom LangChain chain for trading analysis.

        This chain:
        1. Formats ticker + candle data into a prompt
        2. Retrieves relevant historical documents
        3. Sends the combined context to an LLM
        4. Parses the output into a trading signal
        """
        prompt_template = PromptTemplate(
            input_variables=["ticker", "market_status", "candle_data", "retrieved_docs"],
            template=(
                "You are a trading analyst for {ticker}.\n"
                "Market status: {market_status}\n\n"
                "Recent candle and volume data:\n{candle_data}\n\n"
                "Relevant historical patterns:\n{retrieved_docs}\n\n"
                "Based on the data and patterns, return a decision: BUY, SELL, or HOLD. "
                "Provide a short rationale."
            ),
        )

        return TradingAnalysisChain(
            llm=llm,
            retriever=retriever,
            prompt_template=prompt_template,
        )

    def run(self, candle_text, market_status="open"):
        print(f"Running analysis for {self.ticker}...")
        result = self.chain.invoke(
            {
                "ticker": self.ticker,
                "market_status": market_status,
                "candle_text": candle_text,
            }
        )
        print("Signal:", result["signal"])
        print("Analysis:\n", result["analysis"])
        return result
