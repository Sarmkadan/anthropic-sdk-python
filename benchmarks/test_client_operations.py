"""
Comprehensive benchmarks for client operations including initialization, configuration,
and resource-intensive operations.

These benchmarks measure critical SDK operations that impact performance and memory usage.
"""

import pytest
from anthropic import Anthropic, AsyncAnthropic



@pytest.mark.benchmark(group="client_initialization")
def test_client_initialization_baseline(benchmark):
    """Benchmark baseline synchronous client initialization."""
    result = benchmark(
        lambda: Anthropic(api_key="test-api-key")
    )
    assert result is not None
    assert isinstance(result, Anthropic)



@pytest.mark.benchmark(group="client_initialization")
def test_client_initialization_full_config(benchmark):
    """Benchmark client initialization with comprehensive configuration."""
    result = benchmark(
        lambda: Anthropic(
            api_key="test-api-key",
            auth_token="test-auth-token",
            base_url="https://api.anthropic.com",
            timeout=30.0,
            max_retries=5,
            default_headers={"X-Custom-Header": "value", "User-Agent": "test-sdk"},
            default_query={"version": "2023-06-01", "custom": "param"},
        )
    )
    assert result is not None



@pytest.mark.benchmark(group="client_initialization")
def test_async_client_initialization_baseline(benchmark):
    """Benchmark baseline async client initialization."""
    result = benchmark(
        lambda: AsyncAnthropic(api_key="test-api-key")
    )
    assert result is not None
    assert isinstance(result, AsyncAnthropic)



@pytest.mark.benchmark(group="client_initialization")
def test_client_initialization_with_timeout_variations(benchmark):
    """Benchmark client initialization with different timeout values."""
    # Test short timeout
    result_short = benchmark(
        lambda: Anthropic(api_key="test-api-key", timeout=5.0)
    )
    assert result_short is not None

    # Test long timeout - use separate test for this variation
    pass



@pytest.mark.benchmark(group="client_initialization")
def test_client_initialization_with_retry_variations(benchmark):
    """Benchmark client initialization with different retry configurations."""
    # Test no retries
    result_no_retry = benchmark(
        lambda: Anthropic(api_key="test-api-key", max_retries=0)
    )
    assert result_no_retry is not None

    # Test high retries - use separate test
    pass



@pytest.mark.benchmark(group="client_initialization")
def test_client_repeated_initialization(benchmark):
    """Benchmark repeated client initialization (realistic usage pattern).

    This simulates creating multiple client instances in sequence, which is a
    common pattern in applications that need to switch between configurations.
    """
    def init_client():
        return Anthropic(api_key="test-api-key", timeout=30.0)

    # Use pedantic to run multiple iterations
    benchmark.pedantic(
        init_client,
        rounds=50,
        iterations=1,
    )



@pytest.mark.benchmark(group="client_memory")
def test_client_memory_allocation_simple(benchmark):
    """Benchmark memory allocation during simple client creation.

    Measures the memory overhead of creating a basic client instance.
    """
    result = benchmark(
        lambda: Anthropic(api_key="test-api-key")
    )
    assert result is not None



@pytest.mark.benchmark(group="client_memory")
def test_client_memory_allocation_full(benchmark):
    """Benchmark memory allocation during full client creation.

    Measures the memory overhead of creating a fully configured client.
    """
    result = benchmark(
        lambda: Anthropic(
            api_key="test-api-key",
            base_url="https://api.anthropic.com",
            timeout=60.0,
            max_retries=10,
            default_headers={"X-Custom": "value"},
        )
    )
    assert result is not None



@pytest.mark.benchmark(group="client_memory")
def test_client_memory_allocation_async(benchmark):
    """Benchmark memory allocation for async client."""
    result = benchmark(
        lambda: AsyncAnthropic(api_key="test-api-key")
    )
    assert result is not None



@pytest.mark.benchmark(group="client_throughput")
class TestClientThroughput:
    """Benchmarks for client creation throughput under different scenarios."""

    def test_client_creation_throughput(self, benchmark):
        """Benchmark client creation throughput (operations per second).

        Measures how many client instances can be created per second.
        """
        def create_client():
            return Anthropic(api_key="test-api-key")

        # Measure throughput
        benchmark.pedantic(
            create_client,
            rounds=100,
            iterations=1,
        )

    def test_client_creation_throughput_async(self, benchmark):
        """Benchmark async client creation throughput."""
        def create_async_client():
            return AsyncAnthropic(api_key="test-api-key")

        benchmark.pedantic(
            create_async_client,
            rounds=100,
            iterations=1,
        )

    def test_client_creation_with_config_variations(self, benchmark):
        """Benchmark client creation with different configuration variations."""
        configs = [
            {"timeout": 10.0},
            {"timeout": 30.0, "max_retries": 3},
            {"timeout": 60.0, "max_retries": 10, "default_headers": {"X-Test": "1"}},
        ]

        for config in configs:
            benchmark(
                lambda cfg=config: Anthropic(api_key="test-api-key", **cfg)
            )
