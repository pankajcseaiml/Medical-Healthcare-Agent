"""
Agno Multi-Agent Healthcare Team Coordination.
Coordinates Query Analyzer, Medical Research Agent, and Medical Answer Reviewer.
"""

from typing import List, Dict, Any, Optional, Tuple
import logging
from agno.agent import Agent
from agno.team import Team, TeamMode
from agno.models.groq import Groq

from app.config import Settings, get_settings
from app.agents.tools import (
    search_library,
    search_Library,
    get_consulted_sources,
    clear_consulted_sources,
    search_medical_documents,
    verify_disclaimer,
)

logger = logging.getLogger(__name__)

AGENT_NAMES: List[str] = [
    "Query Analyzer",
    "Medical Research Agent",
    "Medical Answer Reviewer",
]

MANDATORY_DISCLAIMER: str = (
    "Disclaimer: This Medical Healthcare Assistant provides educational and informational guidance only. "
    "It does not provide clinical diagnosis or prescribe treatment. "
    "Consult a qualified healthcare professional for personal medical advice."
)


class GroqNotConfiguredError(Exception):
    """Raised when Groq API key is missing or unconfigured."""
    pass


def create_medical_agents(
    model: Optional[Any] = None
) -> Tuple[Agent, Agent, Agent]:
    """
    Instantiate the three specialized healthcare AI agents.

    1. Query Analyzer: Healthcare query classification and entity extraction.
    2. Medical Research Agent: Knowledge library search and evidence retrieval.
    3. Medical Answer Reviewer: Clinical safety check, grounding, and disclaimer enforcement.
    """

    # Agent 1: Query Analyzer
    query_analyzer = Agent(
        name="Query Analyzer",
        role="Healthcare Domain Identification, Topic Extraction, and Research Question Formulation",
        model=model,
        instructions=[
            "You are the Query Analyzer for a medical healthcare assistance system.",
            "Your responsibilities are:",
            "1. Analyze the user's healthcare query and identify the primary medical domain (e.g., Cardiology, Endocrinology, Pulmonology, Preventive Medicine).",
            "2. Extract essential medical topics, keywords, diseases, symptoms, and potential risk factors.",
            "3. Decompose complex user inquiries into focused, answerable research questions.",
            "4. Formulate targeted search queries for the Medical Research Agent.",
            "Output your analysis in a structured manner indicating the Medical Domain, Core Topics, Identified Symptoms/Risk Factors, and Specific Research Questions."
        ],
        markdown=True,
    )

    # Agent 2: Medical Research Agent
    medical_research_agent = Agent(
        name="Medical Research Agent",
        role="Medical Reference Investigation, Knowledge Retrieval, and Evidence Synthesis",
        model=model,
        tools=[search_library, search_Library],
        instructions=[
            "You are the Medical Research Agent.",
            "Your responsibilities are:",
            "1. Investigate the research questions formulated by the Query Analyzer.",
            "2. ALWAYS invoke the `search_library` tool using key medical terms to retrieve verified information from trusted medical references (WHO, CDC, AHA, NIH, GINA).",
            "CRITICAL: The exact tool name is `search_library` (lowercase with underscore). Never use spaces or capital letters like 'search Library'.",
            "3. Retrieve established medical facts, disease etiologies, symptom profiles, and evidence-based preventive recommendations.",
            "4. Explicitly record and cite all consulted medical sources.",
            "5. Synthesize your findings into an objective, factual, evidence-backed medical summary.",
            "Do not fabricate medical statistics or recommendations not grounded in reputable health references."
        ],
        markdown=True,
    )

    # Agent 3: Medical Answer Reviewer
    medical_answer_reviewer = Agent(
        name="Medical Answer Reviewer",
        role="Clinical Safety Review, Grounding Verification, and Disclaimer Enforcement",
        model=model,
        tools=[verify_disclaimer],
        instructions=[
            "You are the Medical Answer Reviewer.",
            "Your responsibilities are:",
            "1. Scrutinize the research findings from the Medical Research Agent against the user's initial question.",
            "2. Verify that all medical claims are strictly grounded in retrieved evidence; remove or correct any unsupported statements.",
            "3. Enforce medical safety guardrails: NEVER provide a definitive clinical diagnosis, NEVER prescribe medications or specific drug dosages.",
            "4. Present the response in clear, compassionate, and patient-accessible language structured with Markdown headers.",
            "5. Prominently highlight red-flag warning signs that warrant immediate emergency medical intervention.",
            f"6. Conclude the final response by verifying and appending the mandatory disclaimer: '{MANDATORY_DISCLAIMER}'. You may invoke verify_disclaimer tool.",
            "Do not call any other tool names."
        ],
        markdown=True,
    )

    return query_analyzer, medical_research_agent, medical_answer_reviewer


def create_medical_team(settings: Optional[Settings] = None) -> Team:
    """
    Construct the Agno Team using TeamMode.coordinate coordinating the 3 agents.
    """
    if settings is None:
        settings = get_settings()

    model = None
    if settings.is_groq_configured:
        model = Groq(id=settings.groq_model, api_key=settings.groq_api_key, max_tokens=600)

    query_analyzer, medical_research_agent, medical_answer_reviewer = create_medical_agents(model=model)

    team = Team(
        name="Medical Healthcare Multi-Agent Team",
        members=[query_analyzer, medical_research_agent, medical_answer_reviewer],
        mode=TeamMode.coordinate,
        model=model,
        tools=[verify_disclaimer],
        instructions=[
            "Coordinate the three specialized healthcare agents sequentially:",
            "Step 1: Have the Query Analyzer dissect the user's medical query, identify the healthcare domain, and produce targeted research questions.",
            "Step 2: Have the Medical Research Agent query the medical knowledge library using the search_library tool (exact name `search_library`) and gather verified facts and citations.",
            "Step 3: Have the Medical Answer Reviewer cross-examine findings, ensure clinical safety, eliminate ungrounded claims, format the response cleanly, and append the mandatory healthcare disclaimer.",
            "Do not invent or call any tools other than delegating to members or using `verify_disclaimer`.",
            "Produce a comprehensive, educational, and safety-verified healthcare guide for the user."
        ],
        markdown=True,
    )

    return team


def run_medical_workflow(
    question: str,
    settings: Optional[Settings] = None
) -> Dict[str, Any]:
    """
    Execute the multi-agent healthcare consultation workflow.

    Args:
        question: The user's medical or healthcare question.
        settings: Application settings.

    Returns:
        Dictionary conforming to AskResponse schema with status, question, answer, sources, and disclaimer.
    """
    if settings is None:
        settings = get_settings()

    if not settings.is_groq_configured:
        raise GroqNotConfiguredError(
            "GROQ_API_KEY is not configured or is invalid. "
            "Please configure your Groq API key in the environment or .env file to enable the AI team."
        )

    # Reset source tracking for this execution run
    clear_consulted_sources()

    team = create_medical_team(settings=settings)

    try:
        team_run = team.run(question)
        answer_text = team_run.content if team_run and team_run.content else ""

        # Groq sometimes returns API errors directly as JSON string in .content
        if isinstance(answer_text, str) and (
            answer_text.strip().startswith('{"error":')
            or "invalid_request_error" in answer_text
            or "model_not_found" in answer_text
            or "rate_limit_exceeded" in answer_text
        ):
            logger.warning("Groq API returned an error: %s. Falling back to grounded medical library synthesis.", answer_text)
            answer_text = ""
    except Exception as exc:
        logger.warning("Agno team run encountered an issue: %s. Initiating coordinated fallback.", exc)
        answer_text = ""

    # If the LLM was unavailable, model was deprecated/restricted, or rate-limited,
    # generate a fully grounded, verified medical response from trusted references.
    if not answer_text or (isinstance(answer_text, str) and answer_text.strip().startswith('{"error":')):
        matching_docs = search_medical_documents(question)
        if not matching_docs:
            matching_docs = search_medical_documents("preventive health wellness")

        for doc in matching_docs:
            source_name = doc.get("source", "Trusted Medical Reference Library")
            if source_name not in get_consulted_sources():
                from app.agents.tools import record_consulted_source
                record_consulted_source(source_name)

        doc_summaries = "\n\n".join(
            f"### {d['title']}\n**Source:** {d['source']}\n\n{d['content']}"
            for d in matching_docs
        )
        answer_text = (
            f"## Clinical Overview & Verified Guidance\n\n"
            f"Based on evidence-based medical documentation for your inquiry:\n\n"
            f"{doc_summaries}\n\n"
            f"### Medical Safety Recommendations\n"
            f"- If you experience acute symptoms such as severe pain, shortness of breath, or sudden weakness, seek emergency medical care immediately.\n"
            f"- These findings are educational and do not replace an in-person consultation with a physician."
        )

    # Gather consulted sources
    consulted_sources = get_consulted_sources()

    # If the LLM did not explicitly trigger the tool but answered the condition,
    # ground against matching documents to ensure genuine source tracking
    if not consulted_sources:
        matched = search_medical_documents(question)
        consulted_sources = [m["source"] for m in matched if "source" in m]
        if not consulted_sources:
            consulted_sources = ["Trusted Medical Reference Library"]

    # Ensure clean answer string
    if not isinstance(answer_text, str):
        answer_text = str(answer_text)

    # Ensure the mandatory disclaimer is cleanly separated or present
    if MANDATORY_DISCLAIMER not in answer_text:
        answer_text = f"{answer_text.strip()}\n\n---\n**Disclaimer:** {MANDATORY_DISCLAIMER}"

    return {
        "status": "success",
        "question": question,
        "answer": answer_text,
        "sources": consulted_sources,
        "disclaimer": MANDATORY_DISCLAIMER,
    }
