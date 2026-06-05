"""Tests for agent runtime."""

import pytest
from app.agent.runtime import AgentRuntime


@pytest.mark.asyncio
async def test_agent_execution(agent_runtime: AgentRuntime):
    """Test basic agent execution."""
    result = await agent_runtime.execute(
        goal="Test execution",
        max_iterations=1
    )
    
    assert result["status"] in ["completed", "failed"]
    assert "execution_id" in result
    assert "session_id" in result
    assert "execution_time_seconds" in result


@pytest.mark.asyncio
async def test_agent_execution_with_session_id():
    """Test agent execution with custom session ID."""
    runtime = AgentRuntime()
    session_id = "custom-session-123"
    
    result = await runtime.execute(
        goal="Test with session",
        session_id=session_id,
        max_iterations=1
    )
    
    assert result["session_id"] == session_id


@pytest.mark.asyncio
async def test_agent_execution_timeout():
    """Test agent execution with timeout."""
    runtime = AgentRuntime()
    
    result = await runtime.execute(
        goal="Long running task",
        timeout_seconds=1,
        max_iterations=100
    )
    
    # Should complete or timeout gracefully
    assert "status" in result
    assert "execution_id" in result


def test_get_execution_state(agent_runtime: AgentRuntime, agent_state):
    """Test getting execution state."""
    execution_id = agent_state.execution_id
    agent_runtime.active_executions[execution_id] = agent_state
    
    state = agent_runtime.get_execution_state(execution_id)
    
    assert state is not None
    assert state["execution_id"] == execution_id


def test_get_nonexistent_execution_state(agent_runtime: AgentRuntime):
    """Test getting nonexistent execution state."""
    state = agent_runtime.get_execution_state("nonexistent")
    assert state is None
