"""
Benchmarks for message operations - the most critical SDK operations.

These benchmarks measure the performance of message creation, which is the
primary operation users perform with the SDK.
"""

import pytest
import respx
from httpx import Response
from anthropic import Anthropic, AsyncAnthropic



@pytest.fixture
def sync_client():
    """Create a synchronous client for benchmarking."""
    return Anthropic(api_key="test-api-key")



@pytest.fixture
async def async_client():
    """Create an async client for benchmarking."""
    return AsyncAnthropic(api_key="test-api-key")



@pytest.mark.benchmark(group="message_operations")
def test_message_create_simple(sync_client, benchmark):
    """Benchmark simple message creation."""
    with respx.mock:
        # Mock the API response
        respx.post("https://api.anthropic.com/v1/messages").return_value = Response(
            200,
            json={
                "id": "msg_test_123",
                "type": "message",
                "role": "assistant",
                "model": "claude-3-5-sonnet-20240620",
                "content": [{"type": "text", "text": "Hello, world!"}],
                "stop_reason": "end_turn",
                "stop_sequence": None,
                "usage": {
                    "input_tokens": 10,
                    "output_tokens": 20,
                },
            },
        )

        result = benchmark(
            sync_client.messages.create,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Hello, world",
                }
            ],
            model="claude-3-5-sonnet-20240620",
        )

        assert result is not None
        assert result.id == "msg_test_123"



@pytest.mark.benchmark(group="message_operations")
def test_message_create_with_system_prompt(sync_client, benchmark):
    """Benchmark message creation with system prompt."""
    with respx.mock:
        respx.post("https://api.anthropic.com/v1/messages").return_value = Response(
            200,
            json={
                "id": "msg_test_456",
                "type": "message",
                "role": "assistant",
                "model": "claude-3-5-sonnet-20240620",
                "content": [{"type": "text", "text": "Response with system context"}],
                "stop_reason": "end_turn",
                "usage": {
                    "input_tokens": 25,
                    "output_tokens": 30,
                },
            },
        )

        result = benchmark(
            sync_client.messages.create,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Explain quantum computing",
                }
            ],
            model="claude-3-5-sonnet-20240620",
            system="You are a helpful assistant",
        )

        assert result is not None



@pytest.mark.benchmark(group="message_operations")
def test_message_create_with_multiple_messages(sync_client, benchmark):
    """Benchmark message creation with multiple messages (conversation history)."""
    with respx.mock:
        respx.post("https://api.anthropic.com/v1/messages").return_value = Response(
            200,
            json={
                "id": "msg_test_789",
                "type": "message",
                "role": "assistant",
                "model": "claude-3-5-sonnet-20240620",
                "content": [{"type": "text", "text": "Response to multi-turn conversation"}],
                "stop_reason": "end_turn",
                "usage": {
                    "input_tokens": 100,
                    "output_tokens": 50,
                },
            },
        )

        result = benchmark(
            sync_client.messages.create,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi there!"},
                {"role": "user", "content": "What can you do?"},
            ],
            model="claude-3-5-sonnet-20240620",
        )

        assert result is not None



@pytest.mark.benchmark(group="message_operations")
def test_message_create_with_large_input(sync_client, benchmark):
    """Benchmark message creation with large input payload."""
    with respx.mock:
        respx.post("https://api.anthropic.com/v1/messages").return_value = Response(
            200,
            json={
                "id": "msg_test_large",
                "type": "message",
                "role": "assistant",
                "model": "claude-3-5-sonnet-20240620",
                "content": [{"type": "text", "text": "Response"}],
                "stop_reason": "end_turn",
                "usage": {
                    "input_tokens": 500,
                    "output_tokens": 100,
                },
            },
        )

        # Create a large message payload
        large_content = "A" * 10000  # 10KB of content

        result = benchmark(
            sync_client.messages.create,
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": large_content,
                }
            ],
            model="claude-3-5-sonnet-20240620",
        )

        assert result is not None



@pytest.mark.benchmark(group="message_operations")
class TestMessageCreateConfigurations:
    """Benchmarks for different message creation configurations."""

    def test_message_with_max_tokens(self, sync_client, benchmark):
        """Benchmark message creation with high max_tokens."""
        with respx.mock:
            respx.post("https://api.anthropic.com/v1/messages").return_value = Response(
                200,
                json={
                    "id": "msg_max_tokens",
                    "type": "message",
                    "role": "assistant",
                    "model": "claude-3-5-sonnet-20240620",
                    "content": [{"type": "text", "text": "Response"}],
                    "stop_reason": "end_turn",
                    "usage": {"input_tokens": 10, "output_tokens": 20},
                },
            )

            result = benchmark(
                sync_client.messages.create,
                max_tokens=4096,
                messages=[{"role": "user", "content": "Test"}],
                model="claude-3-5-sonnet-20240620",
            )
            assert result is not None

    def test_message_with_temperature(self, sync_client, benchmark):
        """Benchmark message creation with temperature parameter."""
        with respx.mock:
            respx.post("https://api.anthropic.com/v1/messages").return_value = Response(
                200,
                json={
                    "id": "msg_temp",
                    "type": "message",
                    "role": "assistant",
                    "model": "claude-3-5-sonnet-20240620",
                    "content": [{"type": "text", "text": "Response"}],
                    "stop_reason": "end_turn",
                    "usage": {"input_tokens": 10, "output_tokens": 20},
                },
            )

            result = benchmark(
                sync_client.messages.create,
                max_tokens=1024,
                messages=[{"role": "user", "content": "Test"}],
                model="claude-3-5-sonnet-20240620",
                temperature=0.7,
            )
            assert result is not None



@pytest.mark.benchmark(group="message_operations")
class TestAsyncMessageOperations:
    """Benchmarks for async message operations."""

    @pytest.mark.asyncio
    async def test_async_message_create(self, async_client, benchmark):
        """Benchmark async message creation."""
        with respx.mock:
            respx.post("https://api.anthropic.com/v1/messages").return_value = Response(
                200,
                json={
                    "id": "msg_async_123",
                    "type": "message",
                    "role": "assistant",
                    "model": "claude-3-5-sonnet-20240620",
                    "content": [{"type": "text", "text": "Async response"}],
                    "stop_reason": "end_turn",
                    "usage": {"input_tokens": 10, "output_tokens": 20},
                },
            )

            result = await benchmark(
                async_client.messages.create,
                max_tokens=1024,
                messages=[{"role": "user", "content": "Hello async"}],
                model="claude-3-5-sonnet-20240620",
            )

            assert result is not None
            assert result.id == "msg_async_123"

    @pytest.mark.asyncio
    async def test_async_message_create_multiple(self, async_client, benchmark):
        """Benchmark multiple async message creations in sequence."""
        with respx.mock:
            respx.post("https://api.anthropic.com/v1/messages").return_value = Response(
                200,
                json={
                    "id": "msg_async_multi",
                    "type": "message",
                    "role": "assistant",
                    "model": "claude-3-5-sonnet-20240620",
                    "content": [{"type": "text", "text": "Response"}],
                    "stop_reason": "end_turn",
                    "usage": {"input_tokens": 10, "output_tokens": 20},
                },
            )

            # Create multiple messages in sequence
            results = []
            for i in range(10):
                result = await async_client.messages.create(
                    max_tokens=1024,
                    messages=[{"role": "user", "content": f"Message {i}"}],
                    model="claude-3-5-sonnet-20240620",
                )
                results.append(result)

            assert len(results) == 10

    @pytest.mark.asyncio
    async def test_async_message_create_large_batch(self, async_client, benchmark):
        """Benchmark creating a large batch of async messages.

        Measures throughput when creating many messages in sequence.
        """
        with respx.mock:
            respx.post("https://api.anthropic.com/v1/messages").return_value = Response(
                200,
                json={
                    "id": "msg_async_batch",
                    "type": "message",
                    "role": "assistant",
                    "model": "claude-3-5-sonnet-20240620",
                    "content": [{"type": "text", "text": "Batch response"}],
                    "stop_reason": "end_turn",
                    "usage": {"input_tokens": 50, "output_tokens": 30},
                },
            )

            # Create a batch of messages
            results = []
            for i in range(50):
                result = await async_client.messages.create(
                    max_tokens=1024,
                    messages=[{"role": "user", "content": f"Query {i}"}],
                    model="claude-3-5-sonnet-20240620",
                )
                results.append(result)

            assert len(results) == 50

    @pytest.mark.asyncio
    async def test_async_message_with_streaming_simulation(self, async_client, benchmark):
        """Benchmark async message creation with streaming simulation.

        Measures the overhead of async operations.
        """
        with respx.mock:
            respx.post("https://api.anthropic.com/v1/messages").return_value = Response(
                200,
                json={
                    "id": "msg_async_stream",
                    "type": "message",
                    "role": "assistant",
                    "model": "claude-3-5-sonnet-20240620",
                    "content": [{"type": "text", "text": "Streaming response"}],
                    "stop_reason": "end_turn",
                    "usage": {"input_tokens": 25, "output_tokens": 40},
                },
            )

            result = await benchmark(
                async_client.messages.create,
                max_tokens=2048,
                messages=[{"role": "user", "content": "Generate a long response"}],
                model="claude-3-5-sonnet-20240620",
                stream=True,
            )

            assert result is not None
            assert result.id == "msg_async_stream"
