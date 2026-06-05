"""Agent coordinator for multi-agent orchestration."""

from typing import Any, Dict, List, Optional
import logging
from datetime import datetime
from app.agent.multi_agent import (
    AgentPool,
    TaskQueue,
    AgentRole,
    TaskStatus,
    get_agent_pool,
    get_task_queue
)

logger = logging.getLogger(__name__)


class AgentCoordinator:
    """
    Coordinates multiple agents and distributes tasks.
    """
    
    def __init__(self):
        """Initialize coordinator."""
        self.pool = get_agent_pool()
        self.queue = get_task_queue()
        self.execution_history: List[Dict[str, Any]] = []
    
    async def orchestrate(
        self,
        goal: str,
        max_iterations: int = 10
    ) -> Dict[str, Any]:
        """
        Orchestrate multi-agent execution for a goal.
        
        Args:
            goal: Main goal
            max_iterations: Max coordination iterations
            
        Returns:
            Orchestration result
        """
        orchestration_id = f"orch-{datetime.utcnow().timestamp()}"
        
        try:
            logger.info(f"Starting orchestration {orchestration_id} for goal: {goal}")
            
            # Phase 1: Planning
            logger.info("Phase 1: Decomposing goal into tasks")
            planner_agents = self.pool.get_available_agents(AgentRole.PLANNER)
            if not planner_agents:
                logger.warning("No planner agents available")
                planner_agents = self.pool.get_agents_by_role(AgentRole.PLANNER)
            
            # Phase 2: Research
            logger.info("Phase 2: Researching")
            researcher_agents = self.pool.get_available_agents(AgentRole.RESEARCHER)
            
            # Phase 3: Analysis
            logger.info("Phase 3: Analyzing")
            analyzer_agents = self.pool.get_available_agents(AgentRole.ANALYZER)
            
            # Phase 4: Execution
            logger.info("Phase 4: Executing")
            executor_agents = self.pool.get_available_agents(AgentRole.EXECUTOR)
            
            # Placeholder: actual multi-agent execution logic
            # Real implementation would have sophisticated task distribution
            
            result = {
                "orchestration_id": orchestration_id,
                "goal": goal,
                "status": "completed",
                "phases": {
                    "planning": {"agents_used": len(planner_agents)},
                    "research": {"agents_used": len(researcher_agents)},
                    "analysis": {"agents_used": len(analyzer_agents)},
                    "execution": {"agents_used": len(executor_agents)}
                },
                "timestamp": datetime.utcnow().isoformat()
            }
            
            self.execution_history.append(result)
            logger.info(f"Orchestration {orchestration_id} completed")
            
            return result
        
        except Exception as e:
            logger.error(f"Orchestration {orchestration_id} failed: {str(e)}")
            return {
                "orchestration_id": orchestration_id,
                "status": "failed",
                "error": str(e)
            }
    
    async def assign_task(
        self,
        title: str,
        description: str,
        agent_role: AgentRole,
        priority: int = 1
    ) -> Dict[str, Any]:
        """
        Assign task to available agent.
        
        Args:
            title: Task title
            description: Task description
            agent_role: Required agent role
            priority: Task priority
            
        Returns:
            Assignment result
        """
        # Add task to queue
        task_id = self.queue.add_task(
            title=title,
            description=description,
            agent_role=agent_role,
            priority=priority
        )
        
        # Find available agent
        agents = self.pool.get_available_agents(agent_role)
        
        if not agents:
            logger.warning(f"No available {agent_role.value} agents")
            return {
                "success": False,
                "task_id": task_id,
                "error": f"No available agents for role {agent_role.value}"
            }
        
        # Assign to first available agent
        agent = agents[0]
        agent_id = agent["id"]
        
        self.queue.assign_task(task_id, agent_id)
        self.pool.set_agent_status(agent_id, "busy")
        self.pool.set_agent_task(agent_id, task_id)
        
        return {
            "success": True,
            "task_id": task_id,
            "assigned_to": agent_id
        }
    
    async def complete_task(
        self,
        task_id: str,
        result: Any
    ) -> bool:
        """
        Mark task as completed.
        
        Args:
            task_id: Task ID
            result: Task result
            
        Returns:
            Success status
        """
        task = self.queue.get_task(task_id)
        if not task or not task.assigned_to:
            return False
        
        self.queue.complete_task(task_id, result)
        agent_id = task.assigned_to
        
        self.pool.set_agent_status(agent_id, "idle")
        self.pool.set_agent_task(agent_id, None)
        self.pool.increment_task_count(agent_id)
        
        return True
    
    def get_status(self) -> Dict[str, Any]:
        """Get coordinator status."""
        return {
            "pool": self.pool.get_pool_status(),
            "queue": self.queue.get_queue_status(),
            "orchestrations": len(self.execution_history)
        }


# Global coordinator instance
_coordinator: Optional[AgentCoordinator] = None


def get_agent_coordinator() -> AgentCoordinator:
    """Get or create agent coordinator."""
    global _coordinator
    if _coordinator is None:
        _coordinator = AgentCoordinator()
    return _coordinator
