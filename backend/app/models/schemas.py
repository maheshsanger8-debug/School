"""Pydantic schemas for API requests and responses."""

from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
from datetime import datetime


class ExecuteAgentRequest(BaseModel):
    """Request to execute an agent."""
    
    goal: str = Field(description="Main goal for the agent to accomplish")
    session_id: Optional[str] = Field(default=None, description="Optional session ID")
    tools: Optional[List[str]] = Field(default=None, description="Tools to make available")
    preferences: Optional[Dict[str, Any]] = Field(default=None, description="User preferences")
    timeout_seconds: Optional[int] = Field(default=300, description="Execution timeout")
    max_iterations: Optional[int] = Field(default=10, description="Max iterations")


class ExecuteAgentResponse(BaseModel):
    """Response from agent execution."""
    
    execution_id: str = Field(description="Unique execution ID")
    session_id: str = Field(description="Session ID")
    status: str = Field(description="Execution status")
    goal: str = Field(description="Goal that was executed")
    final_answer: Optional[str] = Field(description="Final answer from agent")
    steps: int = Field(description="Number of steps executed")
    tools_used: List[str] = Field(description="Tools used during execution")
    execution_time_seconds: float = Field(description="Total execution time")
    error: Optional[str] = Field(description="Error if execution failed")


class ToolSchema(BaseModel):
    """Schema definition for a tool."""
    
    name: str = Field(description="Tool name")
    description: str = Field(description="Tool description")
    parameters: Dict[str, Any] = Field(description="Parameter schema")


class ListToolsResponse(BaseModel):
    """Response listing available tools."""
    
    tools: List[ToolSchema] = Field(description="Available tools")


class HealthResponse(BaseModel):
    """Health check response."""
    
    status: str = Field(description="Service status")
    version: str = Field(description="Service version")
    timestamp: datetime = Field(description="Response timestamp")


class ErrorResponse(BaseModel):
    """Error response."""
    
    error: str = Field(description="Error message")
    details: Optional[str] = Field(description="Error details")
    timestamp: datetime = Field(description="Error timestamp")
