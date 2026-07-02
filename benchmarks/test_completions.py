"""
Benchmarks for completion operations.

These benchmarks measure the performance of the completions API,
which is an alternative to the messages API for simpler use cases.
"""

import pytest
import respx
from httpx import Response
from anthropic import Anthropic, AsyncAnthropic



@pytest.mark.benchmark(group="completion_operations")
def test_completion_create(sync_client, benchmark):
    """Benchmark completion creation."""
    with respx.mock:
        respx.post("https://api.anthropic.com/v1/completions").return_value = Response(
            200,
            json={
                "id": "comp_test_123",
                "type": "completion",
                "completion": "This is a test completion response",
                "model": "claude-3-5-sonnet-20240620",
                "stop_reason": "end_turn",
                "stop_sequence": None,
                "usage": {
                    "input_tokens": 15,
                    "output_tokens": 25,
                },
            },
        )

        result = benchmark(
            sync_client.completions.create,
            model="claude-3-5-sonnet-20240620",
            prompt="\n\nHuman: Hello\n\nAssistant:",
            max_tokens_to_sample=1024,
        )

        assert result is not None
        assert result.id == "comp_test_123"



@pytest.mark.benchmark(group="completion_operations")
def test_completion_with_system(sync_client, benchmark):
    """Benchmark completion with system prompt."""
    with respx.mock:
        respx.post("https://api.anthropic.com/v1/completions").return_value = Response(
            200,
            json={
                "id": "comp_system_456",
                "type": "completion",
                "completion": "Response with system context",
                "model": "claude-3-5-sonnet-20240620",
                "stop_reason": "end_turn",
                "usage": {
                    "input_tokens": 20,
                    "output_tokens": 30,
                },
            },
        )

        result = benchmark(
            sync_client.completions.create,
            model="claude-3-5-sonnet-20240620",
            prompt="\n\nHuman: Explain AI\n\nAssistant:",
            system="You are an AI expert",
            max_tokens_to_sample=1024,
        )

        assert result is not None



@pytest.mark.benchmark(group="completion_operations")
class TestCompletionOperations:
    """Benchmarks for various completion operations."""

    def test_completion_with_temperature(self, sync_client, benchmark):
        """Benchmark completion with temperature parameter."""
        with respx.mock:
            respx.post("https://api.anthropic.com/v1/completions").return_value = Response(
                200,
                json={
                    "id": "comp_temp_789",
                    "type": "completion",
                    "completion": "Temperature controlled response",
                    "model": "claude-3-5-sonnet-20240620",
                    "stop_reason": "end_turn",
                    "usage": {"input_tokens": 15, "output_tokens": 25},
                },
            )

            result = benchmark(
                sync_client.completions.create,
                model="claude-3-5-sonnet-20240620",
                prompt="\n\nHuman: Test\n\nAssistant:",
                max_tokens_to_sample=1024,
                temperature=0.8,
            )
            assert result is not None

    def test_completion_with_stop_sequences(self, sync_client, benchmark):
        """Benchmark completion with stop sequences."""
        with respx.mock:
            respx.post("https://api.anthropic.com/v1/completions").return_value = Response(
                200,
                json={
                    "id": "comp_stop_abc",
                    "type": "completion",
                    "completion": "Response with stop sequence",
                    "model": "claude-3-5-sonnet-20240620",
                    "stop_reason": "stop_sequence",
                    "stop_sequence": "\n\nHuman:",
                    "usage": {"input_tokens": 15, "output_tokens": 25},
                },
            )

            result = benchmark(
                sync_client.completions.create,
                model="claude-3-5-sonnet-20240620",
                prompt="\n\nHuman: Write a poem\n\nAssistant:",
                max_tokens_to_sample=1024,
                stop_sequences=["\n\nHuman:"],
            )
            assert result is not None



@pytest.mark.benchmark(group="completion_operations")
class TestAsyncCompletionOperations:
    """Benchmarks for async completion operations."""

    @pytest.mark.asyncio
    async def test_async_completion_create(self, async_client, benchmark):
        """Benchmark async completion creation."""
        with respx.mock:
            respx.post("https://api.anthropic.com/v1/completions").return_value = Response(
                200,
                json={
                    "id": "comp_async_xyz",
                    "type": "completion",
                    "completion": "Async completion response",
                    "model": "claude-3-5-sonnet-20240620",
                    "stop_reason": "end_turn",
                    "usage": {"input_tokens": 15, "output_tokens": 25},
                },
            )

            result = await benchmark(
                async_client.completions.create,
                model="claude-3-5-sonnet-20240620",
                prompt="\n\nHuman: Async test\n\nAssistant:",
                max_tokens_to_sample=1024,
            )
            assert result is not None
            assert result.id == "comp_async_xyz"
