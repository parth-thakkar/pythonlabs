from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import psutil
import shutil

from mcp.server import Server
from mcp.server.models import Tool
from mcp.types import (
    InitializeRequest,
    InitializeResult,
    ToolsListRequest,
    ToolsListResult,
    ToolsCallRequest,
    ToolsCallResult,
)

app = FastAPI()
mcp_server = Server(name="system-metrics-mcp")


# -------------------
# MCP: initialize
# -------------------
@app.post("/initialize")
async def initialize(req: InitializeRequest):
    return InitializeResult(
        protocolVersion="2024-11-05",
        serverInfo={"name": "system-metrics-mcp", "version": "1.0.0"},
        capabilities={"tools": {}},
    )


# -------------------
# Tools
# -------------------

def get_memory_info():
    mem = psutil.virtual_memory()
    return {
        "total_bytes": mem.total,
        "available_bytes": mem.available,
        "used_bytes": mem.used,
        "percent_used": mem.percent,
    }


def get_storage_info():
    total, used, free = shutil.disk_usage("/")
    return {
        "total_bytes": total,
        "used_bytes": used,
        "free_bytes": free,
        "percent_used": round((used / total) * 100, 2),
    }


def get_python_process_count():
    count = 0
    for proc in psutil.process_iter(attrs=["name"]):
        if proc.info["name"] and "python" in proc.info["name"].lower():
            count += 1
    return {"python_process_count": count}


TOOLS = {
    "get_memory_info": get_memory_info,
    "get_storage_info": get_storage_info,
    "get_python_process_count": get_python_process_count,
}


# -------------------
# MCP: tools/list
# -------------------
@app.post("/tools/list")
async def tools_list(_: ToolsListRequest):
    return ToolsListResult(
        tools=[
            Tool(
                name="get_memory_info",
                description="Get system RAM usage",
                inputSchema={},
            ),
            Tool(
                name="get_storage_info",
                description="Get disk usage",
                inputSchema={},
            ),
            Tool(
                name="get_python_process_count",
                description="Count running Python processes",
                inputSchema={},
            ),
        ]
    )


# -------------------
# MCP: tools/call
# -------------------
@app.post("/tools/call")
async def tools_call(req: ToolsCallRequest):
    tool_fn = TOOLS.get(req.name)
    if not tool_fn:
        return JSONResponse(
            status_code=404,
            content={"error": f"Unknown tool {req.name}"},
        )

    result = tool_fn()
    return ToolsCallResult(content=result)


# -------------------
# Run
# -------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3333)
