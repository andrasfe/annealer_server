# D-Wave MCP Server (`mcp_server_dwave`)

This project provides an MCP (Model Context Protocol) server for interacting with D-Wave's quantum computing capabilities, primarily using a simulator. It allows you to create and solve QUBO (Quadratic Unconstrained Binary Optimization) problems.

The server is designed to be run within a Docker container and exposes its functionality via an MCP-compliant API built with FastAPI.

## Original Package Features (Direct Usage - Pre-Docker/MCP)

The underlying Python package `mcp_server_dwave` (which this MCP server wraps) was originally designed for direct library use and had features such as:

- Creating and solving QUBO and Ising model problems.
- Visualizing problem structures and results.
- Listing available D-Wave solvers and their properties.
- Configurable annealing time limits.
- Automatic embedding handling.

Much of this direct usage information has been preserved below for context, but the primary way to use this project now is via the Dockerized MCP server.

## Running with Docker and MCP (FastAPI)

This is the recommended way to run and interact with the D-Wave MCP server.

### Prerequisites

- Docker installed and running.
- Python 3.10+ (for the test client).

### 1. Build the Docker Image

From the root of the `servers` workspace (i.e., the directory containing `src/dwave/...`):

```bash
docker build -t dwave-mcp-server:latest -f src/dwave/Dockerfile .
```

### 2. Run the Docker Container

This command will start the server and expose its port `3000` (inside the container) to port `3001` on your host machine. The MCP endpoint will be available at `http://localhost:3001/mcp/`.

```bash
# Ensure no other container is using the name "dwave_mcp_server_run" or port 3001
# docker stop dwave_mcp_server_run && docker rm dwave_mcp_server_run || true

docker run -d -p 3001:3000 --name dwave_mcp_server_run dwave-mcp-server:latest
```
You can view server logs with:
```bash
docker logs dwave_mcp_server_run
```

### 3. Run the Test Client

A Python test client, `docker_test_client.py`, is provided in the root of the `servers` workspace. This script uses the `mcp` library to connect to the Dockerized server, list available tools, and run a sequence of operations.

Ensure you have the necessary Python packages for the client (primarily `mcp` and its dependencies like `httpx`, `anyio`):
```bash
# If you have a virtual environment for the 'servers' project, activate it
# pip install "mcp>=1.9.0" httpx anyio
```

Then run the client:
```bash
python docker_test_client.py
```
The client will output the steps it takes and the results from the server. If successful, it will end with "Test completed successfully!".

### Exposed MCP Tools

The server currently exposes the following tools via MCP:

- `get_simulator_status`: Get the current status of the D-Wave simulator.
- `create_qubo`: Create a QUBO problem.
  - Arguments: `Q` (Dict[str, float]), `description` (str, optional)
- `solve_problem`: Solve a problem previously created.
  - Arguments: `problem_id` (str), `num_reads` (int, optional, default 100), `annealing_time` (int, optional, default 20)

---

## Legacy Information: Original `mcp_server_dwave` Package Details

The following sections detail the original design and usage of the `mcp_server_dwave` Python package before it was primarily wrapped by the Dockerized FastAPI/MCP server.

### Original Prerequisites

- Python 3.10 or higher
- D-Wave Ocean SDK
- A D-Wave Leap account (for accessing real quantum hardware if not using the simulator)

### Original Installation (for direct library use)

1. Clone the repository (if not already done):
   ```bash
   # git clone <repository-url>
   # cd <project-directory> # e.g., servers/src/dwave
   ```

2. Install dependencies (into your Python environment):
   ```bash
   # Assuming your current directory is where pyproject.toml for mcp_server_dwave is
   pip install -e . 
   ```
   (Note: In the Docker setup, this happens inside the container.)

3. Set up your D-Wave API token (if using real hardware, not relevant for the current simulator-only MCP server):
   - Get your token from the D-Wave Leap dashboard
   - Set it as an environment variable:
     ```bash
     export DWAVE_API_TOKEN="your-token-here"
     ```
   - Or create a `~/.dwrc` file with:
     ```json
     {
         "token": "your-token-here"
     }
     ```

### Original Server Configuration (Direct library use)

The server could be configured with various parameters:

```python
# This refers to direct usage of the mcp_server_dwave.server module
# from mcp_server_dwave.server import main as create_dwave_logic_server, ServerConfig

# Create a server logic instance with custom configuration
# config = ServerConfig(use_simulator=True) # Example
# dwave_logic_instance = create_dwave_logic_server(config)

# Or use default configuration
# dwave_logic_instance = create_dwave_logic_server()
```

### Original Problem Creation and Solving (Direct library use)

This demonstrates how one might have interacted with the `DWaveServer` class directly.

#### QUBO Problem
```python
# q_dict = {
#     ("0","0"): -1.0,  # Linear term for variable 0
#     ("1","1"): -1.0,  # Linear term for variable 1
#     ("0","1"): 2.0    # Quadratic term between variables 0 and 1
# }
# result = dwave_logic_instance.create_qubo(Q=q_dict, description="Test QUBO")
```

#### Ising Model
```python
# h = {"0": 1.0, "1": -1.0}  # Linear terms
# J = {("0","1"): -1.0}        # Quadratic terms
# result = dwave_logic_instance.create_ising(h=h, J=J, description="Test Ising")
```

#### Solving Problems
```python
# problem_id_from_create = result["problem_id"]
# solve_result = dwave_logic_instance.solve_problem(problem_id=problem_id_from_create)

# The result includes:
# - Best solution found
# - Energy of the solution
# - Timing information
# - etc.
```

### Original Visualization (Direct library use)

The original package had stubs or plans for visualization.
```python
# Visualize problem structure
# viz = dwave_logic_instance.visualize_problem(problem_id) # Placeholder

# Visualize results
# viz = dwave_logic_instance.visualize_results(result_id, plot_type="histogram") # Placeholder
```

## Development Notes (for `mcp_server_dwave` package)

### Code Style & Tools

The underlying Python package `mcp_server_dwave` uses:
- Poetry for dependency management (see `pyproject.toml`)
- Black for code formatting
- Ruff for linting (potentially)
- Pytest for testing (tests may need updating for MCP context)

## License

MIT License
(Content of MIT License should be here if not in a separate LICENSE file) 