from langgraph.prebuilt import ToolNode
from langchain_core.tools import BaseTool
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import ToolMessage
from typing import  Sequence

def handle_error(state):
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls

    return {
        "messages": [
            ToolMessage(content=f"Error: {repr(error)} please fix your mistakes.", tool_calls=tool_call["id"])
        ]
        for tool_call in tool_calls
    }

def tools_node_with_fallback(tools: Sequence[BaseTool]):
    return ToolNode(tools=tools).with_fallbacks([RunnableLambda(handle_error)], exception_key="error")