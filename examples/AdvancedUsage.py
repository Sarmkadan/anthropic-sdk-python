# Advanced usage examples for the Anthropic SDK
# Demonstrates configuration, error handling, multiple features, and best practices

import os
import json
from typing import Dict, List, Any
from anthropic import Anthropic, APIError, RateLimitError, BadRequestError
from anthropic.types import Message, TextBlock, ToolUseBlock

# Example 1: Advanced client configuration with multiple options
print("=" * 60)
print("Example 1: Advanced Client Configuration")
print("=" * 60)

# Configure client with various options
client = Anthropic(
    # API key can be passed explicitly or via ANTHROPIC_API_KEY environment variable
    api_key=os.environ.get("ANTHROPIC_API_KEY"),

    # Custom base URL (useful for proxies or self-hosted instances)
    base_url="https://api.anthropic.com",

    # Custom timeout settings (in seconds)
    timeout=30.0,

    # Maximum number of retries for failed requests
    max_retries=3,

    # Custom default headers
    default_headers={
        "X-Custom-Header": "my-app/1.0",
        "User-Agent": "my-app/1.0"
    },

    # Enable strict response validation (catches API response format issues)
    _strict_response_validation=True,
)

print("✓ Client configured with custom settings")
print(f"  Base URL: {client.base_url}")
print(f"  Timeout: {client.timeout}")
print(f"  Max retries: {client.max_retries}")

# Example 2: Error handling and retry logic
print("\n" + "=" * 60)
print("Example 2: Error Handling and Retry Logic")
print("=" * 60)

def call_with_retry(
    client: Anthropic,
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0
) -> Message:
    """
    Call the API with exponential backoff retry logic.

    Args:
        client: Configured Anthropic client
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        backoff_factor: Multiplier for exponential backoff

    Returns:
        Message response from API

    Raises:
        APIError: After all retries exhausted
    """
    for attempt in range(max_retries):
        try:
            return client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": "Explain quantum computing in simple terms"
                    }
                ]
            )
        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise
            delay = initial_delay * (backoff_factor ** attempt)
            print(f"⚠ Rate limited. Retrying in {delay:.2f} seconds... (attempt {attempt + 1}/{max_retries})")
            import time
            time.sleep(delay)
        except BadRequestError as e:
            print(f"✗ Bad request error: {e}")
            raise
        except APIError as e:
            print(f"✗ API error: {e}")
            raise

    raise APIError("Max retries exceeded")

try:
    response = call_with_retry(client)
    print("✓ Successfully called API with retry logic")
except APIError as e:
    print(f"✗ Failed after retries: {e}")

# Example 3: Working with different message formats
print("\n" + "=" * 60)
print("Example 3: Working with Different Message Formats")
print("=" * 60)

# Text-only message
text_response = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=512,
    messages=[
        {
            "role": "user",
            "content": "Write a short poem about autumn"
        }
    ]
)

print("✓ Text response received")
print(f"  Response type: {type(text_response.content[0])}")
if isinstance(text_response.content[0], TextBlock):
    print(f"  Content preview: {text_response.content[0].text[:100]}...")

# Multi-modal message with system prompt
multi_response = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1024,
    system="You are a helpful assistant that responds in JSON format",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Generate a JSON object with 3 programming languages and their creators"
                }
            ]
        }
    ]
)

print("✓ Multi-modal response received")
print(f"  Response content: {multi_response.content}")

# Example 4: Streaming responses for real-time interaction
print("\n" + "=" * 60)
print("Example 4: Streaming Responses")
print("=" * 60)

stream_response = client.messages.stream(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Tell me a short story about a robot"
        }
    ]
)

print("✓ Streaming response started")
print("  Receiving chunks:")

with stream_response as stream:
    for event in stream:
        if event.type == "text":
            print(f"    {event.text}", end="", flush=True)
        elif event.type == "message_start":
            print(f"\n  Message started: {event.message}")
        elif event.type == "content_block_start":
            print(f"\n  Content block started: {event.content_block}")
        elif event.type == "content_block_stop":
            print(f"\n  Content block stopped")

print("\n✓ Stream completed")

# Example 5: Using tools and structured outputs
print("\n" + "=" * 60)
print("Example 5: Tools and Structured Outputs")
print("=" * 60)

# Define a simple tool
tools = [
    {
        "name": "get_weather",
        "description": "Get weather information for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and state, e.g., San Francisco, CA"
                }
            },
            "required": ["location"]
        }
    }
]

# Create a message with tool use
tool_response = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=512,
    tools=tools,
    messages=[
        {
            "role": "user",
            "content": "What's the weather in Paris?"
        }
    ]
)

print("✓ Tool response received")
print(f"  Response has {len(tool_response.content)} content blocks")
for i, block in enumerate(tool_response.content):
    print(f"    Block {i}: {type(block).__name__}")
    if isinstance(block, ToolUseBlock):
        print(f"      Tool name: {block.name}")
        print(f"      Tool input: {block.input}")

# Example 6: Working with different models
print("\n" + "=" * 60)
print("Example 6: Different Models")
print("=" * 60)

models = [
    "claude-3-5-sonnet-20240620",
    "claude-3-opus-20240229",
    "claude-3-haiku-20240307",
]

for model_name in models:
    try:
        model_response = client.messages.create(
            model=model_name,
            max_tokens=100,
            messages=[
                {
                    "role": "user",
                    "content": "Say hello"
                }
            ]
        )
        print(f"✓ Model {model_name}: Success")
    except Exception as e:
        print(f"✗ Model {model_name}: {e}")

# Example 7: Best practices - context management and cleanup
print("\n" + "=" * 60)
print("Example 7: Context Management and Cleanup")
print("=" * 60)

# The client manages its own HTTP connections
# For long-running applications, you can explicitly close the client
# In most cases, this happens automatically when the client goes out of scope

print("✓ Client automatically manages HTTP connections")
print("  For long-running apps, use context managers:")
print("    with Anthropic() as client:")
print("        # use client")
print("    # client automatically closed")

# Example 8: Logging and debugging
print("\n" + "=" * 60)
print("Example 8: Logging and Debugging")
print("=" * 60)

# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("anthropic").setLevel(logging.DEBUG)

print("✓ Debug logging enabled")
print("  Set ANTHROPIC_LOG=debug environment variable for detailed logs")

print("\n" + "=" * 60)
print("Advanced Usage Examples Complete!")
print("=" * 60)
print("\nKey takeaways:")
print("  • Configure client with custom settings for your environment")
print("  • Implement retry logic with exponential backoff")
print("  • Handle different response types (text, tools, streaming)")
print("  • Use appropriate models for your use case")
print("  • Enable logging for debugging")
print("  • Always validate API responses")