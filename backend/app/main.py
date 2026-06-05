"""FastAPI application main entry point."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import logging
from contextlib import asynccontextmanager

from app.config import settings
from app.utils.logger import setup_logging, get_logger
from app.models.schemas import (
    ExecuteAgentRequest,
    ExecuteAgentResponse,
    ListToolsResponse,
    ToolSchema,
    HealthResponse,
    ErrorResponse
)
from app.agent.runtime import get_agent_runtime
from app.tools import get_tool_registry

# Setup logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context."""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    yield
    logger.info(f"Shutting down {settings.APP_NAME}")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Production-grade autonomous AI Agent",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)


# ============================================================================
# Health & Status Endpoints
# ============================================================================

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        timestamp=datetime.utcnow()
    )


@app.get("/status", tags=["Status"])
async def get_status():
    """Get system status."""
    runtime = get_agent_runtime()
    registry = get_tool_registry()
    
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
        "available_tools": registry.list_tools(),
        "active_executions": len(runtime.active_executions),
        "timestamp": datetime.utcnow().isoformat()
    }


# ============================================================================
# Tool Endpoints
# ============================================================================

@app.get("/tools", response_model=ListToolsResponse, tags=["Tools"])
async def list_tools():
    """List available tools."""
    registry = get_tool_registry()
    schemas = registry.get_schemas()
    
    tools = [
        ToolSchema(
            name=s["name"],
            description=s["description"],
            parameters=s.get("parameters", {})
        )
        for s in schemas
    ]
    
    return ListToolsResponse(tools=tools)


# ============================================================================
# Agent Execution Endpoints
# ============================================================================

@app.post("/execute", response_model=ExecuteAgentResponse, tags=["Agent"])
async def execute_agent(request: ExecuteAgentRequest):
    """
    Execute agent to accomplish a goal.
    
    Args:
        goal: Main goal for the agent
        session_id: Optional session ID for continuity
        tools: Optional list of tools to enable
        preferences: Optional user preferences
        timeout_seconds: Execution timeout
        max_iterations: Max iterations
        
    Returns:
        Execution result
    """
    try:
        runtime = get_agent_runtime()
        
        result = await runtime.execute(
            goal=request.goal,
            session_id=request.session_id,
            tools=request.tools,
            user_preferences=request.preferences,
            timeout_seconds=request.timeout_seconds,
            max_iterations=request.max_iterations
        )
        
        return ExecuteAgentResponse(**result)
    
    except Exception as e:
        logger.error(f"Agent execution error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "details": str(exc) if settings.DEBUG else None,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


# ============================================================================
# Root Endpoint
# ============================================================================

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "openapi": "/openapi.json"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
