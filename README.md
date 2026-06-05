# AI Agent System - Production Grade

A fully functional autonomous AI Agent built with Python, FastAPI, and LangGraph.

## Architecture Overview

```
┌─────────────────────────────────────────┐
│         Agent Runtime Layer             │
│  ├─ State Management                    │
│  ├─ Context Management                  │
│  ├─ Execution Engine                    │
│  └─ Task Manager                        │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│         Reasoning Layer                 │
│  ├─ Planning                            │
│  ├─ Reflection                          │
│  ├─ Self Correction                     │
│  └─ Goal Tracking                       │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│         Memory Layer                    │
│  ├─ Short Term (Session)                │
│  ├─ Long Term (PostgreSQL)              │
│  ├─ Vector (Qdrant)                     │
│  └─ Semantic Search                     │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│         Tools & Integration Layer       │
│  ├─ Web Search                          │
│  ├─ File Reader                         │
│  ├─ API Caller                          │
│  ├─ Calculator                          │
│  └─ RAG (Document Processing)           │
└─────────────────────────────────────────┘
```

## Project Structure

```
School/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI entry point
│   │   ├── config.py               # Configuration management
│   │   ├── agent/
│   │   │   ├── __init__.py
│   │   │   ├── runtime.py          # Agent runtime engine
│   │   │   ├── state.py            # State management
│   │   │   ├── context.py          # Context management
│   │   │   └── executor.py         # Task execution
│   │   ├── reasoning/
│   │   │   ├── __init__.py
│   │   │   ├── planner.py          # Planning logic
│   │   │   ├── reflection.py       # Reflection mechanism
│   │   │   └── corrector.py        # Self-correction
│   │   ├── memory/
│   │   │   ├── __init__.py
│   │   │   ├── short_term.py       # Session memory
│   │   │   ├── long_term.py        # PostgreSQL storage
│   │   │   ├── vector_store.py     # Qdrant integration
│   │   │   └── semantic_search.py  # Vector search
│   │   ├── tools/
│   │   │   ├── __init__.py
│   │   │   ├── base.py             # Base tool interface
│   │   │   ├── web_search.py       # Web search tool
│   │   │   ├── file_reader.py      # File reading tool
│   │   │   ├── api_caller.py       # HTTP API tool
│   │   │   └── calculator.py       # Math operations tool
│   │   ├── rag/
│   │   │   ├── __init__.py
│   │   │   ├── uploader.py         # Document upload
│   │   │   ├── chunker.py          # Text chunking
│   │   │   ├── embeddings.py       # Embedding generation
│   │   │   └── retrieval.py        # RAG retrieval
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── schemas.py          # Pydantic schemas
│   │   │   └── db.py               # Database models
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py           # API endpoints
│   │   │   └── middleware.py       # Request/response handling
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── logger.py           # Logging setup
│   │       └── validators.py       # Input validation
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py             # Test fixtures
│   │   ├── test_agent_runtime.py
│   │   ├── test_memory.py
│   │   ├── test_tools.py
│   │   ├── test_reasoning.py
│   │   └── test_api.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── README.md
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Tech Stack

- **Backend**: Python 3.11+
- **Framework**: FastAPI
- **Agent Framework**: LangGraph
- **Data Validation**: Pydantic
- **LLM Provider**: OpenRouter
- **Database**: PostgreSQL
- **Vector DB**: Qdrant
- **Containerization**: Docker

## Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- OpenRouter API Key

### Setup

1. Clone and navigate to branch:
```bash
git clone https://github.com/maheshsanger8-debug/School.git
cd School
git checkout agent-v1-foundation
```

2. Create environment file:
```bash
cp backend/.env.example backend/.env
```

3. Update `.env` with your credentials:
```
OPENROUTER_API_KEY=your_key
DATABASE_URL=postgresql://user:password@localhost:5432/agent_db
QDRANT_URL=http://localhost:6333
```

4. Start services:
```bash
docker-compose up -d
```

5. Run tests:
```bash
cd backend && pytest
```

6. Start agent:
```bash
python -m app.main
```

## Module Progress

- [x] **Phase 1**: Agent Runtime & State Management
- [ ] **Phase 2**: Memory System (Short/Long/Vector)
- [ ] **Phase 3**: Reasoning Engine
- [ ] **Phase 4**: Tools Integration
- [ ] **Phase 5**: RAG Pipeline
- [ ] **Phase 6**: Multi-Agent System
- [ ] **Phase 7**: API & Deployment
- [ ] **Phase 8**: Testing & Documentation
- [ ] **Phase 9**: Frontend (Next.js)

## Documentation

Each module includes:
- Inline code documentation
- Unit tests
- Integration tests
- API documentation
- Usage examples

## Contributing

All code is production-grade with:
- Type hints
- Error handling
- Logging
- Testing coverage
- CI/CD ready

---

**Status**: Foundation Phase - Building core infrastructure
