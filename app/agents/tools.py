"""
Medical Knowledge Library Search Tool.
Provides evidence-based medical reference document search and source tracking for agents.
"""

import re
import contextvars
from typing import List, Dict, Any, Optional
from app.data.sample_documents import MEDICAL_DOCUMENTS

# Thread-safe / async-safe tracking of sources consulted during a request run
_consulted_sources_ctx: contextvars.ContextVar[List[str]] = contextvars.ContextVar(
    "consulted_sources", default=[]
)


def get_consulted_sources() -> List[str]:
    """Retrieve the unique list of medical sources consulted in current context."""
    return list(dict.fromkeys(_consulted_sources_ctx.get()))


def record_consulted_source(source: str) -> None:
    """Record a verified medical source as consulted."""
    current = list(_consulted_sources_ctx.get())
    if source and source not in current:
        current.append(source)
        _consulted_sources_ctx.set(current)


def clear_consulted_sources() -> None:
    """Reset consulted sources for a fresh query context."""
    _consulted_sources_ctx.set([])


def search_medical_documents(query: str, max_results: int = 2) -> List[Dict[str, Any]]:
    """
    Search sample medical reference library using weighted keyword and text relevance.
    Returns matching documents sorted by relevance score.
    """
    if not query or not query.strip():
        return []

    tokens = [t.lower() for t in re.findall(r"\b\w{3,}\b", query.lower())]
    if not tokens:
        return []

    scored_docs = []
    for doc in MEDICAL_DOCUMENTS:
        score = 0
        doc_title_lower = doc["title"].lower()
        doc_category_lower = doc["category"].lower()
        doc_content_lower = doc["content"].lower()
        doc_keywords = [k.lower() for k in doc.get("keywords", [])]

        for token in tokens:
            # High weight for keyword matches
            if any(token in kw for kw in doc_keywords):
                score += 5
            # High weight for title matches
            if token in doc_title_lower:
                score += 4
            # Medium weight for category matches
            if token in doc_category_lower:
                score += 3
            # Low weight for content occurrences
            if token in doc_content_lower:
                score += 1

        if score > 0:
            scored_docs.append((score, doc))

    # Sort by descending score
    scored_docs.sort(key=lambda x: x[0], reverse=True)

    results = [doc for _, doc in scored_docs[:max_results]]

    # If no specific matches scored, but query mentions health/lifestyle, return lifestyle doc
    if not results and any(w in query.lower() for w in ["health", "diet", "lifestyle", "wellness", "prevention", "water"]):
        for doc in MEDICAL_DOCUMENTS:
            if doc["id"] == "doc_lifestyle_07":
                results.append(doc)
                break

    return results


def search_library(query: str) -> str:
    """
    Search the trusted medical knowledge library for verified medical references,
    clinical guidelines, disease symptoms, causes, and prevention methods.

    Args:
        query: The healthcare topic, disease name, symptom, or research question.

    Returns:
        Structured text containing the verified medical findings, reference content, and sources.
    """
    docs = search_medical_documents(query)

    if not docs:
        return (
            "Medical Knowledge Library Search Result:\n"
            "No specific reference documents matched the exact query. "
            "Please rely on established evidence-based clinical guidelines, and advise "
            "the user to consult a licensed medical provider for diagnostic evaluation."
        )

    formatted_sections = []
    for doc in docs:
        source_name = doc.get("source", "Trusted Medical Reference Library")
        record_consulted_source(source_name)
        formatted_sections.append(
            f"--- Medical Reference Document ---\n"
            f"Title: {doc.get('title')}\n"
            f"Source: {source_name}\n"
            f"Category: {doc.get('category')}\n"
            f"Verified Medical Content:\n{doc.get('content')}\n"
        )

    return (
        f"Retrieved {len(docs)} verified medical reference(s) from the knowledge library:\n\n"
        + "\n\n".join(formatted_sections)
    )


def search_Library(query: str) -> str:
    """
    Search library alias supporting models that capitalize Library.
    """
    return search_library(query)


def verify_disclaimer(text: Optional[str] = None) -> str:
    """
    Verify and return the official mandatory healthcare disclaimer.
    Used by agents and reviewers to validate and append medical disclaimer compliance.

    Args:
        text: Optional context or guidance text to attach the disclaimer to.

    Returns:
        The mandatory medical healthcare disclaimer string.
    """
    disclaimer = (
        "Disclaimer: This Medical Healthcare Assistant provides educational and informational guidance only. "
        "It does not provide clinical diagnosis or prescribe treatment. "
        "Consult a qualified healthcare professional for personal medical advice."
    )
    if text:
        return f"{text.strip()}\n\n---\n**Disclaimer:** {disclaimer}"
    return disclaimer
