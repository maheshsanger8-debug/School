"""Integration tests for multi-agent execution."""

import pytest
from app.agent.coordinator import AgentCoordinator
from app.agent.multi_agent import AgentRole, TaskStatus
from app.agent.communication import MessageBroker, MessageType


@pytest.mark.asyncio
async def test_full_multi_agent_workflow():
    """
    Test complete multi-agent workflow from task to result.
    """
    coordinator = AgentCoordinator()
    
    # Setup agent pool
    planner_id = coordinator.pool.register_agent(
        AgentRole.PLANNER,
        "MainPlanner",
        ["decomposition", "planning"]
    )
    
    researcher_id = coordinator.pool.register_agent(
        AgentRole.RESEARCHER,
        "MainResearcher",
        ["research", "search"]
    )
    
    analyzer_id = coordinator.pool.register_agent(
        AgentRole.ANALYZER,
        "MainAnalyzer",
        ["analysis", "insights"]
    )
    
    executor_id = coordinator.pool.register_agent(
        AgentRole.EXECUTOR,
        "MainExecutor",
        ["execution", "tools"]
    )
    
    # Start orchestration
    result = await coordinator.orchestrate(
        goal="Complete research and analysis workflow"
    )
    
    assert result["status"] == "completed"
    assert result["phases"]["planning"]["agents_used"] > 0
    assert result["phases"]["research"]["agents_used"] > 0


@pytest.mark.asyncio
async def test_task_delegation_and_completion():
    """
    Test task delegation between coordinator and agents.
    """
    coordinator = AgentCoordinator()
    
    # Register agents
    coordinator.pool.register_agent(AgentRole.RESEARCHER, "R1", ["research"])
    coordinator.pool.register_agent(AgentRole.ANALYZER, "A1", ["analysis"])
    
    # Assign research task
    research_result = await coordinator.assign_task(
        title="Research AI",
        description="Research artificial intelligence",
        agent_role=AgentRole.RESEARCHER,
        priority=2
    )
    
    assert research_result["success"] is True
    research_task_id = research_result["task_id"]
    
    # Assign analysis task
    analysis_result = await coordinator.assign_task(
        title="Analyze Data",
        description="Analyze AI research data",
        agent_role=AgentRole.ANALYZER,
        priority=1
    )
    
    assert analysis_result["success"] is True
    analysis_task_id = analysis_result["task_id"]
    
    # Check queue status
    queue_status = coordinator.queue.get_queue_status()
    assert queue_status["total_tasks"] == 2
    assert queue_status["pending"] == 2
    
    # Complete first task
    await coordinator.complete_task(
        research_task_id,
        {"findings": "AI is important"}
    )
    
    # Check updated status
    queue_status = coordinator.queue.get_queue_status()
    assert queue_status["completed"] == 1


@pytest.mark.asyncio
async def test_inter_agent_communication():
    """
    Test communication between agents through message broker.
    """
    broker = MessageBroker()
    
    # Setup handlers
    received_messages = {"agent-2": [], "agent-3": []}
    
    async def handler_2(message):
        received_messages["agent-2"].append(message)
    
    async def handler_3(message):
        received_messages["agent-3"].append(message)
    
    broker.register_handler("agent-2", handler_2)
    broker.register_handler("agent-3", handler_3)
    
    # Send research request
    msg1 = await broker.send_message(
        sender_id="agent-1",
        recipient_id="agent-2",
        message_type=MessageType.REQUEST,
        content={"task": "research", "topic": "AI"},
        requires_response=True
    )
    
    # Agent 2 responds
    msg2 = await broker.send_response(
        original_message_id=msg1,
        sender_id="agent-2",
        response_content={"findings": ["Finding 1", "Finding 2"]}
    )
    
    # Send analysis request
    msg3 = await broker.send_message(
        sender_id="agent-1",
        recipient_id="agent-3",
        message_type=MessageType.REQUEST,
        content={"task": "analyze", "data": {"findings": ["Finding 1"]}},
        requires_response=True
    )
    
    # Check communication
    assert len(received_messages["agent-2"]) == 1
    assert len(received_messages["agent-3"]) == 1
    
    # Check broker stats
    stats = broker.get_broker_stats()
    assert stats["total_messages"] == 3


@pytest.mark.asyncio
async def test_agent_load_balancing():
    """
    Test load balancing when assigning tasks to agents.
    """
    coordinator = AgentCoordinator()
    
    # Register multiple agents of same role
    agents = []
    for i in range(3):
        agent_id = coordinator.pool.register_agent(
            AgentRole.EXECUTOR,
            f"Executor-{i}",
            ["execution"]
        )
        agents.append(agent_id)
    
    # Assign multiple tasks
    for i in range(5):
        result = await coordinator.assign_task(
            title=f"Task {i}",
            description=f"Execute task {i}",
            agent_role=AgentRole.EXECUTOR
        )
        assert result["success"] is True
    
    # Check pool status
    pool_status = coordinator.pool.get_pool_status()
    assert pool_status["busy"] > 0
    assert pool_status["total_agents"] == 3
