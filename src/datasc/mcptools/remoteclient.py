"""
LangGraph RemoteMCPClient integration with Linux FS Monitor MCP Server

This example shows how to use the MCP server with LangGraph's RemoteMCPClient
to build AI agents that can access file system and process monitoring tools.
"""

import asyncio
from typing import Annotated
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langchain_mcp import MCPClient
import httpx

# Configuration
MCP_SERVER_URL = "http://localhost:8000"  # Change to your server's URL


class LinuxMCPClient:
    """Wrapper for the Linux FS Monitor MCP Server."""

    def __init__(self, base_url: str = MCP_SERVER_URL):
        self.base_url = base_url.rstrip('/')
        self.client = httpx.AsyncClient(timeout=30.0)

    async def list_tools(self):
        """Get available tools from the MCP server."""
        response = await self.client.get(f"{self.base_url}/tools")
        response.raise_for_status()
        return response.json()["tools"]

    async def execute_tool(self, name: str, arguments: dict):
        """Execute a tool on the MCP server."""
        response = await self.client.post(
            f"{self.base_url}/tools/execute",
            json={"name": name, "arguments": arguments}
        )
        response.raise_for_status()
        return response.json()

    async def health_check(self):
        """Check if the MCP server is healthy."""
        try:
            response = await self.client.get(f"{self.base_url}/health")
            response.raise_for_status()
            return True
        except Exception:
            return False

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


# Create LangChain tools from MCP server
async def create_langchain_tools(mcp_client: LinuxMCPClient):
    """Dynamically create LangChain tools from MCP server tools."""

    tools_list = []
    mcp_tools = await mcp_client.list_tools()

    for mcp_tool in mcp_tools:
        tool_name = mcp_tool["name"]
        tool_description = mcp_tool["description"]

        # Create a closure to capture the tool name
        def make_tool_func(name):
            async def tool_func(**kwargs):
                """Dynamically generated tool function."""
                result = await mcp_client.execute_tool(name, kwargs)
                return result

            return tool_func

        # Create LangChain tool
        lc_tool = tool(
            name=tool_name,
            description=tool_description
        )(make_tool_func(tool_name))

        tools_list.append(lc_tool)

    return tools_list


async def example_simple_query():
    """Example: Simple query using the MCP server."""
    print("\n=== Example 1: Simple Query ===")

    mcp_client = LinuxMCPClient()

    # Check server health
    if not await mcp_client.health_check():
        print("Error: MCP server is not available")
        return

    # Get system stats
    stats = await mcp_client.execute_tool("get_system_stats", {})
    print(f"System Stats:\n{stats}\n")

    # List processes
    processes = await mcp_client.execute_tool("list_processes", {
        "sort_by": "memory",
        "limit": 5
    })
    print(f"Top 5 processes by memory:\n{processes}\n")

    await mcp_client.close()


async def example_langgraph_agent():
    """Example: LangGraph agent with MCP tools."""
    print("\n=== Example 2: LangGraph Agent ===")

    # Initialize MCP client
    mcp_client = LinuxMCPClient()

    # Check server health
    if not await mcp_client.health_check():
        print("Error: MCP server is not available")
        return

    # Create LangChain tools from MCP server
    tools = await create_langchain_tools(mcp_client)
    print(f"Loaded {len(tools)} tools from MCP server")

    # Initialize LLM
    llm = ChatAnthropic(
        model="claude-sonnet-4-20250514",
        temperature=0
    )

    # Create ReAct agent
    agent = create_react_agent(llm, tools)

    # Example queries
    queries = [
        "What are the top 3 processes using the most CPU?",
        "Check the disk usage for the root directory and tell me if we're running low on space",
        "List all Python files in the /tmp directory"
    ]

    for query in queries:
        print(f"\n--- Query: {query} ---")

        # Run the agent
        async for event in agent.astream(
                {"messages": [("user", query)]},
                stream_mode="values"
        ):
            # Get the last message
            last_message = event["messages"][-1]

            if hasattr(last_message, 'content'):
                print(f"Agent: {last_message.content}")

        print()

    await mcp_client.close()


async def example_with_mcp_package():
    """Example: Using langchain-mcp package (if available)."""
    print("\n=== Example 3: Using langchain-mcp MCPClient ===")

    try:
        from langchain_mcp import MCPClient

        # Note: MCPClient typically works with stdio transport
        # For HTTP transport, use the custom client above

        print("For HTTP transport, use the LinuxMCPClient wrapper shown above.")
        print("MCPClient from langchain-mcp is designed for stdio transport.")

    except ImportError:
        print("langchain-mcp not installed. Install with: pip install langchain-mcp")


async def example_file_analysis():
    """Example: Analyze files and processes together."""
    print("\n=== Example 4: File and Process Analysis ===")

    mcp_client = LinuxMCPClient()

    if not await mcp_client.health_check():
        print("Error: MCP server is not available")
        return

    # Create tools
    tools = await create_langchain_tools(mcp_client)

    # Initialize LLM
    llm = ChatAnthropic(
        model="claude-sonnet-4-20250514",
        temperature=0
    )

    # Create agent
    agent = create_react_agent(llm, tools)

    # Complex query
    query = """
    I need a system health report:
    1. Check current CPU and memory usage
    2. Find the top 5 processes by CPU usage
    3. Check disk usage for the root partition
    4. Summarize whether the system is healthy or if there are any concerns
    """

    print(f"Query: {query}\n")

    async for event in agent.astream(
            {"messages": [("user", query)]},
            stream_mode="values"
    ):
        last_message = event["messages"][-1]
        if hasattr(last_message, 'content'):
            print(f"Agent: {last_message.content}\n")

    await mcp_client.close()


async def main():
    """Run all examples."""
    print("=" * 60)
    print("LangGraph + Linux MCP Server Examples")
    print("=" * 60)
    print(f"\nMCP Server URL: {MCP_SERVER_URL}")
    print("\nMake sure your MCP server is running in HTTP mode:")
    print("  python linux_mcp_server.py --mode http\n")

    # Run examples
    await example_simple_query()
    await example_langgraph_agent()
    await example_with_mcp_package()
    await example_file_analysis()


if __name__ == "__main__":
    # Set your Anthropic API key
    # export ANTHROPIC_API_KEY='your-key-here'

    asyncio.run(main())