#!/usr/bin/env python3
import sys
print(f"--- sys.path START ---\n{sys.path}\n--- sys.path END ---")

print("--- PIP FREEZE START ---")
import subprocess
subprocess.run(["pip", "freeze"])
print("--- PIP FREEZE END ---")

from fastapi import FastAPI
import uvicorn
import inspect
import json
from typing import Dict, Any, List
import contextlib # Added for lifespan management

from mcp.server.fastmcp import FastMCP
from mcp_server_dwave.server import ServerConfig, main as create_dwave_logic_server

# This is the actual DWave server logic instance
dwave_logic = create_dwave_logic_server(ServerConfig(use_simulator=True))

# This is the MCP server that will expose the DWave logic
mcp_server_app = FastMCP(
    name="DWaveMCPAdapter",
    description="D-Wave Hybrid Computing Server via MCP",
    version="0.1.0"
)

# --- Define tools for MCP, wrapping calls to dwave_logic ---

# Helper to call dwave_logic methods (sync or async)
async def _call_dwave_method(method_name: str, *args, **kwargs) -> Any:
    method = getattr(dwave_logic, method_name)
    if inspect.iscoroutinefunction(method):
        return await method(*args, **kwargs)
    else:
        # Consider running sync methods in a thread pool if they are blocking
        # For now, direct call for simplicity, assuming non-blocking or short operations
        return method(*args, **kwargs)

@mcp_server_app.tool()
async def get_simulator_status() -> Dict[str, Any]:
    """Get the current status of the D-Wave simulator."""
    return await _call_dwave_method("get_simulator_status")

@mcp_server_app.tool()
async def create_qubo(Q: Dict[str, float], description: str = "QUBO problem") -> Dict[str, Any]:
    """Create a QUBO problem. Q should be a dict like {'0,0': -1, '1,1': -1, '0,1': 2}."""
    return await _call_dwave_method("create_qubo", Q=Q, description=description)

@mcp_server_app.tool()
async def solve_problem(problem_id: str, num_reads: int = 100, annealing_time: int = 20) -> Dict[str, Any]:
    """Solve a problem previously created (QUBO or Ising) identified by its problem_id."""
    # Note: Added num_reads and annealing_time as common parameters for D-Wave solvers.
    # Adjust these or add more based on the actual signature of dwave_logic.solve_problem
    # and what you want to expose via MCP.
    # Ensure the types (int, float, str, etc.) match the dwave_logic method.
    return await _call_dwave_method("solve_problem", problem_id=problem_id, num_reads=num_reads, annealing_time=annealing_time)

# TODO: Add other DWaveServer methods as MCP tools here. Examples:
# @mcp_server_app.tool()
# async def set_simulator_config(some_config_param: str) -> Dict[str, Any]:
#     """Set simulator configuration."""
#     return await _call_dwave_method("set_simulator_config", some_config_param=some_config_param)
#
# @mcp_server_app.tool()
# async def create_ising(linear: Dict[Any, float], quadratic: Dict[Any, float], description: str = "Ising problem") -> Dict[str, Any]:
#     """Create an Ising problem."""
#     return await _call_dwave_method("create_ising", linear=linear, quadratic=quadratic, description=description)
#
# @mcp_server_app.tool()
# async def get_result(problem_id: str) -> Dict[str, Any]:
#     """Get the results for a solved problem."""
#     return await _call_dwave_method("get_result", problem_id=problem_id)

# Lifespan manager for FastMCP session
@contextlib.asynccontextmanager
async def mcp_lifespan(app: FastAPI):
    print("MCP Lifespan: Starting FastMCP session manager...")
    async with mcp_server_app.session_manager.run():
        print("MCP Lifespan: FastMCP session manager started.")
        yield
    print("MCP Lifespan: FastMCP session manager stopped.")

# Create FastAPI app, using the custom lifespan
app = FastAPI(lifespan=mcp_lifespan)

# Mount the MCP application at /
# This will handle /mcp/initialize, /mcp/request, /mcp/stream etc. if the app itself serves these paths
app.mount("/", mcp_server_app.streamable_http_app())

# Optional: Health check or root path
@app.get("/")
async def root():
    return {"message": "DWave MCP Server is running. MCP endpoint at /mcp"}

if __name__ == "__main__":
    # It is crucial that uvicorn runs the 'app' object from this script
    uvicorn.run("api_server:app", host="0.0.0.0", port=3000, reload=False) 