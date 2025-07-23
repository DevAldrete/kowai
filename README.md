# KowAI - Modern AI Chat Application

<div align="center">

![KowAI Logo](https://img.shields.io/badge/KowAI-AI%20Chat%20Platform-4A148C?style=for-the-badge&logo=robot&logoColor=white)

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SvelteKit](https://img.shields.io/badge/SvelteKit-FF3E00?style=flat&logo=svelte&logoColor=white)](https://kit.svelte.dev/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat&logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![DSPy](https://img.shields.io/badge/DSPy-AI%20Framework-purple?style=flat)](https://github.com/stanfordnlp/dspy)

*A sophisticated AI-powered chat application with persona-based AI agents, built with modern technologies and enterprise-grade architecture.*

</div>

## 🌟 Overview

KowAI is a cutting-edge AI chat application that leverages multiple AI providers and persona-based agents to deliver intelligent, context-aware conversations. Built with a microservices architecture, it combines the power of FastAPI, SvelteKit, DSPy, and Prefect to create a scalable, maintainable, and feature-rich platform.

### ✨ Key Features

- 🤖 **Multi-Persona AI Agents** - Assistant, Analyst, Creative, and Technical personas
- 🔄 **Multiple AI Provider Support** - OpenAI, Anthropic, and more
- 🚀 **Real-time Chat Interface** - Responsive and intuitive user experience
- 🔐 **Enterprise Security** - JWT authentication with Appwrite integration
- 📊 **Workflow Orchestration** - Prefect-powered AI workflows
- 🎨 **Modern UI/UX** - Dark mode with glass morphism design
- 📈 **Scalable Architecture** - Docker Swarm for dev, Kubernetes for production
- 🔍 **Comprehensive Monitoring** - Health checks and structured logging

## 🏗️ Architecture

### Technology Stack

#### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** - High-performance async web framework
- **[DSPy](https://github.com/stanfordnlp/dspy)** - AI framework for language model programming
- **[Prefect](https://www.prefect.io/)** - Workflow orchestration for complex AI tasks
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - Modern Python ORM with async support
- **[Appwrite](https://appwrite.io/)** - Backend-as-a-Service for authentication
- **[MariaDB](https://mariadb.org/)** - Reliable relational database
- **[Redis](https://redis.io/)** - In-memory caching and message queuing

#### Frontend
- **[SvelteKit 5](https://kit.svelte.dev/)** - Modern full-stack framework
- **[TailwindCSS 4](https://tailwindcss.com/)** - Utility-first CSS framework
- **[Skeleton UI](https://www.skeleton.dev/)** - Component library for Svelte
- **[Svelte Motion](https://svelte-motion.gradientdescent.de/)** - Smooth animations
- **[TanStack Query](https://tanstack.com/query)** - Data fetching and caching

#### Infrastructure
- **[Docker](https://www.docker.com/)** - Containerization platform
- **[Kubernetes](https://kubernetes.io/)** - Container orchestration
- **[Nginx](https://nginx.org/)** - Load balancer and reverse proxy

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (SvelteKit)                     │
│              TailwindCSS + Skeleton UI                      │
├─────────────────────────────────────────────────────────────┤
│                   API Gateway (FastAPI)                     │
│                Security + Middleware                        │
├─────────────────────────────────────────────────────────────┤
│                  Business Logic Layer                       │
│               Chat + Agents + Workflows                     │
├─────────────────────────────────────────────────────────────┤
│                    AI/Agent Layer                           │
│                  DSPy + Prefect                             │
├─────────────────────────────────────────────────────────────┤
│                  Data Access Layer                          │
│              SQLAlchemy + Repositories                      │
├─────────────────────────────────────────────────────────────┤
│               Infrastructure Layer                          │
│         MariaDB + Redis + Appwrite + AI APIs                │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Docker** 20.10+ with Docker Compose v2
- **Node.js** 18+ (for frontend development)
- **Python** 3.12+ (for backend development)
- **Git**

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd kowai
   ```

2. **Backend Setup**
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env with your API keys and configuration
   docker-compose up -d
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Verify Installation**
   ```bash
   # Backend health check
   curl http://localhost:8000/health
   
   # Frontend
   open http://localhost:5173
   ```

### Environment Configuration

Create a `.env` file in the backend directory with the following variables:

```env
# AI Provider API Keys
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Appwrite Configuration
APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=your_project_id
APPWRITE_API_KEY=your_api_key

# Security
SECRET_KEY=your_secret_key_here

# Database
DATABASE_URL=mysql+aiomysql://kowai_user:kowai_password@localhost:3306/kowai

# Optional: Redis, Prefect, etc.
REDIS_URL=redis://localhost:6379
PREFECT_API_URL=http://localhost:4200/api
```

## 📚 Documentation

### Backend Documentation
- **[Architecture Guide](backend/DOCS_ARQUITECTURE_SUMMARY.md)** - Detailed architecture overview
- **[API Documentation](backend/DOCUMENTATION.md)** - Comprehensive backend docs
- **[Deployment Guide](backend/DEPLOYMENT.md)** - Production deployment instructions
- **[Docker Guide](backend/README.docker.md)** - Docker setup and usage

### API Endpoints

The backend provides RESTful APIs with automatic OpenAPI documentation:

- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Chat API**: `/api/v1/chat/`
- **Agents API**: `/api/v1/agents/`
- **Workflows API**: `/api/v1/workflows/`

### Key Features Implementation

#### AI Personas
The system includes four specialized AI personas:
- **Assistant** - General helpful assistant for everyday tasks
- **Analyst** - Data-driven analyst for insights and patterns  
- **Creative** - Creative thinker for innovative solutions
- **Technical** - Technical expert for implementation details

#### Workflow Orchestration
Prefect-powered workflows handle:
- Sequential message processing
- Batch conversation analysis
- User profile updates
- Periodic analytics

## 🐳 Deployment

### Development (Docker Swarm)
```bash
cd backend
docker swarm init
docker stack deploy -c docker-swarm-dev.yml kowai-dev
```

### Production (Kubernetes)
```bash
cd backend/k8s
kubectl apply -k production/
```

### Services Overview

| Service | Development Port | Production | Description |
|---------|-----------------|------------|-------------|
| Backend API | 8000 | LoadBalancer | FastAPI application |
| Frontend | 5173 | LoadBalancer | SvelteKit application |
| MariaDB | 3306 | ClusterIP | Primary database |
| Redis | 6379 | ClusterIP | Caching layer |
| Prefect UI | 4200 | ClusterIP | Workflow management |

## 🔧 Development

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

### Testing
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm run test
```

### Code Quality
```bash
# Backend linting
cd backend
ruff check .
mypy .

# Frontend linting
cd frontend
npm run lint
npm run format
```

## 🎨 Design System

KowAI features a modern, dark-themed design system:

### Color Palette
- **Primary**: Deep Purple (#4A148C)
- **Background**: Dark Gray (#1A1A1A)
- **Accents**: Electric Blue (#00B4D8), Magenta (#FF00FF)

### Visual Effects
- Gradient overlays (purple to dark)
- Glass morphism for cards and modals
- Neon highlights for important actions
- Subtle grain texture overlay (15% opacity)
- Spotlight highlights on hover

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the `/backend` and `/frontend` README files
- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions

## 🗺️ Roadmap

### Current Status (v1.0.0)
- ✅ Core AI chat functionality
- ✅ Multi-persona system
- ✅ Docker containerization
- ✅ Kubernetes deployment
- ✅ Health monitoring

### Upcoming Features
- 🔄 Stripe subscription integration
- 🔄 Advanced analytics dashboard
- 🔄 Mobile application
- 🔄 Voice chat capabilities
- 🔄 Plugin system

---

<div align="center">

**Built with ❤️ by the KowAI Team**

[Documentation](backend/DOCUMENTATION.md) • [API Docs](http://localhost:8000/docs) • [Contributing](CONTRIBUTING.md) • [License](LICENSE)

</div>