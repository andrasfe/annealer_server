#!/usr/bin/env python3
"""
Startup script for the D-Wave MCP Server
"""
from mcp_server_dwave.server import main
import sys
import mcp
import os
import inspect

# Print available modules and functions in mcp
print("MCP package contents:")
print(dir(mcp))

# Create the server instance
server = main()

# Get the transport module path
transport_dir = os.path.dirname(inspect.getfile(mcp))
transport_path = os.path.join(transport_dir, "http_transport.py")
print(f"Looking for transport at: {transport_path}")

# Start the server
if os.path.exists(transport_path):
    print("Starting server with HTTP transport")
    # Try different methods to start the server
    try:
        if hasattr(mcp, 'run_server'):
            mcp.run_server(server, transport='http', port=3000)
        elif hasattr(mcp, 'server'):
            mcp.server.run_server(server, transport='http', port=3000)
        elif hasattr(mcp, 'serve'):
            mcp.serve.run(server, transport='http', port=3000)
        else:
            print("Could not find appropriate method to start server")
            sys.exit(1)
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)
else:
    print(f"Transport file not found: {transport_path}")
    sys.exit(1) 