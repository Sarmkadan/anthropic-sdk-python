"""Simple conftest for benchmarks that doesn't depend on test infrastructure."""

import pytest


@pytest.fixture
def sync_client():
    """Create a synchronous client for benchmarking."""
    from anthropic import Anthropic
    return Anthropic(api_key="test-api-key")



@pytest.fixture
async def async_client():
    """Create an async client for benchmarking."""
    from anthropic import AsyncAnthropic
    return AsyncAnthropic(api_key="test-api-key")