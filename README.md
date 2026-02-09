# Claude Code Agent

A ReAct (Reasoning + Acting) agent powered by Claude, built with [LangGraph](https://github.com/langchain-ai/langgraph) and the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/). The agent runs as an interactive CLI that reasons through problems, calls tools, and streams responses in real-time.

## Features

- **ReAct pattern** - LLM decides when to call tools vs respond directly
- **Streaming output** - See tool calls, intermediate reasoning, and final answers as they happen
- **Math tools** - Basic arithmetic via an MCP server (add, subtract, multiply, divide)
- **Weather** - Current conditions for any location using Open-Meteo (no API key needed)
- **Web search** - Tavily-powered search for current events (optional, requires API key)

## Quick Start

### Prerequisites

- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com/)

### Setup

```bash
# Clone the repo
git clone https://github.com/bpeddi/claude-code-agent.git
cd claude-code-agent

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate        # Windows
source venv/bin/activate       # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env           # or create .env manually
```

Add your API keys to `.env`:

```
ANTHROPIC_API_KEY=your-key-here
TAVILY_API_KEY=your-key-here   # optional, enables web search
```

### Run

```bash
python myagent.py
```

You'll see the agent graph structure printed, then an interactive prompt:

```
[READY] Claude ReAct Agent with Streaming
============================================================

[Chat] Interactive Agent Chat
Type 'exit' or 'quit' to end the conversation

[You]: What's the weather in Tokyo?
```

## Project Structure

```
├── myagent.py          # Entry point - interactive agent loop with streaming
├── tools.py            # LangChain tool definitions (math, weather, search)
├── server.py           # MCP math server (can run standalone or be imported)
├── test_agent.py       # Agent integration test
├── test_server.py      # Math tools unit test
├── requirements.txt    # Python dependencies
└── .env                # API keys (not committed)
```

## How It Works

1. `myagent.py` creates a LangGraph ReAct agent with Claude Sonnet 4 and the tools from `tools.py`
2. User input is wrapped in a `HumanMessage` and streamed through the agent
3. The agent reasons about which tools to call (if any), executes them, and formulates a response
4. `tools.py` wraps the MCP math functions from `server.py` as LangChain `@tool` functions, alongside the weather and search tools
5. All intermediate steps (tool calls, tool results, final answer) are streamed to the console

## Running Tests

```bash
python test_server.py    # Verify math tools work (no API key needed)
python test_agent.py     # End-to-end agent test (requires ANTHROPIC_API_KEY)
```

## Running the MCP Server Standalone

`server.py` can also run as a standalone MCP server:

```bash
python server.py
```

This exposes the math tools over the MCP protocol for use with any MCP-compatible client.
