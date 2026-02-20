# conftest.py
import sys
import pytest
from unittest.mock import MagicMock, AsyncMock
from typing import Any, Dict

# Create mock MCP module before any imports
class MockMCPClient:
    def __init__(self, server_name: str):
        self.server_name = server_name
        
    async def connect(self) -> bool:
        return True
        
    async def execute_query(self, query: str) -> Dict[str, Any]:
        return {"result": "mock data", "status": "success"}
        
    async def close(self) -> None:
        pass

# Create the mock mcp module
mock_mcp_module = MagicMock()
mock_mcp_module.MCPClient = MockMCPClient

# Insert the mock before any other imports
sys.modules['mcp'] = mock_mcp_module

# Also handle potential submodules
sys.modules['mcp.client'] = MagicMock()
sys.modules['mcp.client'].MCPClient = MockMCPClient

# Now we can import the real modules
pytest_plugins = ['pytest_asyncio']


@pytest.fixture
def mock_mcp_client():
    """Fixture to provide a mock MCP client"""
    return MockMCPClient("test_server")


@pytest.fixture(autouse=True)
def setup_test_env():
    """Setup test environment before each test"""
    # Any common setup code
    yield
    # Any common teardown code
