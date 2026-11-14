"""
Tests for Request Validation and Error Handling.
Verifies input validation on POST /ask and graceful handling of missing Groq configuration.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.config import Settings

client = TestClient(app)


def test_empty_question_validation():
    """Verify that an empty question string returns 422 Unprocessable Entity."""
    response = client.post("/ask", json={"question": ""})
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_whitespace_only_question_validation():
    """Verify that whitespace-only question returns 422 Unprocessable Entity."""
    response = client.post("/ask", json={"question": "     "})
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_too_short_question_validation():
    """Verify that a question with fewer than 3 characters is rejected."""
    response = client.post("/ask", json={"question": "ab"})
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_missing_question_field_validation():
    """Verify that an empty JSON body or missing question field returns 422."""
    response = client.post("/ask", json={})
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_graceful_error_when_groq_not_configured():
    """Verify POST /ask returns 503 Service Unavailable when Groq API key is unconfigured."""
    unconfigured_settings = Settings(groq_api_key=None)

    with patch("app.main.get_settings", return_value=unconfigured_settings):
        response = client.post(
            "/ask",
            json={"question": "What are the common symptoms of asthma?"}
        )
        assert response.status_code == 503
        data = response.json()
        assert "GROQ_API_KEY is not configured" in data.get("detail", "")
