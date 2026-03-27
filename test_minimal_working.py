# test_minimal_working.py
import pytest
import asyncio

def test_simple_math():
    """A simple test that should always pass"""
    assert 1 + 1 == 2
    print("✅ Simple math test passed")


@pytest.mark.asyncio
async def test_simple_async():
    """A simple async test"""
    await asyncio.sleep(0.1)
    result = "success"
    assert result == "success"
    print("✅ Simple async test passed")


class TestClass:
    def test_method(self):
        assert "hello".upper() == "HELLO"
        print("✅ Class method test passed")