#!/usr/bin/env python3
"""Entry point for the Python Cheatsheet MCP server.

Runs the MCP server over stdio, which is the transport required by
Claude Desktop and most MCP client integrations.

Usage:
    python run_mcp_server.py
"""

import sys
from pathlib import Path

# Ensure the repository root is on the Python path so that the `mcp`
# and `src` packages are importable when this script is run directly.
sys.path.insert(0, str(Path(__file__).parent))

from cheatsheet_mcp.server import mcp  # noqa: E402


def main() -> None:
    mcp.run(transport='stdio')


if __name__ == '__main__':
    main()
