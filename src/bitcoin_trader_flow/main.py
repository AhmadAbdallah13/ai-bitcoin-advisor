import os

from crewai import LLM
from crewai.flow.flow import Flow, start
from dotenv import load_dotenv
from pydantic import BaseModel

from bitcoin_trader_flow.crews.tracker_crew.tracker_crew import BitcoinTradingCrew

load_dotenv()

LLM_KEY = os.getenv("LLM_KEY")


class TradingDecision(BaseModel):
    trading_decision: str = ""


class BitcoinTrackAndInformFlow(Flow[TradingDecision]):
    """Flow for tracking and making an informed decision about buying/selling/holding bitcoin"""

    def __init__(self, persistence=None, **kwargs):
        super().__init__(persistence, **kwargs)
        # Initialize the LLM
        self.llm = LLM(
            model="ollama/qwen2.5:latest",
            base_url="http://localhost:11434",
            api_key="ollama",  # dummy value
            # temperature=0.1,
        )

    @start()
    def get_trading_decision(self):
        print("Fetching and archiving Bitcoin price...")

        # Run the content crew for this section
        result = (
            BitcoinTradingCrew(llm=self.llm)
            .crew()
            .kickoff(
                inputs={
                    "COINGECKO_API_URL": "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
                    "NEWS_SOURCES": ["https://cointelegraph.com", "https://decrypt.co"],
                    "CURRENT_YEAR": 2025,
                    "PRICES_ARCHIVE_PATH": "output/prices_archive.json",
                    "NEWS_ARCHIVE_PATH": "output/news_archive.txt",
                    "TRADING_DECISION_ARCHIVE_PATH": "output/trading_decision.json",
                }
            )
        )

        decision = result.json_dict

        print("Decision made, goodbye.")

        return decision


def kickoff():
    """Run the Bitcoin tracking and decision-making flow"""
    return BitcoinTrackAndInformFlow().kickoff()


if __name__ == "__main__":
    kickoff()
