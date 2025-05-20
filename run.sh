#!/bin/bash

# Check if DWAVE_API_TOKEN is set
if [ -z "$DWAVE_API_TOKEN" ]; then
  echo "Warning: DWAVE_API_TOKEN environment variable is not set."
  echo "You can set it with: export DWAVE_API_TOKEN=your-token-here"
  echo "Alternatively, ensure you have a valid ~/.dwrc file with your token."
  echo ""
fi

# Run the MCP server
python -m mcp serve src/mcp_server_dwave/server.py "$@" 