# KIT’s College of Engineering (Autonomous), Kolhapur
## Department of Computer Science & Engineering
### Course Name: Generative and Agentic AI Lab (Course Code: UAMPC0731)
#### External POE – A.Y. 2026–2027
**Assignment No. 10 – Medical Healthcare Multi-Agent Assistant**  
**GenAI & ML DevOps Lab — Containerization**  
**CO:** 3 | **BL:** 5

---

## 1. Project Overview

The **Medical Healthcare Multi-Agent Assistant** is an intelligent AI-powered healthcare guidance system designed to provide users with reliable, understandable, and evidence-based medical information.

The application is built using **Python, FastAPI, Agno Framework, and Groq API**, utilizing fast open-weight models such as LLaMA 3.3.

The system coordinates exactly **three specialized AI agents** through Agno's `Team` framework using `TeamMode.coordinate`. It searches a trusted medical knowledge library for verified information and applies rigorous clinical safety checks and disclaimers before answering user queries.

> **Medical Disclaimer:** This system provides educational and informational healthcare guidance only. It does not replace professional medical consultation, clinical diagnosis, emergency services, or treatment prescribed by qualified healthcare professionals.

---

## 2. Multi-Agent Architecture

The system utilizes Agno's `Team` orchestration in `TeamMode.coordinate`:

```text
+-----------------------------------------------------------+
|                        User Query                         |
|  "What are the symptoms of diabetes and how can it be     |
|   prevented?"                                             |
+-----------------------------+-----------------------------+
                              |
                              v
+-----------------------------------------------------------+
|                   Agno Multi-Agent Team                   |
|                   (TeamMode.coordinate)                   |
|                                                           |
|  1. Query Analyzer                                        |
|  - Identifies primary medical domain                      |
|  - Extracts medical topics, symptoms, and risk factors    |
|  - Formulates targeted research questions                 |
|                             |                             |
|                             v                             |
|  2. Medical Research Agent                                |
|  - Invokes `search_library` tool                          |
|  - Searches trusted medical references (WHO, CDC, AHA)    |
|  - Tracks verified sources consulted                      |
|  - Prepares evidence-based findings summary               |
|                             |                             |
|                             v                             |
|  3. Medical Answer Reviewer                               |
|  - Cross-checks claims against retrieved evidence         |
|  - Enforces safety: prevents diagnosis & prescriptions    |
|  - Highlights emergency warning signs (red flags)         |
|  - Appends mandatory healthcare disclaimer                |
+-----------------------------+-----------------------------+
                              |
                              v
+-----------------------------------------------------------+
|                    Final Reviewed Output                  |
|  + Evidence-Based Educational Guidance                    |
|  + Verified Medical Sources Consulted                     |
|  + Clinical Safety Notes & Red Flag Indicators            |
|  + Mandatory Healthcare Disclaimer                        |
+-----------------------------------------------------------+
```

### Agent Responsibilities

1. **Query Analyzer**: Classifies healthcare domains (e.g., Endocrinology, Cardiology, Pulmonology), extracts keywords and disease concepts, and formulates research questions.
2. **Medical Research Agent**: Queries the medical knowledge library using the registered `search_library` tool, retrieving grounded facts from WHO, CDC, AHA, and NIH references while tracking consulted citations.
3. **Medical Answer Reviewer**: Verifies grounding, removes unsupported assertions, blocks diagnostic/prescriptive output, highlights emergency warnings, and ensures the mandatory disclaimer is attached.

---

## 3. Project Directory Structure

```text
MedicalHealthcareBot/
│
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules for virtual environments and secrets
├── requirements.txt          # Python project dependencies
├── README.md                 # Complete documentation and lab manual
├── streamlit_app.py          # Option A: Streamlit UI implementation
│
├── app/
│   ├── __init__.py           # Application package init
│   ├── config.py             # Pydantic BaseSettings environment configuration
│   ├── main.py               # FastAPI application with REST endpoints
│   ├── schemas.py            # Pydantic request and response schemas
│   │
│   ├── agents/
│   │   ├── __init__.py       # Agents package export
│   │   ├── team.py           # Agno 3-agent team definition & TeamMode.coordinate
│   │   └── tools.py          # search_library tool and source tracking
│   │
│   ├── data/
│   │   ├── __init__.py       # Reference library data package
│   │   └── sample_documents.py # Trusted medical references (WHO, CDC, AHA, GINA)
│   │
│   └── static/
│       ├── index.html        # Modern responsive clinical frontend
│       ├── style.css         # Styling, animations, and accessible typography
│       └── app.js            # Frontend client with live agent stepper animation
│
├── tests/
│   ├── __init__.py           # Test package init
│   ├── test_health.py        # Health check and homepage tests
│   ├── test_validation.py    # Input validation and error handling tests
│   └── test_agents.py        # Agno team coordination, tools, and safety tests
│
├── Dockerfile                # Multi-stage secure container image specification
├── docker-compose.yml        # Multi-container local orchestration
│
├── k8s/
│   ├── configmap.yaml        # Non-sensitive runtime configuration
│   ├── secret.yaml           # Secure API key credential storage
│   ├── deployment.yaml       # Replicas, rolling update, health probes, resources
│   ├── service.yaml          # ClusterIP networking service
│   └── ingress.yaml          # NGINX ingress routing configuration
│
└── .github/
    └── workflows/
        └── ci-cd.yml         # GitHub Actions automated test, build, and publish pipeline
```

---

## 4. Getting Started

### Prerequisites

- Python 3.10 – 3.13
- Docker & Docker Compose
- Free Groq API Key: [https://console.groq.com/keys](https://console.groq.com/keys)
- Git

### 1. Setup Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**On macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Configure `.env` with your Groq API key:
```ini
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
HOST=127.0.0.1
PORT=8000
REQUEST_TIMEOUT=60
```

---

## 5. Running the Application

### Option B: FastAPI Backend & Web Interface (Primary)

Start the server using Uvicorn:
```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Access the interfaces:
- **Web Application:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Interactive Swagger Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Health Check Endpoint:** [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

### Option A: Streamlit Dashboard (Optional)

Run the companion Streamlit user interface:
```bash
streamlit run streamlit_app.py
```
Open [http://localhost:8501](http://localhost:8501).

---

## 6. Running Automated Tests

Run the complete automated test suite using pytest:

```bash
pytest -v
```

The test suite validates:
1. `GET /health` operational status, active model, and registered agent names.
2. `GET /` homepage accessibility and UI rendering.
3. Secret isolation (ensuring API keys and credentials are never leaked).
4. `POST /ask` input validation (rejecting empty strings, whitespace, and short queries with 422).
5. Graceful error handling (503 Service Unavailable when Groq API key is unconfigured).
6. Agno Team creation with `TeamMode.coordinate` and exactly three agents.
7. `search_library` tool execution and document relevance retrieval.
8. Medical source tracking (ensuring only genuinely retrieved sources are returned).
9. Reviewer safety checks and mandatory healthcare disclaimer inclusion.

---

## 7. REST API Endpoints

### 1. `GET /health`
Returns the application's health status, active model, and registered agent information without exposing secrets.

**Response:**
```json
{
  "status": "healthy",
  "app_name": "Medical Healthcare Multi-Agent Assistant",
  "groq_configured": true,
  "model": "llama-3.3-70b-versatile",
  "agents": [
    "Query Analyzer",
    "Medical Research Agent",
    "Medical Answer Reviewer"
  ]
}
```

### 2. `POST /ask`
Submits a healthcare-related question to the Agno multi-agent team.

**Request:**
```json
{
  "question": "What are the common symptoms, causes, and prevention methods of diabetes?"
}
```

**Response:**
```json
{
  "status": "success",
  "question": "What are the common symptoms, causes, and prevention methods of diabetes?",
  "answer": "## Diabetes: Overview\n\nDiabetes is a chronic metabolic condition...",
  "sources": [
    "World Health Organization - Diabetes",
    "Trusted Medical Reference Library"
  ],
  "disclaimer": "Disclaimer: This Medical Healthcare Assistant provides educational and informational guidance only. It does not provide clinical diagnosis or prescribe treatment. Consult a qualified healthcare professional for personal medical advice."
}
```

---

## 8. GenAI + ML DevOps Implementation

### 1. Containerization (Docker)

The provided multi-stage `Dockerfile` implements container security and performance best practices:
- Uses a minimal Python 3.11 slim base image.
- Implements a dedicated non-root user (`appuser`, UID/GID 1001).
- Separates dependency building from the runtime image to reduce image size.
- Includes container healthchecks using standard Python library `urllib`.

Build and run the container locally:
```bash
# Build Docker image
docker build -t medical-healthcare-assistant:latest .

# Run container
docker run -d -p 8000:8000 --env-file .env --name medical_bot medical-healthcare-assistant:latest

# Check container health status
docker ps
```

### 2. Multi-Container Orchestration (Docker Compose)

`docker-compose.yml` provides local orchestration with volume mounts for live reference document updates and restart policies:

```bash
# Start the FastAPI healthcare assistant
docker compose up -d

# Start both FastAPI and optional Streamlit dashboard
docker compose --profile ui-optional up -d

# View live container logs
docker compose logs -f

# Stop containers
docker compose down
```

### 3. Cloud-Native Deployment (Kubernetes)

Deploy the multi-agent assistant to any Kubernetes cluster (Minikube, Kind, GKE, EKS, AKS):

```bash
# 1. Apply runtime configuration and secrets
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml

# 2. Deploy application workload with rolling updates & health probes
kubectl apply -f k8s/deployment.yaml

# 3. Expose service internally
kubectl apply -f k8s/service.yaml

# 4. Configure ingress routing
kubectl apply -f k8s/ingress.yaml

# Verify pod readiness and status
kubectl get pods -l app=medical-healthcare-assistant
kubectl get svc medical-healthcare-service
```

### 4. CI/CD Automation (GitHub Actions)

The `.github/workflows/ci-cd.yml` pipeline automates:
1. Multi-version Python environment setup (3.11 & 3.12).
2. Automated dependency caching and installation.
3. Linting and Python syntax validation (`py_compile`).
4. Automated pytest test execution.
5. Kubernetes manifest dry-run validation (`kubectl apply --dry-run=client -f k8s/`).
6. Docker image building, smoke testing, tagging, and publishing to GitHub Container Registry (GHCR).

### 5. CI/CD Automation (Jenkins Pipeline)

The project includes a production-grade declarative [Jenkinsfile](file:///c:/Users/Pankaj/Documents/Medical%20Healthcare%20Agent/Jenkinsfile) compatible with both Linux and Windows Jenkins agents.

#### Pipeline Stages:
1. **Checkout Code:** Fetches source repository via SCM.
2. **Setup Environment & Dependencies:** Creates a clean Python virtual environment and installs `requirements.txt`.
3. **Lint & Syntax Compilation:** Verifies Python bytecode and syntax across `app/` and `tests/`.
4. **Automated Tests (Pytest):** Runs the test suite and exports test reports to `reports/pytest-results.xml` for Jenkins JUnit test trend charts.
5. **Validate Kubernetes Manifests:** Performs client dry-run validation of `k8s/*.yaml`.
6. **Build Docker Image:** Builds the hardened, multi-stage container image tagged with `BUILD_NUMBER` and `latest`.
7. **Container Smoke Test:** Spins up an isolated container, probes the `/health` endpoint to ensure zero regression, and cleans up.
8. **Push Image to Registry:** Authenticates with Docker credentials (`docker-hub-credentials`) and publishes the image.
9. **Deploy to Kubernetes:** Deploys updated manifests and verifies rolling update status via `kubectl rollout status`.

#### Setting up in Jenkins:
1. Open Jenkins and create a **New Item** &rarr; select **Pipeline**.
2. Under **Pipeline Definition**, select **Pipeline script from SCM**.
3. Choose **Git**, specify your repository URL, and set the script path to `Jenkinsfile`.
4. (Optional) Add credentials in Jenkins Credentials Manager:
   - `docker-hub-credentials`: Username & Password for Docker Hub / container registry.
   - `groq-api-key`: Secret text for Groq API key.
5. Click **Build with Parameters** and select `DEPLOY_ENV` (`staging`, `production`, or `none`).

---

## 9. Conclusion

The **Medical Healthcare Multi-Agent Assistant** illustrates how modern Agentic AI workflows can be engineered and containerized following ML DevOps best practices. By partitioning clinical inquiry handling into **Analysis**, **Evidence Retrieval**, and **Safety Review**, the application delivers responsible, grounded healthcare guidance while remaining scalable and deployable across modern cloud platforms.
