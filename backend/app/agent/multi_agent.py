"""Multi-agent orchestration and coordination."""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import uuid


class AgentRole(str, Enum):
    """Agent role enumeration."""
    PLANNER = "planner"
    RESEARCHER = "researcher"
    ANALYZER = "analyzer"
    EXECUTOR = "executor"
    COORDINATOR = "coordinator"


class TaskStatus(str, Enum):
    """Task status enumeration."""
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class AgentTask:
    """Represents a task for an agent."""
    task_id: str
    title: str
    description: str
    agent_role: AgentRole
    status: TaskStatus = TaskStatus.PENDING
    assigned_to: Optional[str] = None
    priority: int = 1
    dependencies: List[str] = None
    result: Optional[Any] = None
    error: Optional[str] = None
    created_at: datetime = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.created_at is None:
            self.created_at = datetime.utcnow()


class AgentPool:
    """
    Pool of specialized agents.
    """
    
    def __init__(self):
        """Initialize agent pool."""
        self.agents: Dict[str, Dict[str, Any]] = {}
        self.agent_counter = 0
    
    def register_agent(
        self,
        role: AgentRole,
        name: str,
        capabilities: List[str]
    ) -> str:
        """
        Register an agent in the pool.
        
        Args:
            role: Agent role
            name: Agent name
            capabilities: List of capabilities
            
        Returns:
            Agent ID
        """
        self.agent_counter += 1
        agent_id = f"{role.value}-{self.agent_counter}"
        
        self.agents[agent_id] = {
            "id": agent_id,
            "role": role,
            "name": name,
            "capabilities": capabilities,
            "status": "idle",
            "current_task": None,
            "tasks_completed": 0,
            "created_at": datetime.utcnow().isoformat()
        }
        
        return agent_id
    
    def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get agent by ID."""
        return self.agents.get(agent_id)
    
    def get_agents_by_role(self, role: AgentRole) -> List[Dict[str, Any]]:
        """Get all agents with specific role."""
        return [a for a in self.agents.values() if a["role"] == role]
    
    def get_available_agents(self, role: AgentRole) -> List[Dict[str, Any]]:
        """Get available agents with specific role."""
        agents = self.get_agents_by_role(role)
        return [a for a in agents if a["status"] == "idle"]
    
    def set_agent_status(self, agent_id: str, status: str) -> bool:
        """Set agent status."""
        if agent_id in self.agents:
            self.agents[agent_id]["status"] = status
            return True
        return False
    
    def set_agent_task(self, agent_id: str, task_id: Optional[str]) -> bool:
        """Assign task to agent."""
        if agent_id in self.agents:
            self.agents[agent_id]["current_task"] = task_id
            return True
        return False
    
    def increment_task_count(self, agent_id: str) -> None:
        """Increment completed task count."""
        if agent_id in self.agents:
            self.agents[agent_id]["tasks_completed"] += 1
    
    def get_pool_status(self) -> Dict[str, Any]:
        """Get pool status."""
        idle = sum(1 for a in self.agents.values() if a["status"] == "idle")
        busy = sum(1 for a in self.agents.values() if a["status"] == "busy")
        
        return {
            "total_agents": len(self.agents),
            "idle": idle,
            "busy": busy,
            "by_role": self._count_by_role()
        }
    
    def _count_by_role(self) -> Dict[str, int]:
        """Count agents by role."""
        counts = {}
        for role in AgentRole:
            counts[role.value] = len(self.get_agents_by_role(role))
        return counts


class TaskQueue:
    """
    Queue for managing tasks.
    """
    
    def __init__(self):
        """Initialize task queue."""
        self.tasks: Dict[str, AgentTask] = {}
        self.pending: List[str] = []
        self.completed: List[str] = []
    
    def add_task(
        self,
        title: str,
        description: str,
        agent_role: AgentRole,
        priority: int = 1,
        dependencies: Optional[List[str]] = None
    ) -> str:
        """
        Add task to queue.
        
        Args:
            title: Task title
            description: Task description
            agent_role: Required agent role
            priority: Task priority
            dependencies: Task dependencies
            
        Returns:
            Task ID
        """
        task_id = str(uuid.uuid4())[:8]
        
        task = AgentTask(
            task_id=task_id,
            title=title,
            description=description,
            agent_role=agent_role,
            priority=priority,
            dependencies=dependencies or []
        )
        
        self.tasks[task_id] = task
        self.pending.append(task_id)
        
        return task_id
    
    def get_pending_tasks(self) -> List[AgentTask]:
        """Get all pending tasks sorted by priority."""
        tasks = [self.tasks[tid] for tid in self.pending]
        return sorted(tasks, key=lambda t: t.priority, reverse=True)
    
    def assign_task(self, task_id: str, agent_id: str) -> bool:
        """Assign task to agent."""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        task.assigned_to = agent_id
        task.status = TaskStatus.ASSIGNED
        task.started_at = datetime.utcnow()
        
        return True
    
    def complete_task(self, task_id: str, result: Any) -> bool:
        """Mark task as completed."""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        task.status = TaskStatus.COMPLETED
        task.result = result
        task.completed_at = datetime.utcnow()
        
        if task_id in self.pending:
            self.pending.remove(task_id)
        self.completed.append(task_id)
        
        return True
    
    def fail_task(self, task_id: str, error: str) -> bool:
        """Mark task as failed."""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        task.status = TaskStatus.FAILED
        task.error = error
        task.completed_at = datetime.utcnow()
        
        if task_id in self.pending:
            self.pending.remove(task_id)
        
        return True
    
    def get_task(self, task_id: str) -> Optional[AgentTask]:
        """Get task by ID."""
        return self.tasks.get(task_id)
    
    def get_queue_status(self) -> Dict[str, Any]:
        """Get queue status."""
        return {
            "total_tasks": len(self.tasks),
            "pending": len(self.pending),
            "completed": len(self.completed),
            "completion_rate": (len(self.completed) / len(self.tasks) * 100) if self.tasks else 0
        }


# Global instances
_agent_pool: Optional[AgentPool] = None
_task_queue: Optional[TaskQueue] = None


def get_agent_pool() -> AgentPool:
    """Get or create agent pool."""
    global _agent_pool
    if _agent_pool is None:
        _agent_pool = AgentPool()
    return _agent_pool


def get_task_queue() -> TaskQueue:
    """Get or create task queue."""
    global _task_queue
    if _task_queue is None:
        _task_queue = TaskQueue()
    return _task_queue
