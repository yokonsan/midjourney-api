"""Example integration test to demonstrate testing infrastructure."""
import pytest
from unittest.mock import AsyncMock, patch


@pytest.mark.integration
class TestIntegrationExample:
    """Example integration test class."""
    
    def test_integration_with_mocked_external_service(self, mock_discord_client):
        """Test simulating integration with Discord client."""
        # Use the mocked Discord client
        assert mock_discord_client.user.name == "TestBot"
        assert mock_discord_client.is_ready() is True
        
        # Simulate sending a message
        mock_discord_client.send_message = AsyncMock(return_value={"id": "123", "content": "Test"})
    
    @pytest.mark.asyncio
    async def test_async_integration(self, mock_async_context):
        """Test async integration scenario."""
        async with mock_async_context as ctx:
            # Simulate async operations
            assert ctx is not None
    
    def test_with_environment_variables(self, mock_env_vars):
        """Test integration with environment variables."""
        import os
        
        # Verify environment variables are set
        assert os.environ.get("DISCORD_TOKEN") == "test_discord_token"
        assert os.environ.get("API_KEY") == "test_api_key"
        assert os.environ.get("PORT") == "8000"
    
    @pytest.mark.slow
    def test_slow_integration(self):
        """Example of a slow test that might be skipped in quick runs."""
        import time
        
        # Simulate a slow operation
        start = time.time()
        time.sleep(0.1)  # Simulate slow operation
        duration = time.time() - start
        
        assert duration >= 0.1