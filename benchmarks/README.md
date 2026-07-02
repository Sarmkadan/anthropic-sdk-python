# Performance Benchmarks

This directory contains performance benchmarks for the Anthropic SDK using `pytest-benchmark`.

The benchmarks follow the **BenchmarkDotNet** methodology, focusing on:

- **Throughput**: Operations per second (ops/sec)
- **Latency**: Time per operation (min/max/mean/median)
- **Memory**: Memory allocations and overhead
- **Comparison**: Historical comparison across runs

## Running Benchmarks

### Prerequisites

Install benchmark dependencies:

```bash
pip install pytest-benchmark pytest-asyncio respx memory-profiler
```

### Running All Benchmarks

```bash
# Run all benchmarks
pytest benchmarks/

# Run with verbose output (recommended for benchmark analysis)
pytest benchmarks/ -v

# Run with specific benchmark only
pytest benchmarks/test_client.py -v
```

### Running Specific Benchmark Groups

```bash
# Client initialization benchmarks
pytest benchmarks/test_client.py::test_client_initialization -v

# Message creation benchmarks (most critical operations)
pytest benchmarks/test_messages.py -v

# Model listing benchmarks
pytest benchmarks/test_models.py -v

# Completion operations
pytest benchmarks/test_completions.py -v

# Client operations (new comprehensive benchmarks)
pytest benchmarks/test_client_operations.py -v
```

### Running with Different Configurations

```bash
# Run with different message batch sizes
pytest benchmarks/test_messages.py -v --benchmark-json=results.json

# Generate HTML report with charts
pytest benchmarks/ -v --benchmark-html

# Save results for comparison
pytest benchmarks/ -v --benchmark-json=results.json

# Compare with previous results
pytest benchmarks/ --benchmark-compare=results.json
```

### Running Memory Profiling

```bash
# Run benchmarks with memory profiling
pytest benchmarks/test_client_operations.py::test_client_memory_allocation_simple -v --benchmark-memory
```

## Benchmark Results

The benchmarks measure critical SDK operations with the following metrics:

| Metric | Description | BenchmarkDotNet Equivalent |
|--------|-------------|---------------------------|
| **ops/sec** | Operations per second (throughput) | `Throughput` |
| **time/op** | Time per operation | `Mean`, `Median`, `Min`, `Max` |
| **alloc/op** | Memory allocations per operation | `MemoryDiagnoser` |
| **Rounds** | Number of iterations | `Iterations` |

### Sample Benchmark Output

```
----------------------------------------------------------------------
Benchmark                          Size  Operations  ops/sec     Mean  
----------------------------------------------------------------------
test_client_initialization_baseline  1     100         12543.21  0.7976ms
test_message_create_simple           1     100         8765.43   1.1408ms
test_list_models                    1     100         15678.90  0.6378ms
```

## Benchmark Categories

### 1. Client Initialization (`client_initialization`)
Measures the performance of creating client instances with different configurations.

### 2. Message Operations (`message_operations`)
**Most critical category** - measures message creation performance which is the primary SDK operation.

### 3. Model Operations (`model_operations`)
Measures model listing and retrieval performance.

### 4. Completion Operations (`completion_operations`)
Measures the completions API performance (alternative to messages API).

### 5. Client Memory (`client_memory`)
Measures memory allocation during client creation.

### 6. Client Throughput (`client_throughput`)
Measures how many operations can be performed per second.

## Adding New Benchmarks

To add new benchmarks following the BenchmarkDotNet methodology:

1. Create a new test file in the `benchmarks/` directory
2. Use the `pytest-benchmark` fixture for timing
3. Focus on **single operations** (keep benchmarks focused)
4. Include both **sync and async variants** where applicable
5. Use **realistic payload sizes**
6. **Mock API responses** to avoid network I/O in microbenchmarks
7. Document any external dependencies or setup required

### Example Benchmark Structure

```python
import pytest
import respx
from httpx import Response
from anthropic import Anthropic

@pytest.mark.benchmark(group="my_category")
def test_my_operation(benchmark):
    """Benchmark description."""
    with respx.mock:
        respx.post("https://api.anthropic.com/v1/endpoint").return_value = Response(
            200,
            json={"result": "mocked"},
        )

        result = benchmark(
            my_function,
            param1="value",
            param2=123,
        )
        assert result is not None
```

## Critical Operations Benchmarked

The following operations are critical and are benchmarked in this suite:


### Client Operations
- ✅ Client initialization (sync and async)
- ✅ Client configuration variations (timeouts, retries, headers)
- ✅ Memory allocation during client creation
- ✅ Repeated client initialization (realistic usage pattern)

### Message Operations (Most Critical)
- ✅ Simple message creation
- ✅ Message with system prompt
- ✅ Multi-turn conversation (multiple messages)
- ✅ Large input payloads (10KB+)
- ✅ Different model configurations
- ✅ Async message creation
- ✅ Batch message operations
- ✅ Streaming operations

### Model Operations
- ✅ List all models
- ✅ Retrieve specific model
- ✅ Pagination support
- ✅ Async variants

### Completion Operations
- ✅ Completion creation
- ✅ Completion with system prompt
- ✅ Temperature variations
- ✅ Stop sequences
- ✅ Async variants

## Best Practices

### For Benchmark Authors
- Use `respx` to mock HTTP responses (avoid network I/O)
- Use realistic payload sizes (don't use tiny test data)
- Include both sync and async variants
- Document the benchmark purpose and what it measures
- Use `benchmark.pedantic()` for multi-round benchmarks
- Group related benchmarks using `group="category_name"`

### For Running Benchmarks
- Run with `-v` flag for detailed output
- Use `--benchmark-json` to save results for comparison
- Use `--benchmark-html` to generate visual reports
- Run benchmarks multiple times for consistent results
- Warm up the Python interpreter before running (first run is slower)

## Performance Goals

The benchmarks aim to track these key performance indicators:

1. **Client initialization time** < 10ms (baseline)
2. **Message creation throughput** > 500 ops/sec (with mocked responses)
3. **Model listing time** < 5ms per operation
4. **Memory overhead** < 1MB per client instance
5. **Async operations** comparable to sync operations

## Results Comparison

To compare benchmark results across runs:

```bash
# Save current results
pytest benchmarks/ -v --benchmark-json=results_v1.json

# Make changes to SDK
# ...

# Save new results
pytest benchmarks/ -v --benchmark-json=results_v2.json

# Compare
pytest benchmarks/ --benchmark-compare=results_v1.json
```

## CI Integration

Benchmarks can be integrated into CI/CD pipelines to track performance regressions:

```yaml
# Example GitHub Actions step
- name: Run benchmarks
  run: |
    pip install pytest-benchmark respx
    pytest benchmarks/ -v --benchmark-json=benchmark_results.json
    
    # Upload results for comparison
    python scripts/upload_benchmarks.py benchmark_results.json
```

## Additional Resources

- [pytest-benchmark Documentation](https://pytest-benchmark.readthedocs.io/)
- [BenchmarkDotNet Methodology](https://benchmarkdotnet.org/)
- [Python Performance Tips](https://docs.python.org/3/library/timeit.html)
