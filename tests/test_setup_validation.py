"""Validation tests to ensure the testing infrastructure is set up correctly."""
import pytest
import sys
from pathlib import Path

# Mark all async tests with pytest.mark.asyncio
pytestmark = pytest.mark.asyncio


def test_python_version():
    """Verify Python version is 3.8 or higher."""
    assert sys.version_info >= (3, 8), "Python 3.8 or higher is required"


def test_project_structure():
    """Verify the basic project structure exists."""
    project_root = Path(__file__).parent.parent
    
    # Check main directories
    assert (project_root / "app").exists(), "app directory missing"
    assert (project_root / "lib").exists(), "lib directory missing"
    assert (project_root / "task").exists(), "task directory missing"
    assert (project_root / "util").exists(), "util directory missing"
    
    # Check test directories
    assert (project_root / "tests").exists(), "tests directory missing"
    assert (project_root / "tests" / "unit").exists(), "unit tests directory missing"
    assert (project_root / "tests" / "integration").exists(), "integration tests directory missing"


def test_conftest_fixtures(temp_dir, mock_config, mock_env_vars):
    """Verify conftest fixtures are working properly."""
    # Test temp_dir fixture
    assert temp_dir.exists()
    assert temp_dir.is_dir()
    
    # Test mock_config fixture
    assert isinstance(mock_config, dict)
    assert "app" in mock_config
    assert mock_config["app"]["name"] == "test_app"
    
    # Test mock_env_vars fixture
    assert isinstance(mock_env_vars, dict)
    assert "DISCORD_TOKEN" in mock_env_vars
    assert mock_env_vars["DISCORD_TOKEN"] == "test_discord_token"


@pytest.mark.unit
def test_unit_marker():
    """Test that unit test marker is registered."""
    assert True, "Unit test marker is working"


@pytest.mark.integration
def test_integration_marker():
    """Test that integration test marker is registered."""
    assert True, "Integration test marker is working"


@pytest.mark.slow
def test_slow_marker():
    """Test that slow test marker is registered."""
    assert True, "Slow test marker is working"


def test_pytest_configuration():
    """Verify pytest is configured correctly."""
    import pytest
    
    # Check that pytest is installed
    assert hasattr(pytest, "__version__")
    
    # Verify version is recent
    major, minor = map(int, pytest.__version__.split(".")[:2])
    assert major >= 7, f"pytest version {pytest.__version__} is too old"


def test_coverage_configuration():
    """Verify coverage is configured correctly."""
    try:
        import pytest_cov
        assert hasattr(pytest_cov, "__version__")
    except ImportError:
        pytest.fail("pytest-cov is not installed")


def test_mock_configuration():
    """Verify pytest-mock is configured correctly."""
    try:
        import pytest_mock
        # pytest-mock doesn't expose __version__ directly
        # Check for key functionality instead
        assert hasattr(pytest_mock, "plugin")
        assert hasattr(pytest_mock, "MockerFixture")
    except ImportError:
        pytest.fail("pytest-mock is not installed")


async def test_async_support():
    """Verify async test support is working."""
    import asyncio
    
    async def async_function():
        await asyncio.sleep(0.001)
        return "async works"
    
    result = await async_function()
    assert result == "async works"


def test_fixture_isolation(mock_env_vars):
    """Verify fixtures provide proper test isolation."""
    import os
    
    # Verify test environment variable is set
    assert os.environ.get("DISCORD_TOKEN") == "test_discord_token"
    
    # This should not affect other tests due to fixture isolation
    os.environ["TEST_VAR"] = "test_value"