"""Tests for execution context."""

import pytest
from app.agent.context import ExecutionContext


def test_execution_context_creation():
    """Test execution context creation."""
    context = ExecutionContext(
        session_id="test",
        execution_id="test"
    )
    
    assert context.session_id == "test"
    assert context.execution_id == "test"
    assert context.available_tools == []


def test_add_tool():
    """Test adding tool to context."""
    context = ExecutionContext(
        session_id="test",
        execution_id="test"
    )
    
    context.add_tool("calculator")
    context.add_tool("file_reader")
    
    assert "calculator" in context.available_tools
    assert "file_reader" in context.available_tools


def test_add_duplicate_tool():
    """Test adding duplicate tool."""
    context = ExecutionContext(
        session_id="test",
        execution_id="test"
    )
    
    context.add_tool("calculator")
    context.add_tool("calculator")
    
    assert context.available_tools.count("calculator") == 1


def test_set_preference():
    """Test setting user preference."""
    context = ExecutionContext(
        session_id="test",
        execution_id="test"
    )
    
    context.set_preference("language", "en")
    context.set_preference("verbose", True)
    
    assert context.user_preferences["language"] == "en"
    assert context.user_preferences["verbose"] is True


def test_add_message():
    """Test adding message to context."""
    context = ExecutionContext(
        session_id="test",
        execution_id="test"
    )
    
    context.add_message("user", "Hello")
    context.add_message("assistant", "Hi there!")
    
    assert len(context.conversation_history) == 2
    assert context.conversation_history[0]["role"] == "user"
    assert context.conversation_history[0]["content"] == "Hello"


def test_get_messages():
    """Test getting conversation history."""
    context = ExecutionContext(
        session_id="test",
        execution_id="test"
    )
    
    for i in range(5):
        context.add_message("user", f"Message {i}")
    
    # Get last 3 messages
    recent = context.get_messages(limit=3)
    assert len(recent) == 3
    assert recent[0]["content"] == "Message 2"


def test_context_to_dict():
    """Test converting context to dictionary."""
    context = ExecutionContext(
        session_id="test",
        execution_id="test"
    )
    
    context.add_tool("calculator")
    context.set_preference("lang", "en")
    
    context_dict = context.to_dict()
    
    assert context_dict["session_id"] == "test"
    assert "calculator" in context_dict["available_tools"]
    assert context_dict["user_preferences"]["lang"] == "en"
