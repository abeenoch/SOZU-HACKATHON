from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.tavily import TavilyTools
from phi.tools.crawl4ai_tools import Crawl4aiTools
from phi.tools import Toolkit
from phi.workflow import Workflow, RunResponse, RunEvent
from phi.storage.workflow.sqlite import SqlWorkflowStorage
from phi.utils.log import logger
from pydantic import PrivateAttr
from typing import Iterator, List, Dict
import os
from dotenv import load_dotenv
from web3 import Web3
from multiprocessing import Queue


# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
PHI_API_KEY = os.getenv("PHI_API_KEY")
WEB3_PROVIDER_URL = os.getenv("WEB3_PROVIDER_URL")

class Web3Tools(Toolkit):
    _web3: Web3 = PrivateAttr()

    def __init__(self, provider_url: str):
        super().__init__(name="web3_tools")
        self._web3 = Web3(Web3.HTTPProvider(provider_url))
        self.register(self.get_balance)
        self.register(self.get_transaction)
        self.register(self.get_block)
        self.register(self.get_latest_block_number)  # Register the new function

    def get_balance(self, address: str) -> str:
        """
        Get the balance of an Ethereum address.
        """
        if not self._web3.is_address(address):
            return "Invalid Ethereum address."
        balance = self._web3.eth.get_balance(address)
        return f"Balance of {address}: {self._web3.from_wei(balance, 'ether')} ETH"

    def get_transaction(self, tx_hash: str) -> str:
        """
        Get details of a transaction by its hash.
        """
        try:
            tx = self._web3.eth.get_transaction(tx_hash)
            return f"Transaction Details:\n{tx}"
        except:
            return "Transaction not found or invalid hash."

    def get_block(self, block_identifier: str) -> str:
        """
        Get details of a block by its number or hash.
        """
        try:
            block = self._web3.eth.get_block(block_identifier)
            return f"Block Details:\n{block}"
        except:
            return "Block not found or invalid identifier."

    def get_latest_block_number(self) -> str:
        """
        Get the latest block number on the Ethereum network.
        """
        try:
            latest_block_number = self._web3.eth.block_number
            return f"Latest Ethereum block number: {latest_block_number}"
        except Exception as e:
            return f"Error fetching latest block number: {e}"


class MantleAgentWorkflow(Workflow):
    _agent: Agent = PrivateAttr()
    _conversation_history: List[Dict[str, str]] = PrivateAttr(default_factory=list)

    def __init__(self, **data):
        super().__init__(**data)
        self._agent = Agent(
            model=OpenAIChat(id="gpt-4o"),
            tools=[
                TavilyTools(),
                Crawl4aiTools(max_length=None),
                Web3Tools(WEB3_PROVIDER_URL)
            ],
            description="Specialist AI AGENT for 'Mantle Ecosystem' technical questions",
            instructions=[
                "You are a Mantle Ecosystem expert. Respond ONLY to Mantle-related questions.",
                "For a given query, search for the top 3 links.",
                "Then read each URL and scrape them for information; if a URL isn't available, ignore it.",
                "Analyze gathered information and prepare a comprehensive reply.",
                'For technical questions, reference official docs ',
                "Always include relevant code samples from Mantle's GitHub",
                "Reject non-Mantle questions politely but firmly",
                "For blockchain-related queries, use Web3Tools to fetch on-chain data.",
                "For general queries like 'what was the last question?', provide context-aware answers without violating the Mantle-focus.",

            ],
            markdown=True,
            show_tool_calls=True,
            add_datetime_to_instructions=True,
        )

    def run(self, query: str, use_cache: bool = True) -> Iterator[RunResponse]:
        logger.info(f"Processing query: {query}")

        if use_cache and "responses" in self.session_state:
            logger.info("Checking for cached response.")
            for cached in self.session_state["responses"]:
                if cached["query"] == query:
                    logger.info("Found cached response.")
                    yield RunResponse(content=cached["response"], event=RunEvent.workflow_completed)
                    return

        conversation_context = "\n".join(
            [f"User: {entry['query']}\nAgent: {entry['response']}" for entry in self._conversation_history]
        )
        extended_query = f"{conversation_context}\nUser: {query}\nAgent:" if conversation_context else query

        response = self._agent.run(extended_query)

        self._conversation_history.append({"query": query, "response": response.content})

        if "responses" not in self.session_state:
            self.session_state["responses"] = []
        self.session_state["responses"].append({"query": query, "response": response.content})

        yield RunResponse(content=response.content, event=RunEvent.workflow_completed)
