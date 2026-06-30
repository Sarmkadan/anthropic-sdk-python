# syntax=docker/dockerfile:1

# ========================================================================================
# Development and testing image for the Anthropic SDK
# This image provides a complete environment for testing and development
# ========================================================================================

FROM python:3.9-slim as base

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install uv for faster dependency management
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml uv.lock ./
COPY README.md ./

# Create virtual environment
RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
RUN uv pip install --no-cache-dir .[dev]

# Copy source code
COPY src/ src/
COPY examples/ examples/

# Set environment variable for API key
ENV ANTHROPIC_API_KEY=""

# Default command
CMD ["python", "-c", "import anthropic; print(f'Anthropic SDK {anthropic.__version__} ready')"]


# ========================================================================================
# Production build stage
# ========================================================================================

FROM python:3.9-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install build tools
RUN pip install --no-cache-dir uv hatchling==1.26.3

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install build dependencies
RUN uv pip install --no-cache-dir hatch-fancy-pypi-readme

# Build the package
COPY . .
RUN uv pip install --system hatch-fancy-pypi-readme hatchling==1.26.3
RUN hatch build -t wheel

# ========================================================================================
# Final production image
# ========================================================================================
FROM python:3.9-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Expose port 8080
EXPOSE 8080

# Install uv for dependency management
RUN pip install --no-cache-dir uv


# Copy built wheel from builder
COPY --from=builder /app/dist/*.whl /tmp/

# Create virtual environment
RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install the package
RUN uv pip install --no-cache-dir /tmp/*.whl

# Copy source for development (optional)
COPY src/anthropic/ /opt/venv/lib/python3.9/site-packages/anthropic/

# Set environment variable for API key
ENV ANTHROPIC_API_KEY=""

# Default command
CMD ["python", "-c", "import anthropic; print(f'Anthropic SDK {anthropic.__version__} ready')"]
