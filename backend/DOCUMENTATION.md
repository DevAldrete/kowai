# KowAI Backend Architecture Documentation

## Table of Contents
1. [Overview](#overview)
2. [Technology Stack](#technology-stack)
3. [Architecture Design](#architecture-design)
4. [Layer Details](#layer-details)
5. [Security Architecture](#security-architecture)
6. [AI/Agent Integration](#aiagent-integration)
7. [Database Design](#database-design)
8. [Logging & Monitoring](#logging--monitoring)
9. [Docker Configuration](#docker-configuration)
10. [Development Setup](#development-setup)
11. [API Documentation](#api-documentation)
12. [Testing Strategy](#testing-strategy)
13. [Deployment](#deployment)
14. [Best Practices](#best-practices)

## Overview

KowAI Backend is a modern, AI-powered backend service built with a layered architecture that prioritizes security, scalability, and maintainability. The system integrates multiple cutting-edge technologies to provide a robust foundation for AI-driven applications.

### Key Features
- **Secure Authentication**: JWT-based auth with Appwrite SDK integration
- **AI Agent Framework**: DSPy-powered modular AI components
- **Workflow Orchestration**: Prefect for complex agentic workflows
- **High Performance**: Async FastAPI with optimized database access
- **Comprehensive Logging**: Structured logging with correlation tracking
- **Container-Ready**: Docker-based deployment with security hardening

## Technology Stack

### Core Framework
- **FastAPI**: High-performance web framework for building APIs
- **Python 3.12+**: Modern Python runtime with async support
- **Uvicorn**: ASGI server for production deployment

### AI/Agent Technologies
- **DSPy**: Framework for programming language models with optimization
- **Prefect**: Workflow orchestration for complex agentic workflows
- **LiteLLM**: Language model integration and management

### Backend Services
- **Appwrite SDK**: Backend-as-a-Service for authentication and user management
- **SQLAlchemy**: ORM with async support for database operations
- **Alembic**: Database migration management
- **MariaDB**: Primary relational database

### Infrastructure
- **Docker**: Containerization and deployment
- **Redis**: Caching and message queue
- **Nginx**: Load balancer and reverse proxy (production)

## Architecture Design

### Layered Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                  Presentation Layer                          │
│                   (FastAPI Routes)                          │
├─────────────────────────────────────────────────────────────┤
│                   Security Layer                            │
│              (Auth, RBAC, Middleware)                       │
├─────────────────────────────────────────────────────────────┤
│                Business Logic Layer                         │
│                 (Domain Services)                           │
├─────────────────────────────────────────────────────────────┤
│                  AI/Agent Layer                             │
│               (DSPy + Prefect)                              │
├─────────────────────────────────────────────────────────────┤
│                Data Access Layer                            │
│            (SQLAlchemy Repositories)                        │
├─────────────────────────────────────────────────────────────┤
│               Infrastructure Layer                          │
│         (Appwrite, External Services)                       │
└─────────────────────────────────────────────────────────────┘
```

### Directory Structure

```
backend/
├── app/
│   ├── main.py                    # FastAPI application entry point
│   ├── config.py                  # Configuration management
│   ├── api/                       # Presentation Layer
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── auth/              # Authentication endpoints
│   │   │   ├── chat/              # Chat API routes
│   │   │   ├── agents/            # AI agent management
│   │   │   └── workflows/         # Workflow endpoints
│   │   ├── dependencies/          # FastAPI dependencies
│   │   └── middleware/            # Custom middleware
│   ├── core/                      # Cross-cutting concerns
│   │   ├── __init__.py
│   │   ├── security/              # Security utilities
│   │   │   ├── auth.py           # JWT authentication
│   │   │   ├── authorization.py  # RBAC implementation
│   │   │   └── middleware.py     # Security middleware
│   │   ├── config/               # Configuration
│   │   ├── logging/              # Logging configuration
│   │   └── exceptions/           # Exception handling
│   ├── services/                 # Business Logic Layer
│   │   ├── __init__.py
│   │   ├── auth/                 # Authentication services
│   │   ├── chat/                 # Chat services
│   │   ├── agents/               # AI agent services
│   │   ├── workflows/            # Workflow services
│   │   └── notifications/        # Notification services
│   ├── ai/                       # AI/Agent Layer
│   │   ├── __init__.py
│   │   ├── dspy/                 # DSPy modules
│   │   │   ├── modules/          # DSPy AI modules
│   │   │   ├── signatures/       # Input/output signatures
│   │   │   └── optimizers/       # Model optimization
│   │   ├── prefect/              # Prefect flows
│   │   │   ├── flows/            # Workflow definitions
│   │   │   ├── tasks/            # Atomic workflow tasks
│   │   │   └── deployments/      # Workflow deployments
│   │   └── agents/               # Agent implementations
│   │       ├── chat/             # Chat AI agents
│   │       ├── analysis/         # Analysis agents
│   │       └── orchestration/    # Agent coordination
│   ├── database/                 # Data Access Layer
│   │   ├── __init__.py
│   │   ├── models/               # SQLAlchemy models
│   │   ├── repositories/         # Repository pattern
│   │   ├── connection.py         # Database connection
│   │   └── base.py               # Base model classes
│   └── infrastructure/           # Infrastructure Layer
│       ├── __init__.py
│       ├── appwrite/             # Appwrite SDK integration
│       ├── storage/              # File storage services
│       ├── external/             # External API integrations
│       └── monitoring/           # Health checks and metrics
├── tests/                        # Test suite
│   ├── unit/                     # Unit tests
│   ├── integration/              # Integration tests
│   ├── ai/                       # AI module tests
│   ├── workflows/                # Prefect workflow tests
│   └── fixtures/                 # Test data and mocks
├── alembic/                      # Database migrations
│   ├── versions/                 # Migration scripts
│   └── env.py                    # Alembic configuration
├── docker/                       # Docker configuration
│   ├── Dockerfile                # Main application container
│   ├── Dockerfile.worker         # Prefect worker container
│   └── docker-compose.yml        # Development environment
├── requirements/                 # Python dependencies
│   ├── base.txt                  # Base requirements
│   ├── dev.txt                   # Development requirements
│   └── prod.txt                  # Production requirements
├── scripts/                      # Utility scripts
│   ├── start.sh                  # Development startup
│   └── migrate.sh                # Database migration
└── pyproject.toml               # Python project configuration
```

## Layer Details

### 1. Presentation Layer (FastAPI)

**Purpose**: Handle HTTP requests, validate input, and format responses.

**Key Components**:
- **API Routes**: RESTful endpoints organized by domain
- **Pydantic Models**: Request/response validation and serialization
- **Middleware**: CORS, rate limiting, request logging
- **Dependencies**: Dependency injection for services

**Example Route Structure**:
```python
# app/api/v1/chat/routes.py
from fastapi import APIRouter, Depends, HTTPException
from app.services.chat import ChatService
from app.core.security import get_current_user

router = APIRouter()

@router.post("/chat/message")
async def send_message(
    message: ChatMessageRequest,
    current_user: User = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service)
):
    response = await chat_service.process_message(
        user_id=current_user.id,
        message=message.content
    )
    return ChatMessageResponse(response=response)
```

### 2. Security Layer

**Purpose**: Authenticate users, authorize access, and protect against security threats.

**Key Components**:
- **JWT Authentication**: Token validation and user identification
- **Role-Based Access Control**: Permission-based authorization
- **Input Validation**: Sanitization and validation of user input
- **Rate Limiting**: API throttling and abuse prevention

**Authentication Flow**:
```python
# app/core/security/auth.py
from fastapi import Depends, HTTPException, status
from app.infrastructure.appwrite import AppwriteClient

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    appwrite_client: AppwriteClient = Depends(get_appwrite_client)
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        user = await appwrite_client.get_user(user_id)
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
```

### 3. Business Logic Layer

**Purpose**: Implement domain logic, business rules, and use cases.

**Key Components**:
- **Domain Services**: Core business logic implementation
- **Use Cases**: Application-specific business operations
- **Data Transformation**: Convert between domain and external formats
- **Business Rules**: Validation and enforcement of business constraints

**Service Example**:
```python
# app/services/chat/chat_service.py
from app.ai.dspy.modules import ChatModule
from app.database.repositories import ChatRepository

class ChatService:
    def __init__(
        self,
        chat_repository: ChatRepository,
        chat_module: ChatModule
    ):
        self.chat_repository = chat_repository
        self.chat_module = chat_module

    async def process_message(self, user_id: str, message: str) -> str:
        # Business logic: validate, process, and store
        chat_history = await self.chat_repository.get_user_history(user_id)
        
        # AI processing with DSPy
        response = self.chat_module(
            message=message,
            history=chat_history
        ).response
        
        # Store conversation
        await self.chat_repository.save_conversation(
            user_id=user_id,
            message=message,
            response=response
        )
        
        return response
```

### 4. AI/Agent Layer

**Purpose**: Implement AI agents, orchestrate workflows, and optimize AI models.

#### DSPy Integration

**DSPy Modules**:
```python
# app/ai/dspy/modules/chat_module.py
import dspy

class ChatModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.generate_response = dspy.ChainOfThought("message, history -> response")
    
    def forward(self, message: str, history: str) -> dspy.Prediction:
        prediction = self.generate_response(
            message=message,
            history=history
        )
        return prediction
```

**DSPy Signatures**:
```python
# app/ai/dspy/signatures/chat_signatures.py
import dspy

class ChatSignature(dspy.Signature):
    """Generate a helpful response to a user message given chat history."""
    
    message: str = dspy.InputField(desc="User's message")
    history: str = dspy.InputField(desc="Previous conversation history")
    response: str = dspy.OutputField(desc="AI assistant response")
```

#### Prefect Workflow Integration

**Workflow Definition**:
```python
# app/ai/prefect/flows/analysis_flow.py
from prefect import flow, task
from app.ai.dspy.modules import AnalysisModule

@task
async def analyze_data(data: dict) -> dict:
    analyzer = AnalysisModule()
    return analyzer(data=data).analysis

@task
async def generate_report(analysis: dict) -> str:
    report_generator = ReportModule()
    return report_generator(analysis=analysis).report

@flow
async def complex_analysis_workflow(user_id: str, data: dict):
    analysis = await analyze_data(data)
    report = await generate_report(analysis)
    
    # Store results
    await store_analysis_results(user_id, analysis, report)
    
    return {
        "analysis": analysis,
        "report": report
    }
```

### 5. Data Access Layer

**Purpose**: Manage data persistence, queries, and database operations.

**Key Components**:
- **SQLAlchemy Models**: Database entity definitions
- **Repository Pattern**: Data access abstraction
- **Connection Management**: Database connection pooling
- **Migration Management**: Schema versioning with Alembic

**Model Example**:
```python
# app/database/models/chat.py
from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class ChatConversation(Base):
    __tablename__ = "chat_conversations"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="conversations")
```

**Repository Pattern**:
```python
# app/database/repositories/chat_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import ChatConversation

class ChatRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def save_conversation(
        self, 
        user_id: str, 
        message: str, 
        response: str
    ) -> ChatConversation:
        conversation = ChatConversation(
            user_id=user_id,
            message=message,
            response=response
        )
        self.session.add(conversation)
        await self.session.commit()
        return conversation
    
    async def get_user_history(self, user_id: str) -> list[ChatConversation]:
        result = await self.session.execute(
            select(ChatConversation)
            .where(ChatConversation.user_id == user_id)
            .order_by(ChatConversation.created_at.desc())
            .limit(10)
        )
        return result.scalars().all()
```

### 6. Infrastructure Layer

**Purpose**: Integrate with external services and manage infrastructure concerns.

**Appwrite Integration**:
```python
# app/infrastructure/appwrite/client.py
from appwrite.client import Client
from appwrite.services.account import Account
from appwrite.services.users import Users

class AppwriteClient:
    def __init__(self, endpoint: str, project_id: str, api_key: str):
        self.client = Client()
        self.client.set_endpoint(endpoint)
        self.client.set_project(project_id)
        self.client.set_key(api_key)
        
        self.account = Account(self.client)
        self.users = Users(self.client)
    
    async def get_user(self, user_id: str):
        return await self.users.get(user_id)
    
    async def validate_session(self, session_id: str):
        return await self.account.get_session(session_id)
```

## Security Architecture

### Authentication Flow

1. **User Login**: Client authenticates with Appwrite
2. **JWT Token**: Appwrite returns JWT token
3. **Token Validation**: FastAPI middleware validates token
4. **User Context**: User information attached to request
5. **Authorization**: RBAC checks for resource access

### JWT Token Structure

```json
{
  "iss": "appwrite",
  "sub": "user_id",
  "aud": "kowai",
  "exp": 1641234567,
  "iat": 1641230967,
  "roles": ["user", "premium"],
  "session_id": "session_123"
}
```

### Role-Based Access Control

**Permission Decorator**:
```python
# app/core/security/authorization.py
from functools import wraps
from fastapi import HTTPException, status

def require_roles(*roles):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            user_roles = set(current_user.roles)
            required_roles = set(roles)
            
            if not user_roles.intersection(required_roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator
```

**Usage Example**:
```python
@router.delete("/admin/users/{user_id}")
@require_roles("admin", "moderator")
async def delete_user(
    user_id: str,
    current_user: User = Depends(get_current_user)
):
    # Admin-only functionality
    pass
```

### Security Best Practices

1. **Input Validation**: All inputs validated with Pydantic
2. **SQL Injection Prevention**: Parameterized queries only
3. **XSS Protection**: Output encoding and CSP headers
4. **Rate Limiting**: Per-user and per-endpoint limits
5. **CORS Configuration**: Strict origin and method controls
6. **Secure Headers**: HSTS, X-Frame-Options, etc.

## AI/Agent Integration

### DSPy Framework Integration

**Core Concepts**:
- **Modules**: Reusable AI components with input/output signatures
- **Signatures**: Define the interface for AI operations
- **Optimizers**: Automatic prompt and weight optimization
- **Compilation**: Convert modules to optimized implementations

**Module Development Pattern**:
```python
# app/ai/dspy/modules/base_module.py
import dspy
from abc import ABC, abstractmethod

class BaseAIModule(dspy.Module, ABC):
    def __init__(self):
        super().__init__()
        self.setup_module()
    
    @abstractmethod
    def setup_module(self):
        """Setup module-specific components"""
        pass
    
    @abstractmethod
    def forward(self, **kwargs) -> dspy.Prediction:
        """Forward pass implementation"""
        pass
```

**Advanced Chat Module**:
```python
# app/ai/dspy/modules/advanced_chat_module.py
class AdvancedChatModule(BaseAIModule):
    def setup_module(self):
        self.context_analyzer = dspy.ChainOfThought(
            "message, history -> context_analysis"
        )
        self.response_generator = dspy.ChainOfThought(
            "message, context_analysis -> response"
        )
        self.quality_checker = dspy.ChainOfThought(
            "response, message -> quality_score"
        )
    
    def forward(self, message: str, history: str) -> dspy.Prediction:
        # Multi-stage processing
        context = self.context_analyzer(
            message=message,
            history=history
        )
        
        response = self.response_generator(
            message=message,
            context_analysis=context.context_analysis
        )
        
        quality = self.quality_checker(
            response=response.response,
            message=message
        )
        
        return dspy.Prediction(
            response=response.response,
            context_analysis=context.context_analysis,
            quality_score=quality.quality_score
        )
```

### Prefect Workflow Integration

**Complex Agent Workflow**:
```python
# app/ai/prefect/flows/agent_workflow.py
from prefect import flow, task
from prefect.task_runners import ConcurrentTaskRunner
from app.ai.dspy.modules import ChatModule, AnalysisModule

@task
async def process_user_message(message: str, user_id: str) -> dict:
    chat_module = ChatModule()
    response = chat_module(message=message)
    return {
        "user_id": user_id,
        "response": response.response,
        "confidence": response.confidence
    }

@task
async def analyze_conversation(conversation_data: dict) -> dict:
    analysis_module = AnalysisModule()
    analysis = analysis_module(conversation=conversation_data)
    return analysis.analysis

@task
async def update_user_profile(user_id: str, analysis: dict):
    # Update user preferences based on conversation analysis
    pass

@flow(task_runner=ConcurrentTaskRunner())
async def intelligent_chat_flow(message: str, user_id: str):
    # Process message and analyze in parallel
    chat_response = await process_user_message(message, user_id)
    analysis = await analyze_conversation(chat_response)
    
    # Update user profile based on analysis
    await update_user_profile(user_id, analysis)
    
    return {
        "response": chat_response["response"],
        "analysis": analysis
    }
```

## Database Design

### Connection Management

**Async Database Configuration**:
```python
# app/database/connection.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600
)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
```

### Migration Management

**Alembic Configuration**:
```python
# alembic/env.py
from alembic import context
from app.database.models import Base

def run_migrations_online():
    connectable = create_async_engine(DATABASE_URL)
    
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=Base.metadata,
        compare_type=True,
        compare_server_default=True
    )
    
    with context.begin_transaction():
        context.run_migrations()
```

**Migration Commands**:
```bash
# Create new migration
alembic revision --autogenerate -m "Add chat tables"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Logging & Monitoring

### Structured Logging Configuration

**Logger Setup**:
```python
# app/core/logging/config.py
import logging
import json
from datetime import datetime
from contextvars import ContextVar

correlation_id: ContextVar[str] = ContextVar('correlation_id')

class StructuredFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "module": record.name,
            "message": record.getMessage(),
            "correlation_id": correlation_id.get(None)
        }
        
        if hasattr(record, 'user_id'):
            log_entry["user_id"] = record.user_id
        
        if hasattr(record, 'execution_time'):
            log_entry["execution_time"] = record.execution_time
        
        return json.dumps(log_entry)

def setup_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(StructuredFormatter())
    
    logger = logging.getLogger("kowai")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    return logger
```

**Logging Middleware**:
```python
# app/core/middleware/logging_middleware.py
import time
import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Generate correlation ID
        correlation_id.set(str(uuid.uuid4()))
        
        start_time = time.time()
        
        # Log request
        logger.info(
            f"Request: {request.method} {request.url.path}",
            extra={
                "request_method": request.method,
                "request_path": request.url.path,
                "user_agent": request.headers.get("user-agent")
            }
        )
        
        response = await call_next(request)
        
        # Log response
        execution_time = time.time() - start_time
        logger.info(
            f"Response: {response.status_code}",
            extra={
                "response_status": response.status_code,
                "execution_time": execution_time
            }
        )
        
        return response
```

### Monitoring Integration

**Health Check Endpoint**:
```python
# app/api/v1/health.py
from fastapi import APIRouter, Depends
from app.database.connection import get_db
from app.infrastructure.appwrite import get_appwrite_client

router = APIRouter()

@router.get("/health")
async def health_check(
    db: AsyncSession = Depends(get_db),
    appwrite_client = Depends(get_appwrite_client)
):
    checks = {
        "database": await check_database_health(db),
        "appwrite": await check_appwrite_health(appwrite_client),
        "ai_services": await check_ai_services_health()
    }
    
    status = "healthy" if all(checks.values()) else "unhealthy"
    
    return {
        "status": status,
        "checks": checks,
        "timestamp": datetime.utcnow().isoformat()
    }
```

## Docker Configuration

### Multi-stage Dockerfile

```dockerfile
# docker/Dockerfile
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements/prod.txt .
RUN pip install --no-cache-dir --user -r prod.txt

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Copy Python packages from builder stage
COPY --from=builder /root/.local /root/.local

# Create non-root user
RUN adduser --disabled-password --no-create-home appuser

# Copy application code
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini ./

# Set ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Update PATH
ENV PATH=/root/.local/bin:$PATH

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose Configuration

```yaml
# docker/docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=mysql+aiomysql://user:password@mariadb:3306/kowai
      - APPWRITE_ENDPOINT=https://your-appwrite-instance.appwrite.io/v1
      - APPWRITE_PROJECT_ID=your-project-id
    depends_on:
      - mariadb
      - redis
    volumes:
      - ../app:/app/app
    networks:
      - kowai-network

  worker:
    build:
      context: ..
      dockerfile: docker/Dockerfile.worker
    environment:
      - PREFECT_API_URL=http://prefect:4200/api
    depends_on:
      - app
      - prefect
    networks:
      - kowai-network

  mariadb:
    image: mariadb:10.11
    environment:
      - MYSQL_ROOT_PASSWORD=rootpassword
      - MYSQL_DATABASE=kowai
      - MYSQL_USER=user
      - MYSQL_PASSWORD=password
    volumes:
      - mariadb_data:/var/lib/mysql
    networks:
      - kowai-network

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    networks:
      - kowai-network

  prefect:
    image: prefecthq/prefect:2-python3.11
    command: prefect server start --host 0.0.0.0
    ports:
      - "4200:4200"
    environment:
      - PREFECT_API_URL=http://0.0.0.0:4200/api
    networks:
      - kowai-network

volumes:
  mariadb_data:
  redis_data:

networks:
  kowai-network:
    driver: bridge
```

## Development Setup

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- MariaDB client (optional)
- Redis client (optional)

### Local Development Setup

1. **Clone Repository**:
   ```bash
   git clone <repository-url>
   cd kowai/backend
   ```

2. **Create Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements/dev.txt
   ```

4. **Environment Configuration**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Start Services**:
   ```bash
   docker-compose -f docker/docker-compose.dev.yml up -d
   ```

6. **Run Database Migrations**:
   ```bash
   alembic upgrade head
   ```

7. **Start Development Server**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Environment Variables

```bash
# Database
DATABASE_URL=mysql+aiomysql://user:password@localhost:3306/kowai

# Appwrite
APPWRITE_ENDPOINT=https://your-appwrite-instance.appwrite.io/v1
APPWRITE_PROJECT_ID=your-project-id
APPWRITE_API_KEY=your-api-key

# Security
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Services
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key

# Prefect
PREFECT_API_URL=http://localhost:4200/api

# Redis
REDIS_URL=redis://localhost:6379

# Logging
LOG_LEVEL=INFO
```

## API Documentation

### OpenAPI/Swagger Integration

FastAPI automatically generates OpenAPI documentation available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

### API Versioning

```python
# app/api/v1/__init__.py
from fastapi import APIRouter
from app.api.v1 import auth, chat, agents, workflows

api_router = APIRouter()

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

api_router.include_router(
    chat.router,
    prefix="/chat",
    tags=["Chat"]
)

api_router.include_router(
    agents.router,
    prefix="/agents",
    tags=["AI Agents"]
)

api_router.include_router(
    workflows.router,
    prefix="/workflows",
    tags=["Workflows"]
)
```

### Example API Endpoints

#### Authentication
```
POST /api/v1/auth/login
POST /api/v1/auth/logout
POST /api/v1/auth/refresh
GET  /api/v1/auth/me
```

#### Chat
```
POST /api/v1/chat/message
GET  /api/v1/chat/history
POST /api/v1/chat/feedback
```

#### AI Agents
```
GET  /api/v1/agents/
POST /api/v1/agents/
GET  /api/v1/agents/{agent_id}
PUT  /api/v1/agents/{agent_id}
DELETE /api/v1/agents/{agent_id}
```

#### Workflows
```
GET  /api/v1/workflows/
POST /api/v1/workflows/trigger
GET  /api/v1/workflows/{workflow_id}/status
```

## Testing Strategy

### Test Structure

```
tests/
├── conftest.py                # Pytest configuration and fixtures
├── unit/                      # Unit tests
│   ├── test_services/         # Service layer tests
│   ├── test_repositories/     # Repository tests
│   └── test_ai_modules/       # AI module tests
├── integration/               # Integration tests
│   ├── test_api/              # API endpoint tests
│   └── test_workflows/        # Workflow tests
├── fixtures/                  # Test data
│   ├── users.json
│   └── conversations.json
└── utils/                     # Test utilities
    ├── factories.py           # Test data factories
    └── helpers.py             # Test helper functions
```

### Test Configuration

```python
# tests/conftest.py
import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.database.base import Base

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def db_session():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=True
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session
```

### Testing Examples

**Service Unit Test**:
```python
# tests/unit/test_services/test_chat_service.py
import pytest
from unittest.mock import AsyncMock
from app.services.chat import ChatService

@pytest.mark.asyncio
async def test_process_message():
    # Mock dependencies
    mock_repository = AsyncMock()
    mock_ai_module = AsyncMock()
    mock_ai_module.return_value.response = "Test response"
    
    service = ChatService(
        chat_repository=mock_repository,
        chat_module=mock_ai_module
    )
    
    # Test
    result = await service.process_message("user123", "Hello")
    
    # Assertions
    assert result == "Test response"
    mock_repository.save_conversation.assert_called_once()
```

**API Integration Test**:
```python
# tests/integration/test_api/test_chat.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_send_message_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/chat/message",
            json={"content": "Hello, AI!"},
            headers={"Authorization": "Bearer test-token"}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/unit/test_services/test_chat_service.py

# Run with verbose output
pytest -v

# Run integration tests only
pytest tests/integration/
```

## Deployment

### Production Deployment

**Docker Swarm Configuration**:
```yaml
# docker-stack.yml
version: '3.8'

services:
  app:
    image: kowai/backend:latest
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
    environment:
      - DATABASE_URL=mysql+aiomysql://user:password@mariadb:3306/kowai
    networks:
      - kowai-network
    depends_on:
      - mariadb

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    configs:
      - source: nginx_config
        target: /etc/nginx/nginx.conf
    depends_on:
      - app
    networks:
      - kowai-network

configs:
  nginx_config:
    file: ./nginx.conf

networks:
  kowai-network:
    driver: overlay
```

**Kubernetes Deployment**:
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kowai-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: kowai-backend
  template:
    metadata:
      labels:
        app: kowai-backend
    spec:
      containers:
      - name: backend
        image: kowai/backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: kowai-secrets
              key: database-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### CI/CD Pipeline

**GitHub Actions**:
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements/dev.txt
    
    - name: Run tests
      run: |
        pytest --cov=app
    
    - name: Run security scan
      run: |
        bandit -r app/

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker image
      run: |
        docker build -t kowai/backend:${{ github.sha }} .
    
    - name: Push to registry
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker push kowai/backend:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
    - name: Deploy to production
      run: |
        # Deploy to your production environment
        kubectl set image deployment/kowai-backend backend=kowai/backend:${{ github.sha }}
```

## Best Practices

### Code Quality

1. **Type Hints**: Use type hints throughout the codebase
2. **Docstrings**: Document all public functions and classes
3. **Code Formatting**: Use Black for code formatting
4. **Linting**: Use flake8 or ruff for code linting
5. **Import Sorting**: Use isort for import organization

### Security

1. **Input Validation**: Validate all inputs with Pydantic
2. **Authentication**: Always verify user authentication
3. **Authorization**: Implement proper RBAC
4. **Logging**: Log security events without exposing sensitive data
5. **Dependencies**: Keep dependencies updated

### Performance

1. **Database Queries**: Use async queries and proper indexing
2. **Caching**: Implement Redis caching for frequently accessed data
3. **Connection Pooling**: Use connection pooling for database
4. **Async Operations**: Use async/await for I/O operations
5. **Monitoring**: Monitor application performance metrics

### Error Handling

1. **Global Exception Handling**: Implement global exception handlers
2. **Structured Errors**: Return consistent error responses
3. **Logging**: Log errors with context information
4. **User-Friendly Messages**: Provide clear error messages
5. **Retry Logic**: Implement retry mechanisms for transient failures

### AI/ML Operations

1. **Model Versioning**: Track AI model versions
2. **A/B Testing**: Test different AI models in production
3. **Performance Monitoring**: Monitor AI model performance
4. **Fallback Strategies**: Implement fallbacks for AI failures
5. **Cost Optimization**: Monitor and optimize AI service costs

---

*This documentation is maintained by the KowAI development team. For questions or contributions, please refer to our contribution guidelines.*