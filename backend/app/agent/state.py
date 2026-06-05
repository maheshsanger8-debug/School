"""Agent state management."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime
import json


@dataclass
class AgentState:
    """
    Represents the complete state of an agent execution.
    
    Tracks:
    - Current goal and sub-goals
    - Execution history
    - Tool usage
    - Thought processes
    - Intermediate results
    """
    
    # Identifiers
    session_id: str
    execution_id: str
    
    # Goal tracking
    main_goal: str
    current_step: int = 0
    total_steps: Optional[int] = None
    
    # Execution state
    status: str = "running"  # running, completed, failed, paused
    thoughts: List[str] = field(default_factory=list)
    actions: List[Dict[str, Any]] = field(default_factory=list)
    observations: List[str] = field(default_factory=list)
    
    # Tool interactions
    tools_used: List[str] = field(default_factory=list)
    tool_results: Dict[str, Any] = field(default_factory=dict)
    
    # Results
    final_answer: Optional[str] = None
    intermediate_results: Dict[str, Any] = field(default_factory=dict)
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    error: Optional[str] = None
    
    def add_thought(self, thought: str) -> None:
        """Record a thought during reasoning."""
        self.thoughts.append(thought)
        self.updated_at = datetime.utcnow()
    
    def add_action(self, action: Dict[str, Any]) -> None:
        """Record an action taken."""
        self.actions.append(action)
        if "tool" in action:
            self.tools_used.append(action["tool"])
        self.updated_at = datetime.utcnow()
    
    def add_observation(self, observation: str) -> None:
        """Record an observation from an action."""
        self.observations.append(observation)
        self.updated_at = datetime.utcnow()
    
    def set_result(self, tool_name: str, result: Any) -> None:
        """Store a tool result."""
        self.tool_results[tool_name] = result
        self.updated_at = datetime.utcnow()
    
    def increment_step(self) -> None:
        """Move to next execution step."""
        self.current_step += 1
        self.updated_at = datetime.utcnow()
    
    def complete(self, answer: str) -> None:
        """Mark execution as completed with final answer."""
        self.status = "completed"
        self.final_answer = answer
        self.updated_at = datetime.utcnow()
    
    def fail(self, error: str) -> None:
        """Mark execution as failed."""
        self.status = "failed"
        self.error = error
        self.updated_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary."""
        return {
            "session_id": self.session_id,
            "execution_id": self.execution_id,
            "main_goal": self.main_goal,
            "current_step": self.current_step,
            "total_steps": self.total_steps,
            "status": self.status,
            "thoughts": self.thoughts,
            "actions": self.actions,
            "observations": self.observations,
            "tools_used": self.tools_used,
            "tool_results": self.tool_results,
            "final_answer": self.final_answer,
            "intermediate_results": self.intermediate_results,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "error": self.error,
        }
    
    def __repr__(self) -> str:
        return f"AgentState(session_id={self.session_id}, status={self.status}, step={self.current_step}/{self.total_steps})"
