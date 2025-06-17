# src/guide_creator_flow/crews/content_crew/content_crew.py
from crewai import Agent, Crew, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import ScrapeWebsiteTool

from pydantic import BaseModel, Field
from datetime import datetime

class PriceEntry(BaseModel):
    timestamp: str = Field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    price_usd: float

class NewsEntry(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    title: str
    summary: str
    sentiment: str

class TradingDecision(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    trading_decision: str = Field(default="", description="The trading decision made by the agent, e.g., 'buy', 'sell', or 'hold'.")
    rationale: str = Field(default="", description="The reasoning behind the trading decision, including analysis of price trends and news sentiment.")


# Instantiate tools
scrape_website_tool = ScrapeWebsiteTool()

@CrewBase
class BitcoinTradingCrew():
    """Bitcoin tracker and trading decision making crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self, llm):
        self.llm = llm

    @agent
    def price_monitor(self) -> Agent:
        return Agent(
            config=self.agents_config['price_monitor'],
            tools=[scrape_website_tool],
            verbose=True,
            llm=self.llm,
            reasoning=True,
        )

    @agent
    def news_monitor(self) -> Agent:
        return Agent(
            config=self.agents_config['news_monitor'],
            tools=[scrape_website_tool],
            verbose=True,
            llm=self.llm,
            reasoning=True,
        )
    
    @agent
    def decision(self) -> Agent:
        return Agent(
            config=self.agents_config['decision'],
            verbose=True,
            llm=self.llm,
            reasoning=True,
        )

    @task
    def fetchـandـarchiveـpriceـtask(self) -> Task:
        return Task(
            config=self.tasks_config['fetchـandـarchiveـpriceـtask'],
            output_file="output/prices_archive.json",
            output_json=PriceEntry,
        )

    @task
    def scrape_crypto_news_task(self) -> Task:
        return Task(
            config=self.tasks_config['scrape_crypto_news_task'],
            output_file="output/news_archive.txt",
            # output_json=NewsEntry,
        )
    
    @task
    def analyze_and_recommend_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_and_recommend_task'],
            output_json=TradingDecision,
            # output_file="output/trading_decision.json"
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
        )