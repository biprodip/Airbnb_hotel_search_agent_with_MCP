"""Airbnb hotel search agent using LangChain, Gemini, and MCP."""

import sys
import os

root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_dir)

from dotenv import load_dotenv

load_dotenv()

from langchain.agents import create_agent
from langchain.messages import HumanMessage

from config.models import get_gemini
from config.utils import load_mcp_config
from tools import base_tools
from prompts import prompts

from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
import logging

# Configure structured logging with timestamps
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

model = get_gemini()  # Gemini Flash, thinking disabled


async def hotel_search(agent, query):
    """Run a single query through the agent and print the response."""
    try:
        result = await agent.ainvoke({"messages": [HumanMessage(query)]})
        response = result["messages"][-1].text
        print("\n============== Output =============")
        print(response)
    except Exception as e:
        logger.error(f"Agent invocation failed: {e}")


async def ask(agent):
    """Interactive chat loop — keeps prompting until user quits."""
    logger.info("Chat mode started. Type 'q' or 'quit' to exit.")
    while True:
        print("\nAsk Another Question. Type 'q' or 'quit' to exit.")
        query = input("You: ").strip()

        if query.lower() in ["q", "quit"]:
            logger.info("Exiting chat mode.")
            break

        await hotel_search(agent, query)


async def main():
    """Initialise MCP client and agent once, then run initial query and chat loop."""
    client = MultiServerMCPClient(load_mcp_config("airbnb"))
    mcp_tools = await client.get_tools()
    tools = mcp_tools + [base_tools.web_search, base_tools.get_weather]
    logger.info(f"Loaded {len(tools)} tools")

    agent = create_agent(model=model, tools=tools, system_prompt=prompts.AIRBNB_PROMPT)

    # Run initial query from query.txt if present
    query_file = os.path.join(root_dir, "query.txt")
    if os.path.exists(query_file):
        with open(query_file, encoding="utf-8") as f:
            query = f.read().strip()
        logger.info("Query loaded from query.txt")
        await hotel_search(agent, query)
    else:
        logger.warning("query.txt not found, skipping initial search.")

    await ask(agent)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Interrupted by user.")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
