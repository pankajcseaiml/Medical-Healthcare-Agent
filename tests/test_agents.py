"""
Tests for Agno Multi-Agent Team, Tools, and Workflow.
Verifies agent registration, Team coordination mode, library search, source tracking, and safety disclaimer.
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from app.main import app
from app.agents.team import (
    create_medical_agents,
    create_medical_team,
    run_medical_workflow,
    AGENT_NAMES,
    MANDATORY_DISCLAIMER,
)
from app.agents.tools import (
    search_library,
    get_consulted_sources,
    clear_consulted_sources,
    search_medical_documents,
)
from app.config import Settings
from agno.team import TeamMode

client = TestClient(app)


def test_agent_registration_and_configuration():
    """Verify that all three specialized agents are created with proper configurations and tools."""
    query_analyzer, medical_research_agent, medical_answer_reviewer = create_medical_agents()

    assert query_analyzer.name == "Query Analyzer"
    assert "Healthcare Domain" in query_analyzer.role
    assert query_analyzer.instructions is not None

    assert medical_research_agent.name == "Medical Research Agent"
    assert "Medical Reference" in medical_research_agent.role
    assert medical_research_agent.tools is not None
    assert len(medical_research_agent.tools) >= 1
    # Check that search_library tool is registered
    tool_names = [getattr(t, "__name__", str(t)) for t in medical_research_agent.tools]
    assert "search_library" in tool_names

    assert medical_answer_reviewer.name == "Medical Answer Reviewer"
    assert "Safety Review" in medical_answer_reviewer.role
    assert medical_answer_reviewer.instructions is not None


def test_agno_team_creation_and_coordinate_mode():
    """Verify that Agno Team is configured with TeamMode.coordinate and 3 members."""
    settings = Settings(groq_api_key="gsk_mock_test_key_12345")
    team = create_medical_team(settings=settings)

    assert team.name == "Medical Healthcare Multi-Agent Team"
    assert team.mode == TeamMode.coordinate
    assert len(team.members) == 3

    member_names = [m.name for m in team.members]
    assert member_names == AGENT_NAMES


def test_medical_knowledge_library_search_tool():
    """Verify search_library tool retrieves verified reference content and citations."""
    clear_consulted_sources()

    # Search for diabetes
    result = search_library("diabetes symptoms and prevention")
    assert "World Health Organization - Diabetes" in result
    assert "blood glucose" in result.lower() or "insulin" in result.lower()

    # Search for hypertension
    result_hyp = search_library("hypertension high blood pressure DASH")
    assert "American Heart Association" in result_hyp
    assert "blood pressure" in result_hyp.lower()


def test_medical_source_tracking():
    """Verify that search_library tracks consulted medical sources in isolation."""
    clear_consulted_sources()
    assert get_consulted_sources() == []

    # Consult asthma doc
    search_library("asthma symptoms and rescue inhaler")
    sources = get_consulted_sources()
    assert len(sources) >= 1
    assert "Global Initiative for Asthma (GINA) - Patient Guidelines" in sources

    # Consult cold and flu doc
    search_library("influenza vs cold fever differences")
    updated_sources = get_consulted_sources()
    assert len(updated_sources) >= 2
    assert "Centers for Disease Control and Prevention (CDC) - Cold Versus Flu" in updated_sources

    # Reset
    clear_consulted_sources()
    assert get_consulted_sources() == []


def test_reviewer_safety_and_disclaimer_inclusion():
    """Verify that the medical workflow enforces the mandatory healthcare disclaimer and safety guidelines."""
    test_settings = Settings(groq_api_key="gsk_mock_test_key_12345")

    # Mock team.run to simulate team coordination output
    mock_run_output = MagicMock()
    mock_run_output.content = (
        "## Diabetes Management\n\n"
        "Diabetes is managed with healthy nutrition and physical activity.\n\n"
        "### Red Flag Warning Signs\n"
        "Seek emergency medical attention if ketoacidosis symptoms occur."
    )

    with patch("agno.team.team.Team.run", return_value=mock_run_output):
        response = run_medical_workflow(
            "What are the symptoms and prevention methods of diabetes?",
            settings=test_settings,
        )

        assert response["status"] == "success"
        assert "diabetes" in response["question"].lower()
        assert MANDATORY_DISCLAIMER in response["answer"]
        assert response["disclaimer"] == MANDATORY_DISCLAIMER
        assert isinstance(response["sources"], list)
        assert len(response["sources"]) >= 1


def test_end_to_end_ask_api_endpoint():
    """Verify POST /ask returns successful response conforming to AskResponse schema."""
    test_settings = Settings(groq_api_key="gsk_mock_test_key_12345")

    mock_workflow_output = {
        "status": "success",
        "question": "What are common asthma triggers and treatments?",
        "answer": "## Asthma Overview & Guidelines\n\nAsthma is a chronic condition affecting airways.",
        "sources": ["Global Initiative for Asthma (GINA) - Patient Guidelines"],
        "disclaimer": MANDATORY_DISCLAIMER,
    }

    with patch("app.main.get_settings", return_value=test_settings), \
         patch("app.main.run_medical_workflow", return_value=mock_workflow_output):

        response = client.post(
            "/ask",
            json={"question": "What are common asthma triggers and treatments?"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "Asthma" in data["answer"]
        assert isinstance(data["sources"], list)
        assert data["disclaimer"] == MANDATORY_DISCLAIMER
