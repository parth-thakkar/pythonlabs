from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage

# Define the state of the graph
class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]

# Define the graph
graph_builder = StateGraph(State)

# Initialize the LLM
# Note: Ensure OPENAI_API_KEY is set in the environment
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Define the chatbot node
def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

# Add nodes
graph_builder.add_node("chatbot", chatbot)

# Add edges
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# Compile the graph
graph = graph_builder.compile()
