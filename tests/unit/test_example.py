"""Example unit test to demonstrate the testing infrastructure."""
import pytest
from unittest.mock import Mock, patch


class TestExample:
    """Example test class demonstrating various testing patterns."""
    
    def test_simple_assertion(self):
        """Basic test with simple assertion."""
        result = 2 + 2
        assert result == 4
    
    def test_with_fixture(self, mock_config):
        """Test using a fixture from conftest.py."""
        assert mock_config["app"]["name"] == "test_app"
        assert mock_config["discord"]["token"] == "test_token"
    
    def test_with_mock(self, mocker):
        """Test using pytest-mock for mocking."""
        # Create a mock function
        mock_func = mocker.Mock(return_value="mocked value")
        
        # Call the mock
        result = mock_func()
        
        # Verify
        assert result == "mocked value"
        mock_func.assert_called_once()
    
    @pytest.mark.unit
    def test_with_marker(self):
        """Test with custom marker."""
        assert True
    
    def test_exception_handling(self):
        """Test exception handling."""
        with pytest.raises(ValueError, match="Invalid value"):
            raise ValueError("Invalid value")
    
    def test_parametrized(self, temp_dir):
        """Test using temp_dir fixture."""
        # Create a test file
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        
        # Verify
        assert test_file.exists()
        assert test_file.read_text() == "test content"


@pytest.mark.parametrize("input_val,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
    (4, 8),
])
def test_parametrized_function(input_val, expected):
    """Example of parametrized testing."""
    result = input_val * 2
    assert result == expected


@pytest.mark.asyncio
async def test_async_function():
    """Example async test."""
    import asyncio
    
    async def async_operation():
        await asyncio.sleep(0.01)
        return "async result"
    
    result = await async_operation()
    assert result == "async result"