"""Tests for tools."""

import pytest
from app.tools.calculator import CalculatorTool
from app.tools import get_tool_registry


@pytest.mark.asyncio
async def test_calculator_tool_simple_math():
    """Test calculator with simple math."""
    tool = CalculatorTool()
    result = await tool.execute(expression="2 + 2")
    
    assert result.success
    assert result.data == 4


@pytest.mark.asyncio
async def test_calculator_tool_complex_math():
    """Test calculator with complex math."""
    tool = CalculatorTool()
    result = await tool.execute(expression="(10 * 5) + 3")
    
    assert result.success
    assert result.data == 53


@pytest.mark.asyncio
async def test_calculator_tool_division():
    """Test calculator division."""
    tool = CalculatorTool()
    result = await tool.execute(expression="10 / 2")
    
    assert result.success
    assert result.data == 5.0


@pytest.mark.asyncio
async def test_calculator_tool_division_by_zero():
    """Test calculator with division by zero."""
    tool = CalculatorTool()
    result = await tool.execute(expression="10 / 0")
    
    assert not result.success
    assert "Division by zero" in result.error


@pytest.mark.asyncio
async def test_calculator_tool_invalid_expression():
    """Test calculator with invalid expression."""
    tool = CalculatorTool()
    result = await tool.execute(expression="__import__('os').system('ls')")
    
    assert not result.success
    assert "unsafe" in result.error.lower()


def test_tool_registry():
    """Test tool registry."""
    registry = get_tool_registry()
    
    tools = registry.list_tools()
    assert "calculator" in tools


def test_tool_registry_get_tool():
    """Test getting tool from registry."""
    registry = get_tool_registry()
    tool = registry.get("calculator")
    
    assert tool is not None
    assert tool.name == "calculator"


def test_tool_schemas():
    """Test getting tool schemas."""
    registry = get_tool_registry()
    schemas = registry.get_schemas()
    
    assert len(schemas) > 0
    assert any(s["name"] == "calculator" for s in schemas)
