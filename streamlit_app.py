"""
Streamlit Web Interface for Medical Healthcare Multi-Agent Assistant (Option A).
"""

import streamlit as st
from app.config import get_settings
from app.agents.team import AGENT_NAMES, run_medical_workflow, MANDATORY_DISCLAIMER

st.set_page_config(
    page_title="Medical Healthcare Multi-Agent Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

settings = get_settings()

# Custom CSS styling
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0284c7;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    .disclaimer-card {
        background-color: #fffbeb;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 6px;
        margin-top: 1.5rem;
        font-size: 0.88rem;
        color: #78350f;
    }
    .source-badge {
        display: inline-block;
        background-color: #f0fdf4;
        border: 1px solid #86efac;
        color: #166534;
        border-radius: 12px;
        padding: 4px 12px;
        font-size: 0.85rem;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar
with st.sidebar:
    st.header("🩺 Multi-Agent System")
    st.markdown("**KIT’s College of Engineering (Autonomous)**")
    st.markdown("*Generative & Agentic AI Lab (UAMPC0731)*")
    st.markdown("**External POE – A.Y. 2026–2027**")
    st.divider()

    st.subheader("System Status")
    if settings.is_groq_configured:
        st.success("🟢 Groq API Configured")
    else:
        st.error("🔴 Groq API Not Configured")

    st.info(f"**Model:** `{settings.groq_model}`")
    st.info("**Framework:** Agno (`TeamMode.coordinate`)")

    st.divider()
    st.subheader("Specialized AI Agents")
    for idx, agent_name in enumerate(AGENT_NAMES, 1):
        st.markdown(f"**{idx}. {agent_name}**")

# Main Page
st.markdown('<div class="main-header">🩺 Medical Healthcare Multi-Agent Assistant</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Autonomous multi-agent educational guidance coordinating Query Analyzer, Medical Research Agent, and Medical Answer Reviewer.</div>',
    unsafe_allow_html=True,
)

sample_questions = [
    "What are the common symptoms, causes, and prevention methods of diabetes?",
    "Explain hypertension, risk factors, and lifestyle management using the DASH diet.",
    "What are common asthma triggers, and what are the emergency warning signs?",
    "What are the clinical differences between a common cold and influenza?",
    "What are the warning signs of a heart attack and how can cardiovascular disease be prevented?",
]

selected_prompt = st.selectbox(
    "Select an example healthcare inquiry or type your own below:",
    ["-- Custom Question --"] + sample_questions,
)

default_text = "" if selected_prompt == "-- Custom Question --" else selected_prompt
question_input = st.text_area(
    "Enter your medical or healthcare inquiry:",
    value=default_text,
    height=120,
    placeholder="e.g., What are the symptoms of diabetes and how can it be prevented?",
)

if st.button("Consult Multi-Agent Team", type="primary", use_container_width=True):
    if not question_input.strip() or len(question_input.strip()) < 3:
        st.warning("Please enter a valid question with at least 3 characters.")
    elif not settings.is_groq_configured:
        st.error("Groq API key is not configured. Please set `GROQ_API_KEY` in your `.env` file.")
    else:
        with st.spinner("Coordinating AI agents: Analyzing domain, searching medical library, and reviewing clinical safety..."):
            try:
                response = run_medical_workflow(question_input.strip(), settings=settings)

                st.markdown("### Reviewed Medical Guidance")
                st.markdown(response["answer"])

                st.markdown("### Verified Medical Sources Consulted")
                sources = response.get("sources", [])
                if sources:
                    for src in sources:
                        st.markdown(f'<span class="source-badge">✓ {src}</span>', unsafe_allow_html=True)
                else:
                    st.write("Trusted Medical Reference Library")

                st.markdown(
                    f'<div class="disclaimer-card"><strong>Healthcare Disclaimer:</strong><br>{MANDATORY_DISCLAIMER}</div>',
                    unsafe_allow_html=True,
                )
            except Exception as e:
                st.error(f"Error executing agent workflow: {str(e)}")
