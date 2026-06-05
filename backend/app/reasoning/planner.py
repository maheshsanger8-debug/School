"""Planning agent for task decomposition."""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class TaskType(str, Enum):
    """Task type enumeration."""
    RESEARCH = "research"
    ANALYSIS = "analysis"
    CALCULATION = "calculation"
    DATA_RETRIEVAL = "data_retrieval"
    SYNTHESIS = "synthesis"


@dataclass
class Task:
    """Represents a sub-task."""
    id: str
    title: str
    description: str
    task_type: TaskType
    priority: int
    dependencies: List[str]
    completed: bool = False
    result: Optional[Any] = None


class PlanningAgent:
    """
    Agent for decomposing goals into actionable tasks.
    """
    
    def __init__(self):
        """Initialize planning agent."""
        self.tasks: Dict[str, Task] = {}
        self.task_counter = 0
    
    def decompose(
        self,
        goal: str,
        max_tasks: int = 10
    ) -> Dict[str, Any]:
        """
        Decompose a goal into tasks.
        
        Args:
            goal: Main goal
            max_tasks: Max tasks to create
            
        Returns:
            Plan with tasks
        """
        # Placeholder implementation
        # Real implementation would use LLM for decomposition
        
        plan = {
            "goal": goal,
            "tasks": [
                {
                    "id": "task-1",
                    "title": "Understand Goal",
                    "description": f"Analyze: {goal}",
                    "type": "analysis",
                    "priority": 1,
                    "dependencies": []
                },
                {
                    "id": "task-2",
                    "title": "Execute",
                    "description": f"Execute: {goal}",
                    "type": "execution",
                    "priority": 2,
                    "dependencies": ["task-1"]
                }
            ]
        }
        
        return plan
    
    def add_task(
        self,
        title: str,
        description: str,
        task_type: TaskType,
        priority: int = 1,
        dependencies: Optional[List[str]] = None
    ) -> str:
        """
        Add a task to the plan.
        
        Args:
            title: Task title
            description: Task description
            task_type: Task type
            priority: Priority level
            dependencies: Task dependencies
            
        Returns:
            Task ID
        """
        self.task_counter += 1
        task_id = f"task-{self.task_counter}"
        
        task = Task(
            id=task_id,
            title=title,
            description=description,
            task_type=task_type,
            priority=priority,
            dependencies=dependencies or []
        )
        
        self.tasks[task_id] = task
        return task_id
    
    def mark_complete(
        self,
        task_id: str,
        result: Optional[Any] = None
    ) -> bool:
        """
        Mark task as complete.
        
        Args:
            task_id: Task ID
            result: Optional task result
            
        Returns:
            True if successful
        """
        if task_id in self.tasks:
            self.tasks[task_id].completed = True
            self.tasks[task_id].result = result
            return True
        return False
    
    def get_pending_tasks(self) -> List[Task]:
        """Get all pending tasks."""
        return [t for t in self.tasks.values() if not t.completed]
    
    def get_plan_status(self) -> Dict[str, Any]:
        """Get plan status."""
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks.values() if t.completed)
        
        return {
            "total_tasks": total,
            "completed": completed,
            "pending": total - completed,
            "progress_percent": (completed / total * 100) if total > 0 else 0
        }


# Global planning agent instance
_planning_agent: Optional[PlanningAgent] = None


def get_planning_agent() -> PlanningAgent:
    """Get or create global planning agent."""
    global _planning_agent
    if _planning_agent is None:
        _planning_agent = PlanningAgent()
    return _planning_agent
