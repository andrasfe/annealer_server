#!/usr/bin/env python3
import asyncio
import json
import time # Keep for potential delays if needed, though MCPClient might handle waits

from mcp import ClientSession # ClientSession is directly available
from mcp.client.streamable_http import streamablehttp_client # Correct import
# from mcp.types import HttpUrl # Removed as it's not found; URL is likely a string

# The URL for the MCP server run by FastAPI in Docker
# streamablehttp_client expects the full URL.
MCP_SERVER_URL = "http://localhost:3001/mcp/"

def print_exception_group(ex_group, indent=0):
    """Recursively prints exceptions from an ExceptionGroup."""
    if not hasattr(ex_group, 'exceptions') or not isinstance(ex_group.exceptions, (list, tuple)):
        return
    
    prefix = "  " * indent
    print(f"{prefix}Contained exceptions in {type(ex_group).__name__}: {ex_group.message if hasattr(ex_group, 'message') else str(ex_group)}")
    for i, sub_ex in enumerate(ex_group.exceptions):
        print(f"{prefix}  Sub-exception {i+1}: {type(sub_ex).__name__}: {sub_ex}")
        if hasattr(sub_ex, 'exceptions'): # Check if sub_ex is also an ExceptionGroup
            print_exception_group(sub_ex, indent + 2)

async def test_dockerized_mcp_server():
    """Test client for dockerized MCP server using mcp.client.streamable_http."""
    print("Docker MCP Test Client (using mcp.client.streamable_http)")
    print("-----------------------------------------------------------")

    try:
        print(f"Attempting to connect to MCP server at {MCP_SERVER_URL}...")
        async with streamablehttp_client(url=MCP_SERVER_URL) as (read_stream, write_stream, _http_client_instance):
            print("HTTP transport connected. Creating MCP ClientSession...")
            async with ClientSession(read_stream, write_stream) as session:
                print("MCP ClientSession created. Attempting to initialize session...")
                init_payload = await session.initialize()
                print(f"MCP Initialize successful. Response: {init_payload}")

                print("Attempting to list tools...")
                tools_response = await session.list_tools()
                tools = tools_response.tools
                
                if not tools:
                    print("No tools found on the server.")
                    return

                print(f"Successfully received {len(tools)} tools:")
                for tool_obj in tools:
                    print(f"  - {tool_obj.name}: {tool_obj.description}")

                # Test the get_simulator_status tool
                print("\nTesting get_simulator_status tool...")
                call_tool_response = await session.call_tool(name="get_simulator_status", arguments={})
                result_text = call_tool_response.content[0].text
                result = json.loads(result_text)
                print(f"Result: {json.dumps(result, indent=2)}")

                # Test the create_qubo tool
                print("\nTesting create_qubo tool...")
                qubo_args = {
                    "Q": {"0,0": -1, "1,1": -1, "0,1": 2},
                    "description": "Simple QUBO example via mcp.client"
                }
                call_tool_response = await session.call_tool(name="create_qubo", arguments=qubo_args)
                result_text = call_tool_response.content[0].text
                result = json.loads(result_text)
                print(f"Result: {json.dumps(result, indent=2)}")

                problem_id = result.get("problem_id")

                if problem_id:
                    print(f"\nTesting solve_problem tool with problem_id {problem_id}...")
                    solve_args = {"problem_id": problem_id}
                    call_tool_response = await session.call_tool(name="solve_problem", arguments=solve_args)
                    result_text = call_tool_response.content[0].text
                    result = json.loads(result_text)
                    print(f"Result: {json.dumps(result, indent=2)}")
                else:
                    print("Skipping solve_problem tool as problem_id was not retrieved.")

                print("\nTest completed successfully!")

    except ImportError:
        # This is to catch potential issues if anyio is not installed, though it should be a dep of httpx/mcp.
        print("Error: 'anyio' library might be missing or related import failed. Please ensure it is installed.") 
        raise
    except Exception as e:
        print(f"Error during test: {type(e).__name__}: {e}")
        if hasattr(e, 'exceptions'): # Check if it's an ExceptionGroup
            print("--- Detailed Exception Group Trace ---")
            print_exception_group(e)
            print("------------------------------------")
        else:
            import traceback
            traceback.print_exc() # For any other unexpected errors
    # Context managers will handle cleanup.

if __name__ == "__main__":
    asyncio.run(test_dockerized_mcp_server()) 