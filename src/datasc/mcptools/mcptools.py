#!/usr/bin/env python3
import os
import shutil
import subprocess
from typing import List

from mcp.server import Server
from mcp.types import ToolResult, TextContent

server = Server("rhel-filesystem-tools")

# ---------------------------------------------------------
# Tool 1: List filesystems above usage threshold
# ---------------------------------------------------------

@server.tool(
    name="list_high_usage_filesystems",
    description="List mounted filesystems whose disk usage exceeds a given percentage",
    input_schema={
        "type": "object",
        "properties": {
            "threshold_pct": {
                "type": "number",
                "description": "Usage percentage threshold (default 50)",
                "default": 50
            }
        }
    }
)
def list_high_usage_filesystems(threshold_pct: float = 50) -> ToolResult:
    results = []

    # Use df -P for POSIX-safe output
    proc = subprocess.run(
        ["df", "-P"],
        capture_output=True,
        text=True,
        check=True
    )

    lines = proc.stdout.strip().splitlines()
    for line in lines[1:]:
        parts = line.split()
        if len(parts) < 6:
            continue

        filesystem, size, used, avail, pct, mountpoint = parts
        usage = int(pct.rstrip("%"))

        if usage > threshold_pct:
            results.append(
                f"{filesystem} mounted on {mountpoint} is {usage}% used"
            )

    if not results:
        results.append("No filesystems exceed the threshold")

    return ToolResult(
        content=[TextContent(text="\n".join(results))]
    )

# ---------------------------------------------------------
# Tool 2: Size of a specific log file
# ---------------------------------------------------------

@server.tool(
    name="get_log_file_size",
    description="Get size of a specific log file (in bytes)",
    input_schema={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Absolute path to log file (e.g. /var/log/messages)"
            }
        },
        "required": ["path"]
    }
)
def get_log_file_size(path: str) -> ToolResult:
    if not path.startswith("/var/log"):
        return ToolResult(
            content=[TextContent(text="Access denied: only /var/log files allowed")]
        )

    if not os.path.exists(path):
        return ToolResult(
            content=[TextContent(text=f"File does not exist: {path}")]
        )

    size_bytes = os.path.getsize(path)

    return ToolResult(
        content=[TextContent(
            text=f"File {path} size: {size_bytes} bytes"
        )]
    )

# ---------------------------------------------------------
# Run over STDIO (MCP v2)
# ---------------------------------------------------------

if __name__ == "__main__":
    server.run_stdio()
