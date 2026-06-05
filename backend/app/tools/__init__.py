"""Tool registry for managing available tools."""

from typing import Dict, List, Optional
from app.tools.base import BaseTool
from app.tools.calculator import CalculatorTool


class ToolRegistry:
    """Registry for managing agent tools."""
    
    def __init__(self):
        """Initialize tool registry."""
        self.tools: Dict[str, BaseTool] = {}
        self._register_default_tools()
    
    def _register_default_tools(self) -> None:
        """Register default tools."""
        self.register(CalculatorTool())
    
    def register(self, tool: BaseTool) -> None:
        """Register a tool."""
        self.tools[tool.name] = tool
    
    def get(self, tool_name: str) -> Optional[BaseTool]:
        """Get a tool by name."""
        return self.tools.get(tool_name)
    
    def list_tools(self) -> List[str]:
        """List all available tools."""
        return list(self.tools.keys())
    
    def get_schemas(self) -> List[Dict]:
        """Get schemas for all tools."""
        return [tool.get_schema() for tool in self.tools.values()]
    
    def __repr__(self) -> str:
        return f"ToolRegistry(tools={list(self.tools.keys())})"


# Global tool registry
_tool_registry: Optional[ToolRegistry] = None


def get_tool_registry() -> ToolRegistry:
    """Get or create global tool registry."""
    global _tool_registry
    if _tool_registry is None:
        _tool_registry = ToolRegistry()
    return _tool_registry
