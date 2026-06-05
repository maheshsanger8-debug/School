# Backend Configuration

## Environment Variables

```bash
# Application
DEBUG=false
ENVIRONMENT=development
HOST=0.0.0.0
PORT=8000

# OpenRouter LLM
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=mistralai/mistral-7b-instruct

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/agent_db
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10

# Vector Database (Qdrant)
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=optional_api_key
QDRANT_COLLECTION_NAME=agent_memory

# Embeddings
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384

# Agent Configuration
MAX_ITERATIONS=10
TIMEOUT_SECONDS=300
MEMORY_RETENTION_DAYS=30

# Logging
LOG_LEVEL=INFO

# CORS
CORS_ORIGINS=["*"]
CORS_ALLOW_CREDENTIALS=true
CORS_ALLOW_METHODS=["*"]
CORS_ALLOW_HEADERS=["*"]
```

## Setup Instructions

### Local Development

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```bash
cp .env.example .env
# Edit .env with your credentials
```

4. Run development server:
```bash
python -m app.main
```

5. Access API documentation:
```
http://localhost:8000/docs
```

### Docker

```bash
docker build -t agent-backend .
docker run -p 8000:8000 --env-file .env agent-backend
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test
pytest tests/test_agent_runtime.py
```

## API Endpoints

### Health Check
```bash
GET /health
```

### Get Status
```bash
GET /status
```

### List Tools
```bash
GET /tools
```

### Execute Agent
```bash
POST /execute
Content-Type: application/json

{
  "goal": "Calculate 2 + 2",
  "max_iterations": 10,
  "timeout_seconds": 300
}
```
