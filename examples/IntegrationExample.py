# Integration examples for the Anthropic SDK
# Shows how to integrate the SDK with dependency injection patterns and application frameworks

import os
from typing import Optional, Protocol
from dataclasses import dataclass
from anthropic import Anthropic, AsyncAnthropic
from anthropic.types import Message

# Example 1: Service Interface Pattern (similar to ASP.NET Core services)
print("=" * 60)
print("Example 1: Service Interface Pattern")
print("=" * 60)

class AIService(Protocol):
    """Protocol defining the AI service interface"""

    def generate_response(self, prompt: str, max_tokens: int = 1024) -> str:
        """Generate a response from the AI model"""
        ...

    async def generate_response_async(self, prompt: str, max_tokens: int = 1024) -> str:
        """Generate a response asynchronously"""
        ...

@dataclass
class AIServiceConfig:
    """Configuration for the AI service"""
    api_key: Optional[str] = None
    model: str = "claude-3-5-sonnet-20240620"
    max_tokens: int = 1024
    timeout: float = 30.0
    max_retries: int = 3

class AnthropicAIService:
    """Concrete implementation of AIService using Anthropic SDK"""

    def __init__(self, config: AIServiceConfig):
        self.config = config
        self._client: Optional[Anthropic] = None
        self._async_client: Optional[AsyncAnthropic] = None

    @property
    def client(self) -> Anthropic:
        """Lazy initialization of synchronous client"""
        if self._client is None:
            self._client = Anthropic(
                api_key=self.config.api_key or os.environ.get("ANTHROPIC_API_KEY"),
                model=self.config.model,
                timeout=self.config.timeout,
                max_retries=self.config.max_retries,
            )
        return self._client

    @property
    def async_client(self) -> AsyncAnthropic:
        """Lazy initialization of asynchronous client"""
        if self._async_client is None:
            self._async_client = AsyncAnthropic(
                api_key=self.config.api_key or os.environ.get("ANTHROPIC_API_KEY"),
                model=self.config.model,
                timeout=self.config.timeout,
                max_retries=self.config.max_retries,
            )
        return self._async_client

    def generate_response(self, prompt: str, max_tokens: Optional[int] = None) -> str:
        """Generate a response from the AI model"""
        try:
            response = self.client.messages.create(
                model=self.config.model,
                max_tokens=max_tokens or self.config.max_tokens,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            # Extract text content from response
            text_content = ""
            for block in response.content:
                if hasattr(block, 'text'):
                    text_content += block.text
            return text_content.strip()
        except Exception as e:
            return f"Error generating response: {str(e)}"

    async def generate_response_async(self, prompt: str, max_tokens: Optional[int] = None) -> str:
        """Generate a response asynchronously"""
        try:
            response = await self.async_client.messages.create(
                model=self.config.model,
                max_tokens=max_tokens or self.config.max_tokens,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            # Extract text content from response
            text_content = ""
            for block in response.content:
                if hasattr(block, 'text'):
                    text_content += block.text
            return text_content.strip()
        except Exception as e:
            return f"Error generating response: {str(e)}"

# Usage example
config = AIServiceConfig(
    model="claude-3-5-sonnet-20240620",
    max_tokens=512,
    timeout=25.0
)

ai_service = AnthropicAIService(config)

# Synchronous usage
response = ai_service.generate_response("What is the capital of France?")
print("✓ Synchronous response:")
print(f"  {response}")

# Example 2: Factory Pattern for Client Creation
print("\n" + "=" * 60)
print("Example 2: Factory Pattern")
print("=" * 60)

class AnthropicClientFactory:
    """Factory for creating configured Anthropic clients"""

    @staticmethod
    def create_development_client() -> Anthropic:
        """Create a client configured for development"""
        return Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY"),
            base_url="https://api.anthropic.com",
            timeout=10.0,  # Shorter timeout for dev
            max_retries=2,
            default_headers={
                "X-Environment": "development",
                "X-Client-Version": "1.0.0-dev"
            }
        )

    @staticmethod
    def create_production_client() -> Anthropic:
        """Create a client configured for production"""
        return Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY"),
            timeout=30.0,
            max_retries=3,
            _strict_response_validation=True,
            default_headers={
                "X-Environment": "production",
                "X-Client-Version": "1.0.0"
            }
        )

    @staticmethod
    def create_testing_client() -> Anthropic:
        """Create a client configured for testing"""
        return Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY", "test-key"),
            base_url="https://api.anthropic.com",
            timeout=5.0,
            max_retries=1,
            default_headers={
                "X-Environment": "testing"
            }
        )

# Create clients for different environments
dev_client = AnthropicClientFactory.create_development_client()
prod_client = AnthropicClientFactory.create_production_client()
test_client = AnthropicClientFactory.create_testing_client()

print("✓ Created clients for different environments:")
print(f"  Development client timeout: {dev_client.timeout}")
print(f"  Production client timeout: {prod_client.timeout}")
print(f"  Testing client timeout: {test_client.timeout}")

# Example 3: Singleton Pattern (for applications needing a single client instance)
print("\n" + "=" * 60)
print("Example 3: Singleton Pattern")
print("=" * 60)

class AnthropicClientSingleton:
    """Singleton wrapper for Anthropic client"""

    _instance: Optional[Anthropic] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._client = Anthropic(
                api_key=os.environ.get("ANTHROPIC_API_KEY"),
                timeout=30.0,
                max_retries=3
            )
            self._initialized = True

    @property
    def client(self) -> Anthropic:
        return self._client

# Usage
singleton1 = AnthropicClientSingleton()
singleton2 = AnthropicClientSingleton()

print("✓ Singleton pattern verified:")
print(f"  Same instance: {singleton1 is singleton2}")
print(f"  Client configured: {singleton1.client is not None}")

# Example 4: Dependency Injection Container Pattern
print("\n" + "=" * 60)
print("Example 4: Dependency Injection Container Pattern")
print("=" * 60)

class ServiceContainer:
    """Simple dependency injection container"""

    def __init__(self):
        self._services = {}
        self._singletons = {}

    def register_singleton(self, interface: type, implementation: type):
        """Register a singleton service"""
        self._singletons[interface] = implementation

    def register_transient(self, interface: type, implementation: type):
        """Register a transient service"""
        self._services[interface] = implementation

    def resolve(self, interface: type):
        """Resolve a service instance"""
        # Check singletons first
        if interface in self._singletons:
            if interface not in self._services:  # Not yet instantiated
                self._services[interface] = self._singletons[interface]()
            return self._services[interface]

        # Check transients
        if interface in self._services:
            return self._services[interface]()

        raise ValueError(f"No registration found for {interface}")

# Register services
container = ServiceContainer()

# Register configuration
container.register_singleton(AIServiceConfig, lambda: AIServiceConfig(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
    model="claude-3-5-sonnet-20240620",
    max_tokens=1024
))

# Register AI service
container.register_singleton(AIService, AnthropicAIService)

# Resolve and use service
resolved_config: AIServiceConfig = container.resolve(AIServiceConfig)
resolved_service: AIService = container.resolve(AIService)

print("✓ Dependency injection container:")
print(f"  Resolved config model: {resolved_config.model}")
print(f"  Resolved service type: {type(resolved_service).__name__}")

# Use the resolved service
di_response = resolved_service.generate_response("Explain dependency injection in one sentence")
print(f"  DI service response: {di_response}")

# Example 5: Middleware/Interceptor Pattern
print("\n" + "=" * 60)
print("Example 5: Middleware/Interceptor Pattern")
print("=" * 60)

class LoggingMiddleware:
    """Middleware for logging API calls"""

    def __init__(self, client: Anthropic):
        self._client = client
        self.call_count = 0

    def messages_create(self, **kwargs):
        """Intercept messages.create calls"""
        self.call_count += 1
        print(f"📞 API Call #{self.call_count}: {kwargs.get('model', 'unknown')}")

        # Log request details (be careful with sensitive data in production)
        if 'messages' in kwargs:
            user_messages = [msg for msg in kwargs['messages'] if msg.get('role') == 'user']
            if user_messages:
                content_preview = str(user_messages[0].get('content', ''))[:50]
                print(f"   Preview: {content_preview}...")

        try:
            response = self._client.messages.create(**kwargs)
            print(f"   ✓ Success: {len(response.content)} content blocks")
            return response
        except Exception as e:
            print(f"   ✗ Error: {type(e).__name__}: {e}")
            raise

# Wrap client with middleware
wrapped_client = LoggingMiddleware(Anthropic())

print("✓ Middleware wrapper created")
print("  Making a test call through middleware:")

try:
    wrapped_response = wrapped_client.messages_create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=100,
        messages=[{"role": "user", "content": "Hello"}]
    )
    print(f"  Final response received: {wrapped_response.content[0].text[:30]}...")
except Exception as e:
    print(f"  Call failed: {e}")

# Example 6: Configuration from Multiple Sources
print("\n" + "=" * 60)
print("Example 6: Configuration from Multiple Sources")
print("=" * 60)

def load_config_from_multiple_sources() -> dict:
    """Load configuration from multiple sources with precedence"""
    config = {}

    # 1. Default values
    config.update({
        "model": "claude-3-5-sonnet-20240620",
        "max_tokens": 1024,
        "timeout": 30.0,
        "max_retries": 3
    })

    # 2. Environment variables (override defaults)
    env_mapping = {
        "ANTHROPIC_MODEL": "model",
        "ANTHROPIC_MAX_TOKENS": "max_tokens",
        "ANTHROPIC_TIMEOUT": "timeout",
        "ANTHROPIC_MAX_RETRIES": "max_retries"
    }

    for env_var, config_key in env_mapping.items():
        value = os.environ.get(env_var)
        if value is not None:
            # Try to convert to appropriate type
            if config_key in ["max_tokens", "max_retries"]:
                try:
                    config[config_key] = int(value)
                except ValueError:
                    pass  # Keep default
            elif config_key == "timeout":
                try:
                    config[config_key] = float(value)
                except ValueError:
                    pass  # Keep default
            else:
                config[config_key] = value

    # 3. Application-specific config (would come from file/database in real app)
    app_config = {
        "model": "claude-3-5-sonnet-20240620",  # Override from app config
        "custom_feature_flag": True
    }
    config.update(app_config)

    return config

final_config = load_config_from_multiple_sources()
print("✓ Configuration loaded from multiple sources:")
for key, value in final_config.items():
    print(f"  {key}: {value}")

# Create client with final configuration
configured_client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
    **{k: v for k, v in final_config.items()
       if k in ["model", "max_tokens", "timeout", "max_retries"]}
)

print(f"✓ Client created with final configuration:")
print(f"  Model: {configured_client.model}")
print(f"  Max tokens: {configured_client.max_tokens}")

print("\n" + "=" * 60)
print("Integration Examples Complete!")
print("=" * 60)
print("\nPatterns demonstrated:")
print("  • Service Interface Pattern - Define contracts for AI services")
print("  • Factory Pattern - Create environment-specific clients")
print("  • Singleton Pattern - Ensure single client instance")
print("  • Dependency Injection - Decouple configuration from usage")
print("  • Middleware Pattern - Add cross-cutting concerns (logging)")
print("  • Configuration Composition - Load from multiple sources")
print("\nThese patterns make the SDK easy to integrate into:")
print("  • ASP.NET Core applications")
print("  • Spring Boot applications")
print("  • Any application using DI containers")
print("  • Microservices architectures")
print("  • Testable and maintainable codebases")