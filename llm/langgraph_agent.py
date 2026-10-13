"""TEMPLATE: LangGraph tool-calling agent with memory.

Shape: State -> nodes (llm, tools) -> edges (llm -> tools if tool call, else finish) -> compile(checkpointer)
Run:  python langgraph_agent.py   (needs OPENAI_API_KEY)
"""
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()


# 1. State: what flows between nodes. add_messages = append, don't overwrite.
class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# 2. Tools: the docstring + type hints become the tool schema the LLM sees.
@tool
def get_order_status(order_id: str) -> str:
    """Look up the shipping status of an order by its ID."""
    fake_db = {"A1": "shipped", "B2": "processing"}
    return fake_db.get(order_id, "not found")


tools = [get_order_status]
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools(tools)


# 3. Nodes: functions that take state and return an update.
def call_llm(state: State) -> dict:
    return {"messages": [llm.invoke(state["messages"])]}


# 4. Graph: wire nodes and edges.
graph = StateGraph(State)
graph.add_node("llm", call_llm)
graph.add_node("tools", ToolNode(tools))         # runs whatever tool the LLM asked for
graph.add_edge(START, "llm")
graph.add_conditional_edges("llm", tools_condition)  # tool call -> "tools", else -> END
graph.add_edge("tools", "llm")                   # feed tool result back to the LLM

# 5. Compile with a checkpointer = conversation memory per thread_id.
app = graph.compile(checkpointer=MemorySaver())

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "user-1"}}
    for q in ["Where is my order A1?", "And what was the order ID I asked about?"]:
        out = app.invoke({"messages": [HumanMessage(q)]}, config)
        print(">", q, "\n", out["messages"][-1].content)
