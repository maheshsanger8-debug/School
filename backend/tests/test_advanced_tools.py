"""Tests for tools integration."""

import pytest
from app.tools.file_reader import FileReaderTool
from app.tools.api_caller import APICallerTool
from app.tools.web_search import WebSearchTool
import tempfile
from pathlib import Path


@pytest.mark.asyncio
async def test_file_reader_read_file():
    """Test file reader with valid file."""
    tool = FileReaderTool()
    
    # Create temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Test content")
        temp_path = f.name
    
    try:
        result = await tool.execute(file_path=temp_path)
        assert result.success
        assert "Test content" in result.data
    finally:
        Path(temp_path).unlink()


@pytest.mark.asyncio
async def test_file_reader_nonexistent_file():
    """Test file reader with nonexistent file."""
    tool = FileReaderTool()
    result = await tool.execute(file_path="/nonexistent/file.txt")
    
    assert not result.success
    assert "not found" in result.error.lower()


@pytest.mark.asyncio
async def test_api_caller_get_request():
    """Test API caller with GET request."""
    tool = APICallerTool()
    # Using a public API that returns JSON
    result = await tool.execute(
        url="https://api.github.com/users/github",
        method="GET"
    )
    
    assert result.success or result.data is not None


@pytest.mark.asyncio
async def test_api_caller_invalid_url():
    """Test API caller with invalid URL."""
    tool = APICallerTool()
    result = await tool.execute(url="not-a-url")
    
    assert not result.success
    assert "http" in result.error.lower()


@pytest.mark.asyncio
async def test_web_search_query():
    """Test web search tool."""
    tool = WebSearchTool()
    result = await tool.execute(query="python programming")
    
    # Should return something even if empty results
    assert result.success
    assert "results" in result.data


@pytest.mark.asyncio
async def test_web_search_empty_query():
    """Test web search with empty query."""
    tool = WebSearchTool()
    result = await tool.execute(query="")
    
    assert not result.success
    assert "empty" in result.error.lower()
