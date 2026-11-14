"""
FastAPI Backend Application for Medical Healthcare Multi-Agent Assistant.
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.schemas import HealthResponse, AskRequest, AskResponse, ErrorResponse
from app.agents.team import AGENT_NAMES, run_medical_workflow, GroqNotConfiguredError


app = FastAPI(
    title="Medical Healthcare Multi-Agent Assistant",
    description=(
        "An intelligent AI-powered healthcare guidance system coordinating three specialized "
        "AI agents (Query Analyzer, Medical Research Agent, Medical Answer Reviewer) via Agno and Groq."
    ),
    version="1.0.0",
)

# Enable CORS for local testing and web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files directory
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=FileResponse, summary="Serve Web User Interface")
async def serve_homepage():
    """Serve the single-page responsive Medical Healthcare Assistant interface."""
    index_path = os.path.join(STATIC_DIR, "index.html")
    if not os.path.exists(index_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Frontend interface not found at app/static/index.html"
        )
    return FileResponse(index_path)


@app.get("/health", response_model=HealthResponse, summary="Application Health Check")
async def health_check():
    """
    Returns application operational status, model configuration, and registered agent names.
    Does not expose sensitive API keys or credentials.
    """
    settings = get_settings()
    return HealthResponse(
        status="healthy",
        app_name=settings.app_name,
        groq_configured=settings.is_groq_configured,
        model=settings.groq_model,
        agents=AGENT_NAMES,
    )


@app.post(
    "/ask",
    response_model=AskResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input or configuration error"},
        422: {"description": "Validation error for empty or invalid query"},
        503: {"model": ErrorResponse, "description": "Groq API key not configured"},
    },
    summary="Submit Medical Query to Multi-Agent Team"
)
async def ask_question(request: AskRequest):
    """
    Submit a healthcare-related question to the Agno multi-agent team.
    Coordinated through Query Analyzer, Medical Research Agent, and Medical Answer Reviewer.
    """
    settings = get_settings()

    if not settings.is_groq_configured:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="GROQ_API_KEY is not configured. Please set your Groq API key in the environment or .env file."
        )

    try:
        response_data = run_medical_workflow(request.question, settings=settings)
        return AskResponse(**response_data)
    except GroqNotConfiguredError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing healthcare consultation: {str(e)}"
        )
