# Basic usage example
import os
from anthropic import Anthropic

# Initialize the client. The client will automatically look for the
# ANTHROPIC_API_KEY environment variable.
client = Anthropic()

# Create a simple completion
message = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, world!"}
    ]
)

print(message.content)
