"""Generate and save a visual graph of the agent structure.

Starts the MCP server briefly to load real tool names, but does not
invoke the LLM or make any search/API calls.
Output saved to: log/agent_graph.png
"""

import sys
import os
import asyncio

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from config.models import get_gemini
from tools import base_tools
from prompts import prompts


async def main():
    # Load real MCP tools so the graph reflects actual tool names
    client = MultiServerMCPClient(
        {
            "airbnb": {
                "command": "npx",
                "args": ["-y", "@openbnb/mcp-server-airbnb", "--ignore-robots-txt"],
                "transport": "stdio",
            }
        }
    )
    mcp_tools = await client.get_tools()
    tools = mcp_tools + [base_tools.web_search, base_tools.get_weather]

    print(f"Loaded {len(tools)} tools: {[t.name for t in tools]}")

    model = get_gemini()
    agent = create_agent(model=model, tools=tools, system_prompt=prompts.AIRBNB_PROMPT)

    # Export graph as PNG via Mermaid.ink (requires internet, no local deps)
    output_path = os.path.join(root_dir, "log", "agent_graph.png")
    png = agent.get_graph().draw_mermaid_png()
    with open(output_path, "wb") as f:
        f.write(png)

    print(f"Graph saved to: {output_path}")


if __name__ == "__main__":
    asyncio.run(main())
