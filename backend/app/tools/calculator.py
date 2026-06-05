"""Calculator tool for mathematical operations."""

import re
from typing import Any, Dict, Optional
from app.tools.base import BaseTool, ToolResult


class CalculatorTool(BaseTool):
    """Tool for performing mathematical calculations."""
    
    def __init__(self):
        super().__init__(
            name="calculator",
            description="Perform mathematical calculations. Supports +, -, *, /, %, ** operators."
        )
    
    async def execute(self, expression: str) -> ToolResult:
        """
        Evaluate a mathematical expression.
        
        Args:
            expression: Math expression to evaluate (e.g., "2 + 2")
            
        Returns:
            ToolResult with calculation result
        """
        try:
            # Validate expression - only allow safe characters
            if not self._validate_expression(expression):
                return ToolResult(
                    success=False,
                    data=None,
                    error="Invalid expression: contains unsafe characters"
                )
            
            # Evaluate expression
            result = eval(expression, {"__builtins__": {}}, {})
            
            return ToolResult(
                success=True,
                data=result,
                metadata={"expression": expression, "result": result}
            )
        
        except ZeroDivisionError:
            return ToolResult(
                success=False,
                data=None,
                error="Division by zero"
            )
        
        except SyntaxError as e:
            return ToolResult(
                success=False,
                data=None,
                error=f"Syntax error: {str(e)}"
            )
        
        except Exception as e:
            return ToolResult(
                success=False,
                data=None,
                error=f"Calculation error: {str(e)}"
            )
    
    def _validate_expression(self, expression: str) -> bool:
        """Validate that expression only contains safe characters."""
        # Allow numbers, operators, spaces, and parentheses
        allowed_pattern = r'^[\d+\-*/%().\s]+$'
        return bool(re.match(allowed_pattern, expression))
    
    def get_schema(self) -> Dict[str, Any]:
        """Get JSON schema for calculator parameters."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate"
                    }
                },
                "required": ["expression"]
            }
        }
