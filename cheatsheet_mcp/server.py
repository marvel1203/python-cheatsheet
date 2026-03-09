"""MCP Server for the Python Cheatsheet.

Exposes 5 tools for querying the Python cheatsheet content via the
Model Context Protocol (MCP), enabling direct integration with Claude
Desktop and other MCP-compatible clients.

Usage (stdio transport):
    python run_mcp_server.py

Usage (HTTP transport, for testing):
    python -m mcp.server --transport http
"""

from mcp.server.fastmcp import FastMCP

from .tools import (
    explain_concept,
    get_code_example,
    list_topics,
    search_best_practices,
    search_python_concept,
)

# Create the FastMCP server instance
mcp = FastMCP(
    name="python-cheatsheet",
    instructions=(
        "A comprehensive Python cheatsheet server. "
        "Use the available tools to search Python concepts, retrieve code examples, "
        "get detailed explanations, look up best practices, and list all topics covered."
    ),
)

# Register the 5 tools
mcp.tool()(search_python_concept)
mcp.tool()(get_code_example)
mcp.tool()(explain_concept)
mcp.tool()(search_best_practices)
mcp.tool()(list_topics)
