from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from tools import (
    get_memory_info,
    get_storage_info,
    get_python_process_count,
)

llm = ChatOpenAI(model="gpt-4.1-mini")

tools = [
    get_memory_info,
    get_storage_info,
    get_python_process_count,
]

llm_with_tools = llm.bind_tools(tools)


def agent_node(state):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


graph = StateGraph(dict)
graph.add_node("agent", agent_node)
graph.set_entry_point("agent")
graph.add_edge("agent", END)

app = graph.compile()
