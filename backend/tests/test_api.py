"""Tests for FastAPI application."""

import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "app" in response.json()
    assert "version" in response.json()


def test_health_endpoint():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_status_endpoint():
    """Test status endpoint."""
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert "app_name" in data
    assert "available_tools" in data


def test_list_tools_endpoint():
    """Test list tools endpoint."""
    response = client.get("/tools")
    assert response.status_code == 200
    data = response.json()
    assert "tools" in data
    assert len(data["tools"]) > 0


def test_execute_agent_endpoint():
    """Test execute agent endpoint."""
    request_data = {
        "goal": "Test execution",
        "max_iterations": 1,
        "timeout_seconds": 10
    }
    
    response = client.post("/execute", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "execution_id" in data
    assert "session_id" in data
    assert "status" in data


def test_execute_agent_with_session():
    """Test execute agent with session ID."""
    request_data = {
        "goal": "Test execution",
        "session_id": "test-session-123",
        "max_iterations": 1
    }
    
    response = client.post("/execute", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == "test-session-123"


def test_missing_goal_field():
    """Test missing required goal field."""
    request_data = {"max_iterations": 1}
    
    response = client.post("/execute", json=request_data)
    assert response.status_code == 422  # Validation error
