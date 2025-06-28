"""Shared pytest fixtures for testing."""
import os
import tempfile
from pathlib import Path
from typing import Generator, Dict, Any
import pytest
from unittest.mock import Mock, MagicMock


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for testing.
    
    Yields:
        Path: Path to the temporary directory
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_env_vars(monkeypatch) -> Dict[str, str]:
    """Mock environment variables for testing.
    
    Returns:
        Dict[str, str]: Dictionary of test environment variables
    """
    test_env = {
        "DISCORD_TOKEN": "test_discord_token",
        "API_KEY": "test_api_key",
        "DEBUG": "true",
        "LOG_LEVEL": "DEBUG",
        "PORT": "8000",
    }
    
    for key, value in test_env.items():
        monkeypatch.setenv(key, value)
    
    return test_env


@pytest.fixture
def mock_config() -> Dict[str, Any]:
    """Provide mock configuration for testing.
    
    Returns:
        Dict[str, Any]: Test configuration dictionary
    """
    return {
        "app": {
            "name": "test_app",
            "version": "0.1.0",
            "debug": True,
        },
        "discord": {
            "token": "test_token",
            "guild_id": "123456789",
            "channel_id": "987654321",
        },
        "api": {
            "base_url": "http://localhost:8000",
            "timeout": 30,
            "retry_attempts": 3,
        },
    }


@pytest.fixture
def mock_discord_client():
    """Create a mock Discord client for testing.
    
    Returns:
        Mock: Mocked Discord client
    """
    client = MagicMock()
    client.user = MagicMock()
    client.user.id = 123456789
    client.user.name = "TestBot"
    client.is_ready.return_value = True
    return client


@pytest.fixture
def mock_fastapi_client():
    """Create a mock FastAPI test client.
    
    Returns:
        Mock: Mocked FastAPI test client
    """
    client = MagicMock()
    client.base_url = "http://testserver"
    return client


@pytest.fixture
def sample_discord_message():
    """Create a sample Discord message for testing.
    
    Returns:
        Dict[str, Any]: Sample Discord message data
    """
    return {
        "id": "1234567890",
        "content": "Test message content",
        "author": {
            "id": "987654321",
            "username": "testuser",
            "discriminator": "1234",
        },
        "channel_id": "111222333",
        "guild_id": "444555666",
        "timestamp": "2023-01-01T00:00:00.000Z",
    }


@pytest.fixture
def sample_api_response():
    """Create a sample API response for testing.
    
    Returns:
        Dict[str, Any]: Sample API response data
    """
    return {
        "status": "success",
        "data": {
            "id": "response_123",
            "result": "Test result",
            "metadata": {
                "timestamp": "2023-01-01T00:00:00.000Z",
                "version": "1.0.0",
            },
        },
        "error": None,
    }


@pytest.fixture(autouse=True)
def reset_environment(monkeypatch):
    """Reset environment variables before each test.
    
    This fixture runs automatically before each test to ensure
    a clean environment state.
    """
    # Clear any existing environment variables that might interfere
    env_vars_to_clear = [
        "DISCORD_TOKEN",
        "API_KEY",
        "DATABASE_URL",
        "REDIS_URL",
    ]
    
    for var in env_vars_to_clear:
        monkeypatch.delenv(var, raising=False)


@pytest.fixture
def mock_async_context():
    """Provide a mock async context manager.
    
    Useful for testing async context managers without actual I/O.
    """
    class MockAsyncContext:
        async def __aenter__(self):
            return self
        
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass
    
    return MockAsyncContext()


@pytest.fixture
def capture_logs(caplog):
    """Capture and provide access to log messages during tests.
    
    Returns:
        caplog: Pytest caplog fixture configured for the test
    """
    caplog.set_level("DEBUG")
    return caplog