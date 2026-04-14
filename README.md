# Airbnb Hotel Search Agent with MCP

An agentic AI assistant that searches Airbnb listings, checks live weather, and answers travel questions — powered by Google Gemini, LangChain, and the Model Context Protocol (MCP).

## Features

- **Airbnb search** via the `@openbnb/mcp-server-airbnb` MCP server
- **Live weather** lookup using WeatherAPI.com
- **Web search** via Ollama Cloud Search
- **LangSmith tracing** for observability
- **Interactive chat mode** for follow-up questions after the initial search

## Project Structure

```
├── airbnb_mcp.py          # Main agent entry point
├── query.txt              # Initial query (edit to change the search)
├── config/
│   ├── models.py          # Gemini model factory
│   ├── utils.py           # MCP config loader
│   └── mcp_config.json    # MCP server definitions
├── tools/
│   └── base_tools.py      # Web search and weather tools
├── prompts/
│   └── prompts.py         # Agent system prompts
└── pyproject.toml
```

## Requirements

- Python 3.12+
- Node.js (for `npx` / MCP server)
- [uv](https://github.com/astral-sh/uv) package manager

## Setup

**1. Clone and install dependencies**
```bash
git clone <repo-url>
cd Airbnb_hotel_search_agent_with_MCP
uv sync
```

**2. Configure environment variables**

Copy the example and fill in your keys:
```bash
cp .env.example .env
```

| Variable | Description |
|---|---|
| `GOOGLE_API_KEY` | Gemini API key |
| `WEATHER_API_KEY` | WeatherAPI.com key |
| `OLLAMA_API_KEY` | Ollama Cloud key |
| `LANGSMITH_API_KEY` | LangSmith tracing key (optional) |
| `LANGSMITH_TRACING` | Set to `true` to enable tracing |

**3. Set your search query**

Edit `query.txt` with your search:
```
Show me 2 beachfront apartments in Bali for 5 nights from next Friday.
```

## Usage

```bash
uv run python airbnb_mcp.py
```

The agent runs the query from `query.txt` on startup, then enters interactive chat mode for follow-up questions. Type `q` or `quit` to exit.

### Sample Output

![Agent terminal output](log/Screenshot%202026-04-15%20020832.png)

## Observability

LangSmith tracing is enabled via environment variables. Each run logs the full agent trace — tool calls, inputs, outputs, token usage, and latency.

![LangSmith trace](log/Screenshot%202026-04-15%20020701.png)

## Switching Models

Edit `airbnb_mcp.py` to change the model:
```python
from config.models import get_gemini, GEMINI_PRO

model = get_gemini()                   # Gemini Flash (default, fast)
model = get_gemini(model=GEMINI_PRO)   # Gemini Pro (more capable)
model = get_gemini(thinking=True)      # Enable extended thinking
```
