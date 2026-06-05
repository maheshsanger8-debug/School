"""Tests for multi-agent system."""

import pytest
from app.agent.multi_agent import (
    AgentPool,
    TaskQueue,
    AgentRole,
    TaskStatus,
    get_agent_pool,
    get_task_queue
)
from app.agent.coordinator import AgentCoordinator, get_agent_coordinator
from app.agent.specialized_agents import ResearchAgent, AnalysisAgent, ExecutionAgent
from app.agent.communication import MessageBroker, MessageType, get_message_broker


# Agent Pool Tests
def test_agent_pool_register():
    """Test registering agent in pool."""
    pool = AgentPool()
    
    agent_id = pool.register_agent(
        role=AgentRole.RESEARCHER,
        name="TestAgent",
        capabilities=["research"]
    )
    
    assert agent_id is not None
    assert pool.get_agent(agent_id) is not None


def test_agent_pool_by_role():
    """Test getting agents by role."""
    pool = AgentPool()
    
    pool.register_agent(AgentRole.RESEARCHER, "Research1", ["research"])
    pool.register_agent(AgentRole.ANALYZER, "Analyzer1", ["analysis"])
    pool.register_agent(AgentRole.RESEARCHER, "Research2", ["research"])
    
    researchers = pool.get_agents_by_role(AgentRole.RESEARCHER)
    assert len(researchers) == 2


def test_agent_pool_availability():
    """Test getting available agents."""
    pool = AgentPool()
    
    agent_id = pool.register_agent(AgentRole.RESEARCHER, "Research1", ["research"])
    
    available = pool.get_available_agents(AgentRole.RESEARCHER)
    assert len(available) == 1
    
    pool.set_agent_status(agent_id, "busy")
    available = pool.get_available_agents(AgentRole.RESEARCHER)
    assert len(available) == 0


def test_agent_pool_status():
    """Test agent pool status."""
    pool = AgentPool()
    
    pool.register_agent(AgentRole.RESEARCHER, "Research1", ["research"])
    pool.register_agent(AgentRole.ANALYZER, "Analyzer1", ["analysis"])
    
    status = pool.get_pool_status()
    assert status["total_agents"] == 2
    assert status["idle"] == 2


# Task Queue Tests
def test_task_queue_add():
    """Test adding task to queue."""
    queue = TaskQueue()
    
    task_id = queue.add_task(
        title="Test Task",
        description="Test",
        agent_role=AgentRole.RESEARCHER
    )
    
    assert task_id is not None
    assert queue.get_task(task_id) is not None


def test_task_queue_priority():
    """Test task priority ordering."""
    queue = TaskQueue()
    
    queue.add_task("Task1", "Desc", AgentRole.RESEARCHER, priority=1)
    queue.add_task("Task2", "Desc", AgentRole.RESEARCHER, priority=3)
    queue.add_task("Task3", "Desc", AgentRole.RESEARCHER, priority=2)
    
    pending = queue.get_pending_tasks()
    assert pending[0].title == "Task2"  # Highest priority first


def test_task_queue_completion():
    """Test task completion."""
    queue = TaskQueue()
    
    task_id = queue.add_task("Task", "Desc", AgentRole.RESEARCHER)
    queue.assign_task(task_id, "agent-1")
    
    success = queue.complete_task(task_id, {"result": "done"})
    assert success is True
    
    task = queue.get_task(task_id)
    assert task.status == TaskStatus.COMPLETED


def test_task_queue_status():
    """Test queue status."""
    queue = TaskQueue()
    
    queue.add_task("Task1", "Desc", AgentRole.RESEARCHER)
    queue.add_task("Task2", "Desc", AgentRole.RESEARCHER)
    
    status = queue.get_queue_status()
    assert status["total_tasks"] == 2
    assert status["pending"] == 2
    assert status["completed"] == 0


# Coordinator Tests
@pytest.mark.asyncio
async def test_coordinator_orchestrate():
    """Test agent coordination."""
    coordinator = AgentCoordinator()
    
    # Register some agents
    coordinator.pool.register_agent(AgentRole.PLANNER, "Planner", ["planning"])
    coordinator.pool.register_agent(AgentRole.RESEARCHER, "Researcher", ["research"])
    coordinator.pool.register_agent(AgentRole.ANALYZER, "Analyzer", ["analysis"])
    coordinator.pool.register_agent(AgentRole.EXECUTOR, "Executor", ["execution"])
    
    result = await coordinator.orchestrate(goal="Test goal")
    
    assert result["status"] == "completed"
    assert result["goal"] == "Test goal"


@pytest.mark.asyncio
async def test_coordinator_assign_task():
    """Test task assignment."""
    coordinator = AgentCoordinator()
    
    coordinator.pool.register_agent(AgentRole.RESEARCHER, "Researcher", ["research"])
    
    result = await coordinator.assign_task(
        title="Research Task",
        description="Conduct research",
        agent_role=AgentRole.RESEARCHER
    )
    
    assert result["success"] is True
    assert "task_id" in result


# Specialized Agents Tests
@pytest.mark.asyncio
async def test_research_agent():
    """Test research agent."""
    agent = ResearchAgent("research-1")
    
    findings = await agent.research("Python", depth="medium")
    
    assert findings["topic"] == "Python"
    assert "sources" in findings
    assert "key_findings" in findings


@pytest.mark.asyncio
async def test_analysis_agent():
    """Test analysis agent."""
    agent = AnalysisAgent("analysis-1")
    
    data = {"metric1": 10, "metric2": 20}
    analysis = await agent.analyze(data, analysis_type="statistical")
    
    assert "patterns" in analysis
    assert "insights" in analysis


@pytest.mark.asyncio
async def test_execution_agent():
    """Test execution agent."""
    agent = ExecutionAgent("executor-1")
    
    result = await agent.execute(
        task_description="Calculate sum",
        required_tools=["calculator"]
    )
    
    assert result["status"] == "completed"
    assert "output" in result


# Message Broker Tests
@pytest.mark.asyncio
async def test_message_broker_send():
    """Test sending message."""
    broker = MessageBroker()
    
    msg_id = await broker.send_message(
        sender_id="agent-1",
        recipient_id="agent-2",
        message_type=MessageType.REQUEST,
        content={"task": "research"}
    )
    
    assert msg_id is not None
    assert broker.get_message(msg_id) is not None


@pytest.mark.asyncio
async def test_message_broker_response():
    """Test message response."""
    broker = MessageBroker()
    
    msg_id = await broker.send_message(
        sender_id="agent-1",
        recipient_id="agent-2",
        message_type=MessageType.REQUEST,
        content={"task": "research"},
        requires_response=True
    )
    
    response_id = await broker.send_response(
        original_message_id=msg_id,
        sender_id="agent-2",
        response_content={"result": "done"}
    )
    
    response = broker.get_message(response_id)
    assert response.response_to == msg_id


@pytest.mark.asyncio
async def test_message_broker_handler():
    """Test message handler."""
    broker = MessageBroker()
    handled = []
    
    async def handler(message):
        handled.append(message.message_id)
    
    broker.register_handler("agent-2", handler)
    
    msg_id = await broker.send_message(
        sender_id="agent-1",
        recipient_id="agent-2",
        message_type=MessageType.REQUEST,
        content={"task": "research"}
    )
    
    assert msg_id in handled


def test_message_broker_stats():
    """Test broker statistics."""
    broker = MessageBroker()
    
    stats = broker.get_broker_stats()
    assert "total_messages" in stats
    assert "message_types" in stats
    assert "active_agents" in stats
