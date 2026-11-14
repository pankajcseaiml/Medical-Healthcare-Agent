"""
Pydantic Schemas for Request and Response Models.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class HealthResponse(BaseModel):
    """Health check endpoint response model."""
    status: str = Field(default="healthy", description="Application operational status")
    app_name: str = Field(default="Medical Healthcare Multi-Agent Assistant", description="Application name")
    groq_configured: bool = Field(..., description="Whether a valid Groq API key is configured")
    model: str = Field(..., description="Configured LLM model name")
    agents: List[str] = Field(
        default_factory=lambda: [
            "Query Analyzer",
            "Medical Research Agent",
            "Medical Answer Reviewer"
        ],
        description="Names of registered multi-agent team members"
    )


class AskRequest(BaseModel):
    """User query request model with validation."""
    question: str = Field(
        ...,
        min_length=3,
        max_length=2000,
        description="Healthcare question submitted by the user",
        examples=["What are the common symptoms, causes, and prevention methods of diabetes?"]
    )

    @field_validator("question")
    @classmethod
    def validate_question(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("Question cannot be empty or whitespace only.")
        if len(stripped) < 3:
            raise ValueError("Question must be at least 3 characters long.")
        return stripped


class AskResponse(BaseModel):
    """Healthcare assistant answer response model."""
    status: str = Field(default="success", description="Response status indicator")
    question: str = Field(..., description="Original user question")
    answer: str = Field(..., description="Educational medical guidance generated and reviewed by the team")
    sources: List[str] = Field(
        default_factory=list,
        description="Verified medical sources retrieved and consulted during research"
    )
    disclaimer: str = Field(
        default=(
            "Disclaimer: This Medical Healthcare Assistant provides educational and informational guidance only. "
            "It does not provide clinical diagnosis or prescribe treatment. "
            "Consult a qualified healthcare professional for personal medical advice."
        ),
        description="Mandatory medical and healthcare disclaimer"
    )


class ErrorResponse(BaseModel):
    """Standardized error response model."""
    status: str = Field(default="error")
    detail: str = Field(...)
