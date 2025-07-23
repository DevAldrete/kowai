#!/bin/bash

# KowAI Backend Development Startup Script
set -e

echo "🚀 Starting KowAI Backend Development Environment..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install uv first:"
    echo "curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Sync dependencies with uv (including dev dependencies for development)
echo "📋 Syncing dependencies with uv..."
uv sync --group dev

# Activate virtual environment created by uv
echo "🔧 Activating uv virtual environment..."
source .venv/bin/activate

# Set up environment variables if .env doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️ Creating default .env file..."
    cat > .env << EOL
# Database
DATABASE_URL=mysql+aiomysql://user:password@localhost:3306/kowai

# Security
SECRET_KEY=dev-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Appwrite
APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=your-project-id
APPWRITE_API_KEY=your-api-key

# AI Services
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key

# Prefect
PREFECT_API_URL=http://localhost:4200/api

# Redis
REDIS_URL=redis://localhost:6379

# Logging
LOG_LEVEL=INFO

# Development
DEBUG=true
EOL
    echo "✅ Default .env file created. Please update with your credentials."
fi

# Start the development server
echo "🌟 Starting FastAPI development server..."
echo "🌍 Server will be available at: http://localhost:8000"
echo "📖 API documentation at: http://localhost:8000/docs"
echo "🔍 Health check at: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"

uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000