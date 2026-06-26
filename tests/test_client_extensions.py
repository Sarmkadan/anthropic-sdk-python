import pytest
import httpx
from anthropic import Anthropic, NotFoundError

base_url = "http://127.0.0.1:4010"
api_key = "my-anthropic-api-key"

def test_client_initialization_missing_key():
    # Verify that without credentials it raises TypeError
    with pytest.raises(TypeError, match="Could not resolve authentication method"):
        Anthropic(base_url=base_url, api_key=None, credentials=None)

def test_client_custom_timeout():
    timeout = httpx.Timeout(5.0)
    client = Anthropic(base_url=base_url, api_key=api_key, timeout=timeout)
    assert client.timeout == timeout
    client.close()

def test_client_base_url_override():
    custom_url = "https://custom.anthropic.com/"
    # The client adds a trailing slash to base_url if not present,
    # but the assertion in test_client.py showed the client.base_url
    # property includes it.
    client = Anthropic(base_url=custom_url, api_key=api_key)
    assert client.base_url == f"{custom_url.rstrip('/')}/"
    client.close()

def test_client_default_headers_merging():
    client = Anthropic(base_url=base_url, api_key=api_key, default_headers={"X-Test": "Value"})
    assert client.default_headers["X-Test"] == "Value"
    assert "anthropic-version" in client.default_headers
    client.close()

def test_client_with_options_copy():
    client = Anthropic(base_url=base_url, api_key=api_key, max_retries=2)
    copied = client.with_options(max_retries=5)
    assert copied.max_retries == 5
    assert client.max_retries == 2
    client.close()

@pytest.mark.respx(base_url=base_url)
def test_error_handling_404(respx_mock):
    respx_mock.get("/v1/models/invalid").mock(return_value=httpx.Response(404, json={"error": "Not Found"}))
    client = Anthropic(base_url=base_url, api_key=api_key)
    with pytest.raises(NotFoundError):
        client.get("/v1/models/invalid", cast_to=httpx.Response)
    client.close()
