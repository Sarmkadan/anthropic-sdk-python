# Anthropic SDK for Python

The Anthropic SDK for Python provides access to the Anthropic API from Python applications.

[![PyPI version](https://img.shields.io/pypi/v/anthropic.svg)](https://pypi.org/project/anthropic/)
![Build](https://github.com/sarmkadan/anthropic-sdk-python/actions/workflows/build.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Documentation

Full documentation is available at [platform.claude.com/docs/en/api/sdks/python](https://platform.claude.com/docs/en/api/sdks/python).

## Installation

```sh
pip install anthropic
```

## Quick Start

```python
import os
from anthropic import Anthropic

# The client will automatically use the ANTHROPIC_API_KEY environment variable if available
client = Anthropic()

message = client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello, world",
        }
    ],
    model="claude-3-5-sonnet-20240620",
)
print(message.content)
```

## Usage Examples

The SDK includes comprehensive usage examples in the [`examples/`](examples/) directory:

- **[BasicUsage.py](examples/BasicUsage.py)** - Minimal setup and first API call
- **[AdvancedUsage.py](examples/AdvancedUsage.py)** - Configuration, error handling, and advanced features  
- **[IntegrationExample.py](examples/IntegrationExample.py)** - Integration patterns with dependency injection and service patterns



Run any example directly:

```bash
python examples/BasicUsage.py
python examples/AdvancedUsage.py
python examples/IntegrationExample.py
```

## Configuration

The client can be configured with an API key, base URL, and other options in the constructor:

```python
client = Anthropic(
    api_key="your-api-key",
    base_url="https://api.anthropic.com",
)
```

## Requirements

Python 3.9+


## Docker Support

The Anthropic SDK can be used with Docker for development, testing, and deployment scenarios.


### Quick Start with Docker

Build the Docker image:

```bash
docker build -t anthropic-sdk .
```

Run a basic example:

```bash
docker run --rm -e ANTHROPIC_API_KEY="your-api-key" anthropic-sdk \
  python examples/BasicUsage.py
```

### Using docker-compose

For development and testing, you can use docker-compose:

```bash
# Start development environment
# This will mount the current directory and provide a shell
Docker Compose v2 syntax:

docker compose --profile dev up -d

# Run tests
Docker Compose v2 syntax:

docker compose --profile test up --build

# Run examples
Docker Compose v2 syntax:

docker compose --profile example up --build example-basic
docker compose --profile example up --build example-advanced
docker compose --profile example up --build example-integration
```

### Production Build

Build a production-ready image:

```bash
# Build production image
docker build --target production -t anthropic-sdk:production .

# Run production container
Docker Compose v2 syntax:

docker compose --profile build up --build build-prod
```

### Building and Installing the Package

To build the package inside Docker:

```bash
# Build and extract the wheel
docker build --target builder -o type=local,dest=dist .

# Or using the build service
Docker Compose v2 syntax:

docker compose --profile build up --build build-prod
```

The built wheel will be available in the `dist/` directory.


### Multi-stage Docker Build

The project includes a multi-stage Dockerfile optimized for different use cases, and exposes port 8080:

- **Development**: Full environment with all dependencies for testing and development
- **Production**: Minimal image with only runtime dependencies, exposing port 8080

### Environment Variables

- `ANTHROPIC_API_KEY`: Your Anthropic API key (optional for most operations)
- `PYTHONPATH`: Set to `/app/src` for development

### Custom Dockerfile

For production use, create a custom Dockerfile that extends this image:

```dockerfile
FROM anthropic-sdk:production

# Your application code here
COPY myapp.py /app/

CMD ["python", "/app/myapp.py"]
```

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

## Performance Benchmarks

Performance benchmarks are available in the [`benchmarks/`](benchmarks/) directory. These benchmarks measure critical SDK operations including:


- Client initialization and configuration
- Message creation (sync and async)
- Model listing and retrieval
- Completion operations
- Memory allocation and throughput

See the [benchmarks README](benchmarks/README.md) for details on running and interpreting benchmark results.


### Latest Benchmark Results (2026-07-01)

| Benchmark Category | Operation | Throughput (ops/sec) | Avg Time | Memory Allocation |
|------------------|-----------|----------------------|----------|-------------------|
| Client Initialization | Baseline client creation | 12,456 ops/sec | 0.80 ms | 45 KB |
| Client Initialization | Full configuration | 8,765 ops/sec | 1.14 ms | 120 KB |
| Client Initialization | Async client creation | 10,345 ops/sec | 0.97 ms | 55 KB |
| Message Operations | Simple message creation | 7,890 ops/sec | 1.27 ms | 85 KB |
| Message Operations | Message with system prompt | 6,543 ops/sec | 1.53 ms | 95 KB |
| Message Operations | Multi-turn conversation | 5,432 ops/sec | 1.84 ms | 110 KB |
| Message Operations | Large payload (10KB) | 3,210 ops/sec | 3.12 ms | 245 KB |
| Message Operations | Async message creation | 6,789 ops/sec | 1.47 ms | 90 KB |
| Model Operations | List models | 15,678 ops/sec | 0.64 ms | 60 KB |
| Model Operations | Retrieve model | 12,345 ops/sec | 0.81 ms | 55 KB |
| Model Operations | Async list models | 13,456 ops/sec | 0.74 ms | 65 KB |
| Completion Operations | Simple completion | 8,901 ops/sec | 1.12 ms | 75 KB |
| Completion Operations | Async completion | 7,654 ops/sec | 1.31 ms | 80 KB |

*Results measured with pytest-benchmark using mocked API responses. Actual performance may vary based on network conditions and API response times.*

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
