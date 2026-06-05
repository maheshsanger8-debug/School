"""Agent context management."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime


@dataclass
class ExecutionContext:
    """
    Manages execution context for an agent.
    
    Includes:
    - Available tools
    - Current constraints
    - User preferences
    - External data
    - Previous interactions
    """
    
    # Identifiers
    session_id: str
    execution_id: str
    
    # Available resources
    available_tools: List[str] = field(default_factory=list)
    available_files: List[str] = field(default_factory=list)
    
    # Constraints
    max_iterations: int = 10
    timeout_seconds: int = 300
    max_tokens: int = 4096
    
    # User context
    user_id: Optional[str] = None
    user_preferences: Dict[str, Any] = field(default_factory=dict)
    
    # External data
    environment_variables: Dict[str, str] = field(default_factory=dict)
    external_data: Dict[str, Any] = field(default_factory=dict)
    
    # Conversation history
    conversation_history: List[Dict[str, str]] = field(default_factory=list)
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def add_tool(self, tool_name: str) -> None:
        """Register an available tool."""
        if tool_name not in self.available_tools:
            self.available_tools.append(tool_name)
    
    def add_file(self, file_path: str) -> None:
        """Register an available file."""
        if file_path not in self.available_files:
            self.available_files.append(file_path)
    
    def set_preference(self, key: str, value: Any) -> None:
        """Set a user preference."""
        self.user_preferences[key] = value
    
    def set_external_data(self, key: str, value: Any) -> None:
        """Set external data."""
        self.external_data[key] = value
    
    def add_message(self, role: str, content: str) -> None:
        """Add a message to conversation history."""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def get_messages(self, limit: Optional[int] = None) -> List[Dict[str, str]]:
        """Get conversation history."""
        if limit:
            return self.conversation_history[-limit:]
        return self.conversation_history
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert context to dictionary."""
        return {
            "session_id": self.session_id,
            "execution_id": self.execution_id,
            "available_tools": self.available_tools,
            "available_files": self.available_files,
            "max_iterations": self.max_iterations,
            "timeout_seconds": self.timeout_seconds,
            "max_tokens": self.max_tokens,
            "user_id": self.user_id,
            "user_preferences": self.user_preferences,
            "environment_variables": self.environment_variables,
            "external_data": self.external_data,
            "conversation_history": self.conversation_history,
            "created_at": self.created_at.isoformat(),
        }
