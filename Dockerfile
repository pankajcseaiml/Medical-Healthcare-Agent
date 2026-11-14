# Multi-Stage Optimized Dockerfile for Medical Healthcare Multi-Agent Assistant
# Build Stage: Python 3.11 slim for minimal footprint and security hardening

FROM python:3.11-slim AS builder

WORKDIR /app

# Prevent Python from writing .pyc files and buffer outputs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install application dependencies in wheel cache
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --user --no-cache-dir -r requirements.txt


# Final Runtime Stage
FROM python:3.11-slim AS runner

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/appuser/.local/bin:$PATH" \
    HOST=0.0.0.0 \
    PORT=8000

# Create dedicated non-root user and group for container security
RUN groupadd -g 1001 appgroup && \
    useradd -u 1001 -g appgroup -m -s /bin/bash appuser

# Copy installed python packages from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy application source code and configurations with appropriate ownership
COPY --chown=appuser:appgroup app /app/app
COPY --chown=appuser:appgroup streamlit_app.py /app/streamlit_app.py
COPY --chown=appuser:appgroup .env.example /app/.env.example

# Set directory permissions
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose FastAPI application port
EXPOSE 8000

# Container healthcheck using standard library urllib
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')" || exit 1

# Start the FastAPI service using Uvicorn
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
