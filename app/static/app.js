/**
 * Medical Healthcare Multi-Agent Assistant Frontend Client.
 */

document.addEventListener("DOMContentLoaded", () => {
    // DOM Elements
    const queryForm = document.getElementById("query-form");
    const queryInput = document.getElementById("query-input");
    const charCounter = document.getElementById("char-counter");
    const submitBtn = document.getElementById("submit-btn");
    const submitBtnText = document.getElementById("submit-btn-text");
    const clearBtn = document.getElementById("clear-btn");
    const copyBtn = document.getElementById("copy-btn");
    const copyText = document.getElementById("copy-text");
    const printBtn = document.getElementById("print-btn");

    const loadingIndicator = document.getElementById("loading-indicator");
    const loadingPhaseTitle = document.getElementById("loading-phase-title");
    const loadingPhaseDetail = document.getElementById("loading-phase-detail");

    const errorContainer = document.getElementById("error-container");
    const errorTitle = document.getElementById("error-title");
    const errorMessage = document.getElementById("error-message");

    const responseCard = document.getElementById("response-card");
    const responseQuestionEcho = document.getElementById("response-question-echo");
    const answerContent = document.getElementById("answer-content");
    const sourcesList = document.getElementById("sources-list");
    const disclaimerText = document.getElementById("disclaimer-text");

    const systemStatusPill = document.getElementById("system-status-pill");
    const systemStatusText = document.getElementById("system-status-text");
    const activeModelText = document.getElementById("active-model-text");

    const stepAnalyzer = document.getElementById("step-analyzer");
    const stepResearcher = document.getElementById("step-researcher");
    const stepReviewer = document.getElementById("step-reviewer");

    let currentAnswerRawText = "";

    // 1. Fetch System Health on Load
    async function checkSystemHealth() {
        try {
            const res = await fetch("/health");
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            const data = await res.json();

            activeModelText.textContent = data.model || "llama-3.3-70b";

            const dot = systemStatusPill.querySelector(".status-dot");
            if (data.groq_configured) {
                dot.className = "status-dot online";
                systemStatusText.textContent = "AI Agents Ready";
            } else {
                dot.className = "status-dot offline";
                systemStatusText.textContent = "Groq Key Missing";
                showError(
                    "Groq API Key Unconfigured",
                    "The Groq API key is not configured in the application environment (.env). " +
                    "Please set GROQ_API_KEY to enable live multi-agent execution."
                );
            }
        } catch (err) {
            console.error("Health check failed:", err);
            const dot = systemStatusPill.querySelector(".status-dot");
            dot.className = "status-dot offline";
            systemStatusText.textContent = "Service Offline";
        }
    }

    checkSystemHealth();

    // 2. Character Counter
    queryInput.addEventListener("input", () => {
        const len = queryInput.value.length;
        charCounter.textContent = `${len} / 2000`;
    });

    // 3. Suggestion Chips
    document.querySelectorAll(".chip-btn").forEach((btn) => {
        btn.addEventListener("click", () => {
            const text = btn.getAttribute("data-query");
            if (text) {
                queryInput.value = text;
                queryInput.dispatchEvent(new Event("input"));
                queryInput.focus();
            }
        });
    });

    // 4. Clear Button
    clearBtn.addEventListener("click", () => {
        queryInput.value = "";
        queryInput.dispatchEvent(new Event("input"));
        hideError();
        resetStepper();
        queryInput.focus();
    });

    // 5. Copy Answer Button
    copyBtn.addEventListener("click", async () => {
        if (!currentAnswerRawText) return;
        try {
            await navigator.clipboard.writeText(currentAnswerRawText);
            copyText.textContent = "Copied!";
            setTimeout(() => {
                copyText.textContent = "Copy";
            }, 2000);
        } catch (err) {
            console.error("Copy failed:", err);
        }
    });

    // 6. Print Button
    printBtn.addEventListener("click", () => {
        window.print();
    });

    // 7. Multi-Agent Stepper Animation Helpers
    function setStepState(stepElement, state) {
        stepElement.classList.remove("active", "completed");
        if (state === "active") stepElement.classList.add("active");
        if (state === "completed") stepElement.classList.add("completed");
    }

    function resetStepper() {
        setStepState(stepAnalyzer, "");
        setStepState(stepResearcher, "");
        setStepState(stepReviewer, "");
    }

    function showError(title, msg) {
        errorTitle.textContent = title;
        errorMessage.textContent = msg;
        errorContainer.classList.remove("hidden");
    }

    function hideError() {
        errorContainer.classList.add("hidden");
    }

    // 8. Form Submission & Agent Team Coordination
    queryForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const question = queryInput.value.trim();

        if (!question || question.length < 3) {
            showError("Invalid Input", "Please enter a question with at least 3 characters.");
            return;
        }

        // Reset UI state
        hideError();
        responseCard.classList.add("hidden");
        loadingIndicator.classList.remove("hidden");
        submitBtn.disabled = true;
        submitBtnText.textContent = "Coordinating Agents...";

        // Step 1: Query Analyzer
        setStepState(stepAnalyzer, "active");
        setStepState(stepResearcher, "");
        setStepState(stepReviewer, "");
        loadingPhaseTitle.textContent = "Agent 1: Query Analyzer Running...";
        loadingPhaseDetail.textContent = "Classifying medical domain, identifying symptoms, and decomposing questions.";

        // Simulate progressive agent activity feedback while waiting for response
        const phaseTimer1 = setTimeout(() => {
            setStepState(stepAnalyzer, "completed");
            setStepState(stepResearcher, "active");
            loadingPhaseTitle.textContent = "Agent 2: Medical Research Agent Running...";
            loadingPhaseDetail.textContent = "Searching knowledge library and retrieving verified medical references.";
        }, 1200);

        const phaseTimer2 = setTimeout(() => {
            setStepState(stepResearcher, "completed");
            setStepState(stepReviewer, "active");
            loadingPhaseTitle.textContent = "Agent 3: Medical Answer Reviewer Running...";
            loadingPhaseDetail.textContent = "Verifying safety bounds, grounding claims, and applying disclaimers.";
        }, 2600);

        try {
            const response = await fetch("/ask", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ question }),
            });

            clearTimeout(phaseTimer1);
            clearTimeout(phaseTimer2);

            const data = await response.json();

            if (!response.ok) {
                const detail = data.detail || "Failed to process question.";
                throw new Error(detail);
            }

            // Mark all agent steps as completed
            setStepState(stepAnalyzer, "completed");
            setStepState(stepResearcher, "completed");
            setStepState(stepReviewer, "completed");

            // Render Results
            currentAnswerRawText = data.answer || "";
            responseQuestionEcho.textContent = data.question || question;

            // Render Markdown
            if (window.marked && typeof window.marked.parse === "function") {
                answerContent.innerHTML = window.marked.parse(data.answer);
            } else {
                answerContent.textContent = data.answer;
            }

            // Render Sources
            sourcesList.innerHTML = "";
            const sources = data.sources && data.sources.length > 0
                ? data.sources
                : ["Trusted Medical Reference Library"];

            sources.forEach((source) => {
                const tag = document.createElement("span");
                tag.className = "source-tag";
                tag.innerHTML = `
                    <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="20 6 9 17 4 12"/>
                    </svg>
                    ${escapeHtml(source)}
                `;
                sourcesList.appendChild(tag);
            });

            // Disclaimer
            disclaimerText.textContent = data.disclaimer || "Disclaimer: Educational healthcare guidance only.";

            // Show response card
            responseCard.classList.remove("hidden");
            responseCard.scrollIntoView({ behavior: "smooth", block: "start" });
        } catch (err) {
            console.error("Consultation error:", err);
            resetStepper();
            showError("Consultation Error", err.message || "An unexpected error occurred during agent coordination.");
        } finally {
            loadingIndicator.classList.add("hidden");
            submitBtn.disabled = false;
            submitBtnText.textContent = "Consult AI Medical Team";
        }
    });

    function escapeHtml(text) {
        const div = document.createElement("div");
        div.textContent = text;
        return div.innerHTML;
    }
});
