# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A ReAct (Reasoning + Acting) agent powered by Claude via LangGraph. The agent runs as an interactive CLI that can reason through problems, call tools (math, weather, web search), and stream responses in real-time.

## Commands

```bash
# Setup
python -m venv venv
.\venv\Scripts\activate          # Windows
pip install -r requirements.txt

# Run the interactive agent
python myagent.py

# Run tests
python test_server.py            # Math tool unit tests
python test_agent.py             # Agent integration test (requires API keys)
```

There is no linter, formatter, or test framework configured. Tests are standalone scripts.

## Required Environment Variables

Set in `.env` (never committed):
- `ANTHROPIC_API_KEY` (required) - Claude API access
- `TAVILY_API_KEY` (optional) - enables web search tool

## Architecture

Three-layer design: **agent -> tools -> server**

- **`myagent.py`** - Entry point. Creates a LangGraph `create_react_agent` with Claude Sonnet 4 as the LLM. Runs an interactive CLI loop that streams agent reasoning steps, tool calls, and final answers.

- **`tools.py`** - Defines the LangChain `@tool` functions the agent can call. Wraps the MCP math functions from `server.py`, adds a `get_weather` tool (Open-Meteo API, no key needed), and conditionally adds Tavily web search if the API key is present. Exports `TOOLS` list consumed by the agent.

- **`server.py`** - MCP (Model Context Protocol) server with `@mcp.tool()` decorated math functions (`add`, `subtract`, `multiply`, `divide`). Can run standalone as an MCP server (`python server.py`) or be imported directly by `tools.py`.

### Data flow

1. User input -> `myagent.py` wraps in `HumanMessage` -> LangGraph ReAct agent
2. Agent decides which tools to call (or responds directly)
3. Tool results feed back into agent for reasoning
4. Final `AIMessage` is streamed to the CLI

### Key pattern

`tools.py` imports math functions directly from `server.py` (not via MCP protocol). The MCP server decorators and LangChain `@tool` decorators coexist on the same functions - `server.py` functions have `@mcp.tool()` for MCP use, and `tools.py` re-wraps them with `@tool` for LangChain use.

## Windows Considerations

Both `myagent.py` and `test_agent.py` include `sys.stdout.reconfigure(encoding='utf-8')` for Windows console Unicode support. Maintain this pattern in any new entry points.
