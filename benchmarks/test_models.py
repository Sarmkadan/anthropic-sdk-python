"""
Benchmarks for model operations.

These benchmarks measure the performance of listing and retrieving models,
which are common operations for discovering available models.
"""

import pytest
import respx
from httpx import Response
from anthropic import Anthropic, AsyncAnthropic



@pytest.mark.benchmark(group="model_operations")
def test_list_models(sync_client, benchmark):
    """Benchmark listing available models."""
    with respx.mock:
        respx.get("https://api.anthropic.com/v1/models").return_value = Response(
            200,
            json={
                "object": "list",
                "data": [
                    {
                        "id": "claude-3-5-sonnet-20240620",
                        "name": "Claude 3.5 Sonnet",
                        "description": "Claude 3.5 Sonnet model",
                        "created": 1718883200,
                        "is_legacy": False,
                    },
                    {
                        "id": "claude-3-opus-20240229",
                        "name": "Claude 3 Opus",
                        "description": "Claude 3 Opus model",
                        "created": 1709206400,
                        "is_legacy": False,
                    },
                    {
                        "id": "claude-3-haiku-20240307",
                        "name": "Claude 3 Haiku",
                        "description": "Claude 3 Haiku model",
                        "created": 1709728000,
                        "is_legacy": False,
                    },
                ],
                "first_id": "claude-3-5-sonnet-20240620",
                "last_id": "claude-3-haiku-20240307",
                "has_more": False,
            },
        )

        result = benchmark(sync_client.models.list)

        assert result is not None
        assert len(result.data) == 3



@pytest.mark.benchmark(group="model_operations")
def test_get_model(sync_client, benchmark):
    """Benchmark retrieving a specific model."""
    with respx.mock:
        model_id = "claude-3-5-sonnet-20240620"
        respx.get(f"https://api.anthropic.com/v1/models/{model_id}").return_value = Response(
            200,
            json={
                "id": model_id,
                "name": "Claude 3.5 Sonnet",
                "description": "Claude 3.5 Sonnet model",
                "created": 1718883200,
                "is_legacy": False,
                "input modalities": ["text"],
                "output modalities": ["text"],
                "default max tokens": 8192,
                "max output tokens": 8192,
            },
        )

        result = benchmark(sync_client.models.retrieve, model=model_id)

        assert result is not None
        assert result.id == model_id



@pytest.mark.benchmark(group="model_operations")
class TestModelOperations:
    """Benchmarks for various model operations."""

    def test_list_models_with_limit(self, sync_client, benchmark):
        """Benchmark listing models with limit parameter."""
        with respx.mock:
            respx.get("https://api.anthropic.com/v1/models?limit=5").return_value = Response(
                200,
                json={
                    "object": "list",
                    "data": [
                        {
                            "id": f"model-{i}",
                            "name": f"Model {i}",
                            "description": f"Test model {i}",
                            "created": 1700000000 + i,
                            "is_legacy": False,
                        }
                        for i in range(5)
                    ],
                    "first_id": "model-0",
                    "last_id": "model-4",
                    "has_more": False,
                },
            )

            result = benchmark(
                lambda: sync_client.models.list(limit=5)
            )
            assert result is not None
            assert len(result.data) == 5

    def test_list_models_with_prefix(self, sync_client, benchmark):
        """Benchmark listing models with prefix filter."""
        with respx.mock:
            respx.get("https://api.anthropic.com/v1/models").return_value = Response(
                200,
                json={
                    "object": "list",
                    "data": [
                        {
                            "id": "claude-3-5-sonnet-20240620",
                            "name": "Claude 3.5 Sonnet",
                            "description": "Claude 3.5 Sonnet model",
                            "created": 1718883200,
                            "is_legacy": False,
                        },
                    ],
                    "first_id": "claude-3-5-sonnet-20240620",
                    "last_id": "claude-3-5-sonnet-20240620",
                    "has_more": False,
                },
            )

            result = benchmark(sync_client.models.list)
            assert result is not None



@pytest.mark.benchmark(group="model_operations")
class TestAsyncModelOperations:
    """Benchmarks for async model operations."""

    @pytest.mark.asyncio
    async def test_async_list_models(self, async_client, benchmark):
        """Benchmark async listing of models."""
        with respx.mock:
            respx.get("https://api.anthropic.com/v1/models").return_value = Response(
                200,
                json={
                    "object": "list",
                    "data": [
                        {
                            "id": "claude-3-5-sonnet-20240620",
                            "name": "Claude 3.5 Sonnet",
                            "description": "Claude 3.5 Sonnet model",
                            "created": 1718883200,
                            "is_legacy": False,
                        },
                    ],
                    "first_id": "claude-3-5-sonnet-20240620",
                    "last_id": "claude-3-5-sonnet-20240620",
                    "has_more": False,
                },
            )

            result = await benchmark(async_client.models.list)
            assert result is not None
            assert len(result.data) == 1

    @pytest.mark.asyncio
    async def test_async_get_model(self, async_client, benchmark):
        """Benchmark async retrieval of a specific model."""
        with respx.mock:
            model_id = "claude-3-opus-20240229"
            respx.get(f"https://api.anthropic.com/v1/models/{model_id}").return_value = Response(
                200,
                json={
                    "id": model_id,
                    "name": "Claude 3 Opus",
                    "description": "Claude 3 Opus model",
                    "created": 1709206400,
                    "is_legacy": False,
                },
            )

            result = await benchmark(
                lambda: async_client.models.retrieve(model=model_id)
            )
            assert result is not None
            assert result.id == model_id

    @pytest.mark.asyncio
    async def test_async_list_models_pagination(self, async_client, benchmark):
        """Benchmark async model listing with pagination.

        Measures performance when dealing with paginated results.
        """
        with respx.mock:
            # Mock paginated response
            respx.get("https://api.anthropic.com/v1/models?limit=5").return_value = Response(
                200,
                json={
                    "object": "list",
                    "data": [
                        {
                            "id": f"model-{i}",
                            "name": f"Model {i}",
                            "description": f"Test model {i}",
                            "created": 1700000000 + i,
                            "is_legacy": False,
                        }
                        for i in range(5)
                    ],
                    "first_id": "model-0",
                    "last_id": "model-4",
                    "has_more": True,  # Indicates there's more data
                },
            )

            result = await benchmark(
                lambda: async_client.models.list(limit=5)
            )
            assert result is not None
            assert len(result.data) == 5
            assert result.has_more is True
