"""Tests for reasoning modules."""

import pytest
from app.reasoning.planner import PlanningAgent, TaskType
from app.reasoning.reflection import Reflection


# Planning Agent Tests
def test_planning_agent_decompose():
    """Test goal decomposition."""
    agent = PlanningAgent()
    plan = agent.decompose("Calculate 2+2")
    
    assert "goal" in plan
    assert "tasks" in plan
    assert len(plan["tasks"]) > 0


def test_planning_agent_add_task():
    """Test adding task to plan."""
    agent = PlanningAgent()
    task_id = agent.add_task(
        title="Test Task",
        description="Test description",
        task_type=TaskType.ANALYSIS,
        priority=1
    )
    
    assert task_id is not None
    assert task_id in agent.tasks


def test_planning_agent_task_completion():
    """Test marking task as complete."""
    agent = PlanningAgent()
    task_id = agent.add_task(
        title="Test Task",
        description="Test",
        task_type=TaskType.ANALYSIS
    )
    
    success = agent.mark_complete(task_id, result="Done")
    assert success is True
    assert agent.tasks[task_id].completed is True


def test_planning_agent_get_pending_tasks():
    """Test getting pending tasks."""
    agent = PlanningAgent()
    
    task1 = agent.add_task("Task 1", "Desc", TaskType.ANALYSIS)
    task2 = agent.add_task("Task 2", "Desc", TaskType.ANALYSIS)
    
    agent.mark_complete(task1)
    
    pending = agent.get_pending_tasks()
    assert len(pending) == 1
    assert pending[0].id == task2


def test_planning_agent_plan_status():
    """Test plan status."""
    agent = PlanningAgent()
    
    task1 = agent.add_task("Task 1", "Desc", TaskType.ANALYSIS)
    task2 = agent.add_task("Task 2", "Desc", TaskType.ANALYSIS)
    
    agent.mark_complete(task1)
    
    status = agent.get_plan_status()
    assert status["total_tasks"] == 2
    assert status["completed"] == 1
    assert status["pending"] == 1


# Reflection Tests
def test_reflection_reflect():
    """Test reflection mechanism."""
    reflection = Reflection()
    
    result = reflection.reflect(
        execution_id="exec-1",
        success=True,
        observations=["Observation 1", "Observation 2"],
        lessons=["Lesson 1"]
    )
    
    assert result["success"] is True
    assert len(result["observations"]) == 2


def test_reflection_insights():
    """Test getting insights from reflections."""
    reflection = Reflection()
    
    reflection.reflect(
        execution_id="exec-1",
        success=True,
        observations=["Obs 1"],
        lessons=["Lesson 1"]
    )
    
    reflection.reflect(
        execution_id="exec-2",
        success=False,
        observations=["Obs 2"],
        lessons=["Lesson 2"]
    )
    
    insights = reflection.get_insights()
    assert insights["total_reflections"] == 2
    assert "success_rate" in insights
    assert "average_effectiveness" in insights


def test_reflection_common_observations():
    """Test getting common observations."""
    reflection = Reflection()
    
    reflection.reflect(
        execution_id="exec-1",
        success=True,
        observations=["Common", "Obs1"],
    )
    
    reflection.reflect(
        execution_id="exec-2",
        success=True,
        observations=["Common", "Obs2"],
    )
    
    insights = reflection.get_insights()
    assert "Common" in insights["common_observations"]
