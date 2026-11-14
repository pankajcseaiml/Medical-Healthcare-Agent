"""
Tests for Health Check and Homepage Endpoints.
Verifies service accessibility, agent registration listing, and secret isolation.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.agents.team import AGENT_NAMES

client = TestClient(app)


def test_homepage_accessibility():
    """Verify the single-page application is served successfully at GET /."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    assert "Medical Healthcare" in response.text
    assert "Agno" in response.text or "Agent" in response.text


def test_health_endpoint_structure_and_agents():
    """Verify GET /health returns operational status and registered agent information."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "healthy"
    assert "medical" in data["app_name"].lower() and "assistant" in data["app_name"].lower()
    assert "groq_configured" in data
    assert "model" in data
    assert isinstance(data["agents"], list)

    # Verify all three required agents are registered
    assert len(data["agents"]) == 3
    for agent_name in AGENT_NAMES:
        assert agent_name in data["agents"]


def test_health_endpoint_does_not_leak_secrets():
    """Verify GET /health never exposes API keys or raw credentials in the payload."""
    response = client.get("/health")
    assert response.status_code == 200
    text_content = response.text.lower()

    # Secrets isolation checks
    assert "gsk_" not in text_content
    assert "api_key" not in text_content
    assert "secret" not in text_content
    assert "password" not in text_content
