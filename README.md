# Smart Restaurant Assistant

Multi-Agent RAG System for restaurant chain operations — menu queries, reservations, availability, and specials.

## Architecture

LangGraph orchestrator with 8 nodes: Memory Loader → Planner → Router → RAG/Operations → Merge → Validator → Formatter → Memory Saver.

## Quick Start

```bash
# 1. Start Ollama
ollama pull qwen2.5:3b-instruct-q3_K_S

# 2. Install dependencies
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 3. Index knowledge base
python -c "from ai.rag.indexer import index_documents; index_documents()"

# 4. Start server
python -m uvicorn app.main:app --reload

# 5. Chat (another terminal)
python chat.py
```

## API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/chat` | POST | Send message |
| `/reset` | POST | Clear conversation |

## Tech Stack

Python 3.12, FastAPI, LangGraph, ChromaDB, BAAI/bge-small-en-v1.5, Ollama, SQLite

## Testing

```bash
pytest tests/ -v
```

## Configuration

Copy `.env.example` to `.env` and adjust. See `PROJECT_MAP.md` for full blueprint.
