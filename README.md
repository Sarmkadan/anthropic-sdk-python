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

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
