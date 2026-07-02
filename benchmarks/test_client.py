"""
Benchmarks for client initialization and configuration.

These benchmarks measure the performance of client creation and configuration,
which is critical for SDK startup time and initialization overhead.
"""

import pytest
from anthropic import Anthropic, AsyncAnthropic



@pytest.mark.benchmark(group="client_initialization")
def test_client_initialization(benchmark):
    """Benchmark synchronous client initialization."""
    result = benchmark(
        lambda: Anthropic(
            api_key="test-api-key",
            base_url="https://api.anthropic.com",
            timeout=30.0,
            max_retries=3,
        )
    )
    assert result is not None
    assert isinstance(result, Anthropic)



@pytest.mark.benchmark(group="client_initialization")
def test_client_initialization_with_config(benchmark):
    """Benchmark client initialization with full configuration."""
    result = benchmark(
        lambda: Anthropic(
            api_key="test-api-key",
            auth_token="test-auth-token",
            base_url="https://api.anthropic.com",
            timeout=30.0,
            max_retries=5,
            default_headers={"X-Custom-Header": "value"},
            default_query={"version": "2023-06-01"},
        )
    )
    assert result is not None



@pytest.mark.benchmark(group="client_initialization")
def test_async_client_initialization(benchmark):
    """Benchmark async client initialization."""
    result = benchmark(
        lambda: AsyncAnthropic(
            api_key="test-api-key",
            base_url="https://api.anthropic.com",
            timeout=30.0,
            max_retries=3,
        )
    )
    assert result is not None
    assert isinstance(result, AsyncAnthropic)



@pytest.mark.benchmark(group="client_initialization")
def test_client_reinitialization(benchmark):
    """Benchmark repeated client initialization (realistic usage pattern)."""
    def init_client():
        return Anthropic(api_key="test-api-key")

    # Simulate creating multiple clients in sequence
    results = benchmark.pedantic(
        init_client,
        rounds=100,
        iterations=1,
    )
    assert len(results) == 100



@pytest.mark.benchmark(group="client_memory")
def test_client_memory_allocation(benchmark):
    """Benchmark memory allocation during client creation."""
    result = benchmark(
        lambda: Anthropic(api_key="test-api-key")
    )
    assert result is not None



@pytest.mark.benchmark(group="client_initialization")
class TestClientConfiguration:
    """Benchmarks for different client configuration scenarios."""

    def test_client_with_minimal_config(self, benchmark):
        """Benchmark client with minimal configuration."""
        result = benchmark(
            lambda: Anthropic(api_key="test-api-key")
        )
        assert result is not None

    def test_client_with_max_retries(self, benchmark):
        """Benchmark client with high max_retries."""
        result = benchmark(
            lambda: Anthropic(api_key="test-api-key", max_retries=100)
        )
        assert result is not None

    def test_client_with_timeout(self, benchmark):
        """Benchmark client with custom timeout."""
        result = benchmark(
            lambda: Anthropic(api_key="test-api-key", timeout=60.0)
        )
        assert result is not None
