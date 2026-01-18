from langchain_core.tools import tool
from mcp_client import SimpleMCPClient

mcp = SimpleMCPClient("http://localhost:3333", api_key="dev-secret")


@tool
def get_memory_info() -> dict:
    """Get system memory usage."""
    return mcp.call_tool("get_memory_info")


@tool
def get_storage_info() -> dict:
    """Get disk usage information."""
    return mcp.call_tool("get_storage_info")


@tool
def get_python_process_count() -> dict:
    """Get count of running Python processes."""
    return mcp.call_tool("get_python_process_count")
