# KowAI Backend - Production Dockerfile
FROM python:3.12-slim AS builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
  build-essential \
  curl \
  pkg-config \
  default-libmysqlclient-dev \
  && rm -rf /var/lib/apt/lists/*

# Install uv for faster dependency management
RUN pip install uv

# Copy dependency files
COPY pyproject.toml README.md ./

# Install Python dependencies using uv
RUN uv sync --no-dev

# Production stage
FROM python:3.12-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
  curl \
  default-mysql-client \
  && rm -rf /var/lib/apt/lists/*

# Copy Python environment from builder stage
COPY --from=builder /app/.venv /app/.venv

# Create non-root user with home directory
RUN adduser --disabled-password appuser

# Create cache directory for uv
RUN mkdir -p /home/appuser/.cache/uv && chown -R appuser:appuser /home/appuser

# Copy application code
COPY app/ ./app/
COPY main.py ./

# Set ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Update PATH to use virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Start application
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
