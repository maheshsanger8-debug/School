"""Tests for agent state."""

import pytest
from app.agent.state import AgentState


def test_agent_state_creation():
    """Test agent state creation."""
    state = AgentState(
        session_id="test-session",
        execution_id="test-exec",
        main_goal="Test goal"
    )
    
    assert state.session_id == "test-session"
    assert state.main_goal == "Test goal"
    assert state.status == "running"
    assert state.current_step == 0


def test_agent_state_add_thought():
    """Test adding thoughts to state."""
    state = AgentState(
        session_id="test",
        execution_id="test",
        main_goal="goal"
    )
    
    state.add_thought("First thought")
    state.add_thought("Second thought")
    
    assert len(state.thoughts) == 2
    assert state.thoughts[0] == "First thought"


def test_agent_state_add_action():
    """Test adding actions to state."""
    state = AgentState(
        session_id="test",
        execution_id="test",
        main_goal="goal"
    )
    
    action = {"tool": "calculator", "params": {"expression": "2+2"}}
    state.add_action(action)
    
    assert len(state.actions) == 1
    assert "calculator" in state.tools_used


def test_agent_state_complete():
    """Test completing agent state."""
    state = AgentState(
        session_id="test",
        execution_id="test",
        main_goal="goal"
    )
    
    state.complete("Final answer")
    
    assert state.status == "completed"
    assert state.final_answer == "Final answer"


def test_agent_state_fail():
    """Test failing agent state."""
    state = AgentState(
        session_id="test",
        execution_id="test",
        main_goal="goal"
    )
    
    state.fail("Error occurred")
    
    assert state.status == "failed"
    assert state.error == "Error occurred"


def test_agent_state_to_dict():
    """Test converting state to dictionary."""
    state = AgentState(
        session_id="test",
        execution_id="test",
        main_goal="goal"
    )
    
    state.add_thought("A thought")
    state.complete("Done")
    
    state_dict = state.to_dict()
    
    assert state_dict["session_id"] == "test"
    assert state_dict["status"] == "completed"
    assert len(state_dict["thoughts"]) == 1
