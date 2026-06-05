"""Base tool interface for the agent."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class ToolResult:
    """Result from tool execution."""
    
    success: bool
    data: Any
    error: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class BaseTool(ABC):
    """
    Abstract base class for all tools.
    
    All tools must implement:
    - name: Unique tool identifier
    - description: Human-readable description
    - execute: Actual tool logic
    """
    
    def __init__(self, name: str, description: str):
        """Initialize tool."""
        self.name = name
        self.description = description
    
    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        """
        Execute the tool.
        
        Args:
            **kwargs: Tool-specific parameters
            
        Returns:
            ToolResult: Result of tool execution
        """
        pass
    
    def get_schema(self) -> Dict[str, Any]:
        """
        Get JSON schema for tool parameters.
        
        Returns:
            Dict describing tool parameters
        """
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {}
        }
    
    def __repr__(self) -> str:
        return f"Tool(name={self.name})"
