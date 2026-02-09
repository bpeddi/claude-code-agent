"""Test the agent with a search query."""
import os
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

from dotenv import load_dotenv
load_dotenv()

from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from tools import TOOLS

print("Available tools:", [t.name for t in TOOLS])

llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    temperature=0,
    max_tokens=4096,
)

agent = create_react_agent(llm, TOOLS)

# Test query
query = "search for NFL superbowl news"
print(f"\nQuery: {query}\n")
print("-" * 60)

for chunk in agent.stream(
    {"messages": [HumanMessage(content=query)]},
    stream_mode="values"
):
    if "messages" in chunk:
        msg = chunk["messages"][-1]
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            print(f"[Agent] Calling tool:")
            for tc in msg.tool_calls:
                print(f"  -> {tc['name']}({tc['args']})")
        elif isinstance(msg, ToolMessage):
            print(f"[Tool Response]: {msg.content[:200]}...")
        elif isinstance(msg, AIMessage) and msg.content and not getattr(msg, 'tool_calls', None):
            print(f"[Final Answer]: {msg.content[:500]}")
