class AnthropicSdkPythonException(Exception):
    """Base exception for all errors in this SDK."""
    pass

class ConfigurationException(AnthropicSdkPythonException):
    """Errors related to SDK configuration."""
    pass

class ValidationException(AnthropicSdkPythonException):
    """Errors related to input or data validation."""
    pass
