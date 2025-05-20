FROM python:3.10-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy necessary files first
COPY src/dwave/README.md .
COPY src/dwave/pyproject.toml .
COPY src/dwave/src ./src

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip uninstall pydantic -y || true && \
    pip install --no-cache-dir "pydantic>=2.7.0" && \
    pip install --no-cache-dir "fastapi>=0.100.0" "uvicorn[standard]>=0.23.0" && \
    pip install --no-cache-dir "mcp>=1.9.0" && \
    pip install --no-cache-dir -e .

# Stage 2: Runtime
FROM python:3.10-slim

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH="/app/src"
COPY --from=builder /app/src /app/src

# Copy source code
# COPY . . # This copies the entire build context, which is too broad.
          # The project code is in the venv via 'pip install -e .'
          # api_server.py is copied separately.

# Port for HTTP server
EXPOSE 3000

# Create the MCP API server using FastMCP
COPY src/dwave/api_server.py /app/api_server.py
RUN chmod +x /app/api_server.py

# Start the server
# Ensure Uvicorn runs the app from the generated api_server.py correctly
CMD ["sh", "-c", "echo 'Listing /app contents:' && ls -R /app && echo '--- Attempting to start Uvicorn ---' && uvicorn api_server:app --host 0.0.0.0 --port 3000"] 