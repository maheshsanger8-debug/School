"""Test configuration and fixtures."""

import pytest
import asyncio
from app.agent.runtime import AgentRuntime
from app.tools import ToolRegistry
from app.agent.state import AgentState
from app.agent.context import ExecutionContext


@pytest.fixture
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def agent_runtime():
    """Create agent runtime instance."""
    return AgentRuntime()


@pytest.fixture
def tool_registry():
    """Create tool registry instance."""
    return ToolRegistry()


@pytest.fixture
def agent_state():
    """Create agent state instance."""
    return AgentState(
        session_id="test-session",
        execution_id="test-execution",
        main_goal="Test goal"
    )


@pytest.fixture
def execution_context():
    """Create execution context instance."""
    return ExecutionContext(
        session_id="test-session",
        execution_id="test-execution"
    )
