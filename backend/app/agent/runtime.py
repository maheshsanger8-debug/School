"""Agent runtime - core execution engine."""

import uuid
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging
from app.agent.state import AgentState
from app.agent.context import ExecutionContext
from app.tools import get_tool_registry
from app.config import settings

logger = logging.getLogger(__name__)


class AgentRuntime:
    """
    Core agent execution engine.
    
    Manages:
    - State
    - Context
    - Execution flow
    - Tool calls
    - Error handling
    """
    
    def __init__(self):
        """Initialize agent runtime."""
        self.tool_registry = get_tool_registry()
        self.active_executions: Dict[str, AgentState] = {}
    
    async def execute(
        self,
        goal: str,
        session_id: Optional[str] = None,
        tools: Optional[List[str]] = None,
        user_preferences: Optional[Dict[str, Any]] = None,
        timeout_seconds: Optional[int] = None,
        max_iterations: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Execute agent to accomplish a goal.
        
        Args:
            goal: Main goal to accomplish
            session_id: Optional session ID
            tools: Optional list of available tools
            user_preferences: Optional user preferences
            timeout_seconds: Execution timeout
            max_iterations: Max iterations
            
        Returns:
            Execution result dictionary
        """
        # Create IDs
        if not session_id:
            session_id = str(uuid.uuid4())
        execution_id = str(uuid.uuid4())
        
        # Create state and context
        state = AgentState(
            session_id=session_id,
            execution_id=execution_id,
            main_goal=goal,
            total_steps=max_iterations or settings.MAX_ITERATIONS
        )
        
        context = ExecutionContext(
            session_id=session_id,
            execution_id=execution_id,
            max_iterations=max_iterations or settings.MAX_ITERATIONS,
            timeout_seconds=timeout_seconds or settings.TIMEOUT_SECONDS,
            user_preferences=user_preferences or {}
        )
        
        # Register available tools
        available_tools = tools or self.tool_registry.list_tools()
        for tool_name in available_tools:
            context.add_tool(tool_name)
        
        # Store execution
        self.active_executions[execution_id] = state
        
        try:
            logger.info(f"Starting execution {execution_id} for goal: {goal}")
            
            # Simple execution loop - placeholder for LangGraph integration
            start_time = datetime.utcnow()
            
            # Add initial thought
            state.add_thought(f"Goal: {goal}")
            state.add_thought(f"Available tools: {', '.join(available_tools)}")
            
            # Simulate execution steps
            for step in range(state.total_steps):
                state.increment_step()
                
                # Check timeout
                elapsed = (datetime.utcnow() - start_time).total_seconds()
                if elapsed > context.timeout_seconds:
                    state.fail("Execution timeout")
                    break
                
                # Placeholder: would integrate with LLM here
                # For now, just demonstrate completion
                if step == state.total_steps - 1:
                    final_answer = f"Completed execution for goal: {goal}"
                    state.complete(final_answer)
                    break
            
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            
            result = {
                "execution_id": execution_id,
                "session_id": session_id,
                "status": state.status,
                "goal": goal,
                "final_answer": state.final_answer,
                "steps": state.current_step,
                "tools_used": state.tools_used,
                "execution_time_seconds": execution_time,
                "error": state.error
            }
            
            logger.info(f"Execution {execution_id} completed with status: {state.status}")
            
            return result
        
        except Exception as e:
            logger.error(f"Execution {execution_id} failed: {str(e)}")
            state.fail(str(e))
            
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            
            return {
                "execution_id": execution_id,
                "session_id": session_id,
                "status": "failed",
                "goal": goal,
                "final_answer": None,
                "steps": state.current_step,
                "tools_used": state.tools_used,
                "execution_time_seconds": execution_time,
                "error": str(e)
            }
        
        finally:
            # Clean up
            if execution_id in self.active_executions:
                del self.active_executions[execution_id]
    
    def get_execution_state(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """Get current execution state."""
        if execution_id in self.active_executions:
            return self.active_executions[execution_id].to_dict()
        return None


# Global runtime instance
_runtime: Optional[AgentRuntime] = None


def get_agent_runtime() -> AgentRuntime:
    """Get or create global agent runtime."""
    global _runtime
    if _runtime is None:
        _runtime = AgentRuntime()
    return _runtime
