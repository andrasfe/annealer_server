# D-Wave MCP Server

This package provides an MCP (Model-Controller-Provider) server implementation for interacting with D-Wave quantum annealers. It allows you to create and solve QUBO (Quadratic Unconstrained Binary Optimization) and Ising model problems using D-Wave's quantum computing resources.

## Features

- Create and solve QUBO problems
- Create and solve Ising model problems
- Visualize problem structures and results
- Interact with D-Wave quantum annealers
- Support for multiple solver types
- Result analysis and visualization tools

## Requirements

- Python 3.8+
- D-Wave Leap account and API token
- Required Python packages (see pyproject.toml)

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -e .
   ```

## Configuration

Set your D-Wave API token in one of these ways:
1. Environment variable: `DWAVE_API_TOKEN`
2. Configuration file: `~/.dwrc` with JSON content: `{"token": "your-token-here"}`

## Usage

```python
from mcp_server_dwave.server import main

# Create server instance
server = main()

# Create a QUBO problem
q_dict = {
    "(0,0)": -1.0,
    "(1,1)": -1.0,
    "(0,1)": 2.0
}
result = await server.tools["create_qubo"].func(request_context, q_dict)

# Solve the problem
solve_result = await server.tools["solve_problem"].func(request_context, result["problem_id"])
```

## API Reference

### Tools

1. `list_solvers`: List available D-Wave solvers and their properties
2. `create_qubo`: Create a QUBO problem
3. `create_ising`: Create an Ising model problem
4. `solve_problem`: Submit a problem to a D-Wave solver
5. `get_result`: Get detailed information about a solve result
6. `visualize_problem`: Generate a visualization of the problem structure
7. `visualize_results`: Generate a visualization of the results

## Development

To run tests:
```bash
pytest tests/
```

## License

[Your License Here]

## Contributing

[Your Contributing Guidelines Here] 