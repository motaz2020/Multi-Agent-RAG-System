# 🍽️ Smart Restaurant Assistant
## Multi-Agent RAG System
### Technical Assessment Project Blueprint

Version: 2.0

---

# 1. Executive Summary

## Project Objective

Design and implement a production-inspired Multi-Agent AI system for a restaurant chain capable of combining:

- Retrieval-Augmented Generation (RAG)
- Backend Tool Calling
- Conversation Memory
- Multi-Agent Orchestration
- Response Validation
- Hallucination Prevention

The objective is not to build a chatbot.

The objective is to build an AI workflow where each component owns a single responsibility and collaborates through a centralized orchestration layer.

The implementation prioritizes:

• Maintainability

• Scalability

• Modularity

• Explainability

• Grounded Responses

---

# 2. Assessment Compliance Matrix

Every assessment requirement is mapped directly to a system component.

| Assessment Requirement | Implementation |
|-------------------------|----------------|
| Main Orchestrator | LangGraph Supervisor Graph |
| Intent Classification | Task Planner Node |
| Route Requests | Routing Engine |
| Maintain Memory | LangGraph Checkpointer |
| Merge Responses | Merge Node |
| Validate Responses | Validation Node |
| Handle Ambiguity | Clarification Node |
| Decide Tool Usage | Planner + Operations Agent |
| Prevent Hallucinations | Validation Layer + Grounded Prompt |
| Restaurant Knowledge | RAG Agent |
| Document Ingestion | Ingestion Pipeline |
| Chunking | Recursive Character Splitter |
| Embedding Model | BAAI BGE Small |
| Vector Store | ChromaDB |
| Retrieval Strategy | Top-K Semantic Retrieval |
| Context Filtering | Metadata Filtering |
| Grounded Generation | Context-only Prompt |
| Operations Agent | Tool Executor |
| Tool Calling | LangChain Tool Registry |
| Memory | SQLite Checkpointer |
| GitHub Repository | Production Repository |
| README | Architecture Documentation |

Result

Every mandatory assessment requirement is covered.

---

# 3. Architecture Philosophy

The project follows six engineering principles.

---

## Principle 1

Single Responsibility

Every module performs exactly one responsibility.

Examples

Planner

↓

Planning only

RAG Agent

↓

Knowledge Retrieval only

Operations Agent

↓

Tool Execution only

Validator

↓

Response Validation only

---

## Principle 2

Centralized Orchestration

Only one component controls execution.

The Orchestrator.

Agents never communicate directly.

---

## Principle 3

Knowledge Isolation

Restaurant knowledge exists only inside the RAG system.

No other component owns restaurant facts.

---

## Principle 4

Operational Isolation

Business operations always execute through backend tools.

LLMs never simulate operational data.

---

## Principle 5

Validation Before Response

Every response must pass validation before reaching the user.

---

## Principle 6

State-Driven Workflow

Execution decisions are based on graph state instead of procedural code.

---

# 4. High-Level Architecture

                              User
                                │
                                ▼
                 +-------------------------------+
                 |        Orchestrator           |
                 |-------------------------------|
                 | Planner                       |
                 | Router                        |
                 | Memory                        |
                 | Merge                         |
                 | Validation                    |
                 +-------------------------------+
                     │                   │
          ┌──────────┘                   └──────────┐
          ▼                                         ▼
+--------------------------+          +----------------------------+
| Restaurant Knowledge     |          | Operations Agent           |
| Agent                    |          |                            |
+--------------------------+          +----------------------------+
| Retrieval                |          | Tool Selection             |
| Context Construction     |          | Tool Execution             |
| Grounded Generation      |          | Structured Results         |
+-------------+------------+          +--------------+-------------+
              │                                      │
              ▼                                      ▼
        Chroma Vector DB                     Backend Tool Registry

---

# 5. Why LangGraph?

The assessment evaluates orchestration.

LangGraph naturally supports:

• Stateful execution

• Multi-agent workflows

• Conditional routing

• Parallel execution

• Memory

• Tool calling

• Graph-based execution

It aligns almost perfectly with the required architecture.

---

# 6. Final Technology Stack

| Layer | Technology |
|--------|------------|
| Language | Python 3.12 |
| API | FastAPI |
| AI Framework | LangGraph |
| LLM | Ollama (Configurable, default: qwen2.5:3b) |
| Embeddings | BAAI/bge-small-en-v1.5 |
| Vector Database | ChromaDB |
| Memory | SQLite Checkpointer |
| Tool Layer | LangChain Tools |
| Validation | Custom Validation Node |
| Configuration | Pydantic Settings |

---

# 7. Project Scope

Included

✓ Restaurant Knowledge

✓ Menu Questions

✓ Restaurant Policies

✓ Table Reservation

✓ Availability Checking

✓ Today's Specials

✓ Multi-turn Conversations

✓ Tool Calling

✓ RAG

✓ Memory

✓ Validation

Excluded

✗ Authentication

✗ Payment

✗ Real Database

✗ Deployment

✗ Monitoring

✗ Admin Dashboard

These are intentionally excluded because they are outside the assessment scope.

---

# 8. Folder Structure

restaurant-ai/

│

├── app/
│   ├── api/
│   │   └── routes.py          # FastAPI endpoints (health, chat, reset)
│   ├── dependencies/
│   │   └── __init__.py         # Singleton graph instance
│   └── main.py                 # FastAPI app with CORS, lifespan
│
├── ai/
│   ├── graph/
│   │   ├── builder.py          # StateGraph + MemorySaver compilation
│   │   ├── state.py            # GraphState schema (all node fields)
│   │   ├── router.py           # Route plan → rag/operations, always → merge
│   │   ├── registry.py         # NodeRegistry for tracking nodes
│   │   └── nodes/
│   │       ├── planner.py      # Keyword detection + LLM fallback
│   │       ├── rag.py          # RAG execution via pipeline
│   │       ├── operations.py   # Tool execution (book/check/specials)
│   │       ├── merge.py        # Merge RAG + operation results
│   │       ├── validator.py    # Confidence + content validation
│   │       ├── formatter.py    # LLM formatting with fallback
│   │       └── memory.py       # Memory loader + saver
│   │
│   ├── rag/
│   │   ├── loader.py           # Load .txt files
│   │   ├── chunker.py          # RecursiveCharacterTextSplitter (500/100)
│   │   ├── embeddings.py       # HuggingFace BGE embeddings
│   │   ├── indexer.py          # ChromaDB indexer
│   │   ├── retriever.py        # Top-4 semantic search
│   │   ├── context.py          # Dedup, rank, build context, build RAGResult
│   │   └── pipeline.py         # Orchestrate retrieve → context → LLM → result
│   │
│   ├── tools/
│   │   ├── registry.py         # ToolRegistry class
│   │   └── restaurant_tools.py # check_table_availability, book_table, get_today_special
│   │
│   ├── prompts/
│   │   ├── planner.md          # Plan generation prompt
│   │   ├── rag.md              # Grounded RAG answer prompt
│   │   ├── operations.md       # Tool selection prompt
│   │   ├── validator.md        # Response validation prompt
│   │   └── formatter.md        # Response formatting prompt
│   │
│   ├── models/
│   │   └── schemas.py          # Pydantic models (Task, ExecutionPlan, RAGResult, etc.)
│   │
│   └── config/
│       └── settings.py         # Pydantic Settings (Ollama, Chroma, thresholds)
│
├── data/
│   ├── restaurant_menu.txt     # Appetizers, mains, desserts, beverages
│   ├── restaurant_policies.txt # Hours, reservations, branches, refund, etc.
│   └── chroma/                 # ChromaDB persisted index
│
├── tests/
│   ├── conftest.py             # Pytest fixtures
│   ├── test_planner.py         # 4 planner tests
│   ├── test_router.py          # 6 router tests
│   ├── test_tools.py           # 12 tool tests
│   ├── test_rag.py             # 9 RAG pipeline tests
│   ├── test_models.py          # 9 schema tests
│   ├── test_validator.py       # 5 validation tests
│   └── test_merge.py           # 4 merge tests
│
├── requirements.txt
├── .env
├── .gitignore
├── README.md
└── PROJECT_MAP.md

---

# 9. Core Modules

The system consists of seven core modules.

1.

Graph Engine

Responsible for workflow execution.

---

2.

RAG Engine

Responsible for restaurant knowledge retrieval.

---

3.

Tool Engine

Responsible for backend operations.

---

4.

Memory Engine

Responsible for conversation continuity.

---

5.

Validation Engine

Responsible for response verification.

---

6.

Prompt Registry

Stores all prompt templates.

---

7.

Configuration Layer

Centralizes project configuration.

---

# 10. Design Decisions

Decision 1

Planner instead of Intent Classifier

Reason

A planner generates an execution plan rather than a single label.

This allows future scalability while remaining fully compatible with the assessment.

---

Decision 2

Validation as a Graph Node

Reason

Validation is part of the execution workflow.

Treating it as a node improves traceability and testing.

---

Decision 3

Structured Outputs

Reason

Every node exchanges typed objects instead of raw strings.

Benefits

• Cleaner state

• Easier testing

• Better debugging

• Stronger contracts

---

Decision 4

Tool Registry

Reason

The Operations Agent never hardcodes tool selection.

New tools can be added without modifying the graph.

---

Decision 5

Prompt Registry

Reason

Every node owns its own prompt.

Prompt logic remains isolated from execution logic.

---

# 11. Development Philosophy

This project is intentionally designed as if it were the first version of a production system.

The primary objective is not maximizing features.

The objective is maximizing software quality, architectural clarity, and maintainability while fully satisfying the assessment requirements.

---


# PART 2 — Graph Workflow & Agent Design

---

# 12. Execution Model

The system follows a graph-based execution model.

Instead of executing business logic sequentially,
execution flows through independent graph nodes.

Each node performs one responsibility only.

The workflow is deterministic, testable, and extensible.

---

# 13. Complete Workflow

                                    START
                                       │
                                       ▼
                              Load Conversation
                                    Memory
                                       │
                                       ▼
                               Planner Node
                                       │
                                       ▼
                               Router Node
                     ┌─────────────────┼──────────────────┐
                     │                 │                  │
                     ▼                 ▼                  ▼
               Knowledge         Operation          Mixed Request
                     │                 │                  │
                     ▼                 ▼                  ▼
                RAG Agent      Operations Agent     Parallel Execution
                     │                 │                  │
                     └─────────────────┴──────────────────┘
                                       │
                                       ▼
                                 Merge Node
                                       │
                                       ▼
                               Validation Node
                                       │
                                       ▼
                               Formatter Node
                                       │
                                       ▼
                                Save Memory
                                       │
                                       ▼
                                      END

---

# 14. Graph Nodes

The graph contains eight execution nodes.

Every node owns exactly one responsibility.

No business logic is duplicated.

---

## Node 1

Memory Loader

Purpose

Load previous conversation context.

Input

thread_id

Output

conversation_history

Responsibilities

- Load previous turns
- Restore session context
- Recover reservation information
- Recover previous branch selection

---

## Node 2

Planner

Purpose

Generate an execution plan using keyword detection + LLM fallback.

The planner does NOT execute anything.

Detection Strategy (Two-Layer)

Layer 1 — Keyword Matching (fast path)

Keywords in the query are matched against intent categories:

- "menu", "appetizer", "price", "allergen", "hour", "policy" → Knowledge
- "book", "reserve", "table for" → Reservation
- "available", "free table" → Availability
- "special", "chef special" → Specials

If keywords match, the plan is returned immediately without calling the LLM.

Layer 2 — LLM Fallback

If no keywords match, the planner invokes Ollama with a structured prompt to parse the intent and generate an ExecutionPlan as JSON.

Example

User

Book a table tomorrow at 8 PM.

Planner Output

Execution Plan

Task 1

Reservation

Priority

High

Requires Tool

Yes

---

Mixed Example

User

Do you have grilled chicken?
Book a table tomorrow.

Planner

Task 1

Restaurant Knowledge

Task 2

Reservation

Execution Mode

Parallel

---

Responsibilities

- Understand user objective via keywords

- Detect missing information

- Decide execution strategy

- Build execution plan

---

ExecutionPlan

Fields

- detected_tasks
- execution_mode
- requires_clarification
- confidence

---

## Node 3

Router

Purpose

Transform the execution plan into graph execution.

Responsibilities

- Select execution path (knowledge → RAG, operation → Operations)

- Start parallel execution via Send()

- Route both paths → Merge node

The router never performs business logic.

---

Routing Rules

Knowledge

↓

RAG

↓

Merge

Operation

↓

Operations Agent

↓

Merge

Mixed

↓

Parallel (Send)

↓

Merge

---

## Node 4

Restaurant Knowledge Agent

Purpose

Retrieve restaurant information.

Responsibilities

- Retrieve documents

- Build context

- Generate grounded response

The RAG Agent never executes backend tools.

---

Input

Question

+

Conversation Context

Output

RAGResult

Fields

answer

sources

confidence

retrieved_chunks

---

## Node 5

Operations Agent

Purpose

Execute operational tasks.

Responsibilities

- Select backend tools

- Execute tools

- Return structured outputs

The Operations Agent never retrieves restaurant knowledge.

---

Output

OperationResult

Fields

tool_name

status

payload

execution_time

---

## Node 6

Merge Node

Purpose

Combine outputs from multiple agents.

Responsibilities

- Merge responses

- Preserve execution order

- Preserve factual integrity

The Merge Node never modifies facts.

---

Example

Knowledge

↓

Chicken is grilled.

+

Operations

↓

Table available.

↓

Merged Response

Chicken is grilled.

A table is available tomorrow at 7 PM.

---

## Node 7

Validation Node

Purpose

Validate response quality.

Responsibilities

Grounding Validation

Tool Validation

Confidence Validation

Formatting Validation

Hallucination Prevention

---

Output

ValidationResult

Fields

passed

issues

confidence

validated_response

---

## Node 8

Formatter

Purpose

Produce the final user response.

Responsibilities

- Formatting

- Bullet lists

- Markdown

- Natural language polishing

No factual generation occurs here.

---

# 15. Shared State

Every node receives the same state object.

The state evolves throughout execution.

```python
class GraphState(BaseModel):

    thread_id: str

    user_query: str

    conversation_history: list

    execution_plan: ExecutionPlan | None

    rag_result: RAGResult | None

    operation_result: OperationResult | None

    merged_result: str | None

    validation_result: ValidationResult | None

    final_response: str | None
```

---

# 16. Execution Plan

Instead of a simple intent label,
the Planner generates an execution plan.

Example

```json
{
  "tasks": [
    {
      "type": "knowledge",
      "priority": 1
    },
    {
      "type": "reservation",
      "priority": 2
    }
  ],
  "execution_mode": "parallel",
  "requires_clarification": false
}
```

Advantages

- Easier scaling
- Cleaner routing
- Supports multiple tasks
- Compatible with LangGraph

---

# 17. Graph Execution Flow

Sequential (Single Intent)

Planner

↓

Router

↓

RAG Agent or Operations Agent

↓

Merge

↓

Validation

↓

Formatter

↓

Memory Saver

---

Parallel (Mixed Intent)

Planner

↓

Router (Send)

↙ ↘

RAG Agent Operations Agent

↘ ↙

Merge

↓

Validation

↓

Formatter

↓

Memory Saver

---

# 18. Clarification Strategy

If mandatory information is missing,
execution pauses.

Example

Book a table.

Planner detects

Missing

Branch

Date

Time

The Router invokes the Clarification Node.

Example Response

Which branch, date, and time would you like?

---

# 19. Validation Pipeline

Validation occurs before every response.

Validation Steps

1.

Grounding

↓

Supported by retrieved context?

---

2.

Tool Consistency

↓

Matches tool output?

---

3.

Confidence

↓

Above threshold?

---

4.

Formatting

↓

Readable?

---

5.

Safety

↓

No hallucinations?

---

Only validated responses reach the user.

---

# 20. Agent Contracts

Every agent communicates through structured models.

No agent exchanges raw text.

Planner

↓

ExecutionPlan

RAG

↓

RAGResult

Operations

↓

OperationResult

Validator

↓

ValidationResult

Formatter

↓

FinalResponse

This ensures strong interfaces,
predictable behavior,
and easier testing.

---

# 21. Architectural Constraints

Constraint 1

Only the Orchestrator communicates with the user.

---

Constraint 2

Only the RAG Agent accesses ChromaDB.

---

Constraint 3

Only the Operations Agent executes backend tools.

---

Constraint 4

Only the Validator decides whether a response is acceptable.

---

Constraint 5

The Planner never executes business logic.

---

Constraint 6

The Router never generates responses.

---

Constraint 7

The Formatter never changes facts.

---

# PART 3 — Knowledge Engine, Tool Engine & API Design

---

# 22. Knowledge Engine Overview

The Restaurant Knowledge Agent is responsible for answering
restaurant-related questions using Retrieval-Augmented Generation (RAG).

The agent owns the complete knowledge lifecycle.

Responsibilities

• Document ingestion

• Chunk generation

• Embedding generation

• Vector indexing

• Retrieval

• Context construction

• Grounded answer generation

The Knowledge Agent never executes backend tools.

---

# 23. Supported Knowledge Domains

To keep the assessment focused while demonstrating a complete RAG system,
the knowledge base will contain two domains.

---------------------------------------------------------

Domain 1

Restaurant Menu

Contains

- Categories

- Meals

- Ingredients

- Prices

- Cooking Method

- Dietary Information

- Allergens

---------------------------------------------------------

Domain 2

Restaurant Policies

Contains

- Opening Hours

- Reservations

- Refund Policy

- Birthday Events

- Catering Rules

---------------------------------------------------------

This satisfies the assessment requirement while keeping the project manageable.

---

# 24. Knowledge Pipeline

Restaurant Documents

↓

Loader

↓

Cleaning

↓

Chunking

↓

Embedding

↓

Chroma Indexing

↓

Semantic Retrieval

↓

Context Builder

↓

Grounded Prompt

↓

LLM

↓

Structured RAG Result

---

# 25. Document Loader

Supported formats

✓ PDF

Future Support

DOCX

Markdown

HTML

CSV

Loader Responsibilities

Read files

↓

Extract text

↓

Preserve metadata

↓

Forward to preprocessing

---

# 26. Document Preprocessing

Before indexing,
documents are normalized.

Operations

Remove page numbers

↓

Remove duplicate spaces

↓

Remove repeated headers

↓

Normalize line breaks

↓

Preserve paragraph structure

Goal

Improve retrieval quality.

---

# 27. Chunking Strategy

Technique

RecursiveCharacterTextSplitter

Configuration

Chunk Size

500

Overlap

100

Reasoning

Small chunks improve retrieval precision.

Overlap preserves semantic continuity between chunks.

---

# 28. Metadata Strategy

Each chunk stores metadata.

Example

{
    "document": "menu",

    "section": "Chicken",

    "page": 4,

    "chunk": 21,

    "category": "Main Course"
}

Metadata enables

Filtering

Traceability

Source Attribution

Future Hybrid Search

---

# 29. Embedding Layer

Embedding Model

BAAI/bge-small-en-v1.5

Reasons

High retrieval quality

Fast inference

Low memory usage

Strong open-source benchmark performance

---

# 30. Vector Store

Database

ChromaDB

Collection

restaurant_documents

Persistence

Enabled

Distance Metric

Cosine Similarity

Reasons

Simple deployment

Persistent storage

Metadata support

Excellent LangChain integration

---

# 31. Retrieval Pipeline

User Question

↓

Embedding

↓

Similarity Search

↓

Top K

↓

Metadata Filtering

↓

Context Builder

↓

Prompt

↓

LLM

↓

RAG Result

Retrieval Configuration

Top K

4

Search Type

Semantic Similarity

---

# 32. Context Builder

The Context Builder prepares the final prompt.

Input

Retrieved Chunks

Conversation Context

User Question

Output

Optimized Prompt Context

Responsibilities

Remove duplicates

↓

Rank passages

↓

Build context

↓

Limit token size

---

# 33. Grounded Prompt

The RAG prompt follows strict rules.

Rules

Only answer from retrieved context.

Never invent information.

Never guess missing facts.

If information is unavailable,
state that clearly.

Always cite document source internally.

---

# 34. Knowledge Output

The RAG Agent returns a structured model.

RAGResult

answer

sources

retrieved_chunks

confidence

reasoning_summary

This object becomes part of the Graph State.

---

# 35. Tool Engine

Operational requests never interact with the RAG system.

Instead,
they execute backend tools.

Responsibilities

Tool Selection

↓

Input Validation

↓

Tool Execution

↓

Response Normalization

↓

Structured Result

---

# 36. Tool Registry

Every tool is registered centrally.

Available Tools

check_table_availability

book_table

get_today_special

The Operations Agent never hardcodes tool references.

Benefits

Easy extension

Cleaner architecture

Simpler testing

---

# 37. Tool Specifications

Tool

check_table_availability()

Input

branch

date

time

Output

available

remaining_tables

---------------------------------------------------------

Tool

book_table()

Input

customer_name

branch

date

time

Output

reservation_id

status

---------------------------------------------------------

Tool

get_today_special()

Input

branch

Output

meal

price

description

---

# 38. Operations Result

Every execution returns

OperationResult

tool_name

status

payload

execution_time

errors

---

# 39. Prompt Registry

Every node owns its own prompt.

prompts/

planner.md

rag.md

operations.md

validator.md

formatter.md

Keeping prompts isolated makes prompt iteration easier.

---

# 40. API Layer

The API remains intentionally thin.

Its responsibility is only to expose the graph.

FastAPI

↓

LangGraph

↓

Graph Builder

↓

Response

No AI logic exists inside FastAPI.

---

# 41. REST Endpoints

POST

/chat

Main conversation endpoint.

---------------------------------------------------------

POST

/reset

Clears conversation memory.

---------------------------------------------------------

GET

/health

Health check.

---

# 42. API Schemas

ChatRequest

thread_id

message

---------------------------------------------------------

ChatResponse

response

sources

tool_calls

confidence

execution_time

---

# 43. Configuration Layer

Configuration is centralized.

settings.py

Contains

API Keys (Ollama base URL)

LLM Model (Ollama model name)

Embedding Model (BGE)

Chunk Size (500)

Chunk Overlap (100)

Top K (4)

Confidence Threshold (0.7)

Collection Name

SQLite Path

This avoids hardcoded values.

---

# 44. Design Rules

Rule 1

Knowledge belongs only to the Knowledge Engine.

---------------------------------------------------------

Rule 2

Operations belong only to backend tools.

---------------------------------------------------------

Rule 3

Prompts never contain business logic.

---------------------------------------------------------

Rule 4

Configuration is centralized.

---------------------------------------------------------

Rule 5

Every component communicates using structured models.

---------------------------------------------------------

Rule 6

The API never communicates directly with tools or Chroma.

Everything passes through the Graph.

---

# PART 4 — Testing, Development Roadmap & Definition of Done

---

# 45. Testing Philosophy

Testing is treated as a first-class component of the project.

Every major layer must be independently testable.

The project follows three testing levels:

• Unit Tests

• Integration Tests

• End-to-End Tests

---

# 46. Unit Testing

Each isolated component is tested independently.

Planner

✓ Single task detection

✓ Multi-task detection

✓ Clarification detection

--------------------------------------------------

Router

✓ Knowledge routing

✓ Operations routing

✓ Parallel routing

✓ Clarification routing

--------------------------------------------------

RAG Pipeline

✓ Document loading

✓ Chunk generation

✓ Embedding generation

✓ Retrieval quality

✓ Context construction

--------------------------------------------------

Operations

✓ Tool selection

✓ Tool execution

✓ Invalid input handling

--------------------------------------------------

Validator

✓ Grounding validation

✓ Confidence validation

✓ Tool consistency validation

✓ Formatting validation

--------------------------------------------------

Formatter

✓ Markdown formatting

✓ Source formatting

✓ Response ordering

---

# 47. Integration Testing

Validate interaction between modules.

Scenario 1

Planner

↓

Router

↓

RAG

↓

Validator

↓

Formatter

--------------------------------------------------

Scenario 2

Planner

↓

Router

↓

Operations

↓

Validator

↓

Formatter

--------------------------------------------------

Scenario 3

Planner

↓

Router

↓

Parallel Execution

↓

Merge

↓

Validator

↓

Formatter

---

# 48. End-to-End Testing

Validate complete application flow.

User

↓

FastAPI

↓

Graph

↓

Planner

↓

Router

↓

Agents

↓

Merge

↓

Validator

↓

Formatter

↓

Memory

↓

Response

---

# 49. Functional Test Cases

Knowledge Query

Question

Do you have vegan pasta?

Expected

✓ Routed correctly

✓ Retrieves menu

✓ Uses RAG

✓ Returns sources

✓ Validation passes

--------------------------------------------------

Operational Query

Book a table tomorrow.

Expected

✓ Tool selected

✓ Tool executed

✓ Reservation returned

--------------------------------------------------

Mixed Query

Do you have grilled chicken?
Book a table tomorrow.

Expected

✓ Parallel execution

✓ Merge

✓ Validation

✓ Final response

--------------------------------------------------

Clarification Query

Book a table.

Expected

Clarification request.

--------------------------------------------------

Unknown Knowledge

Do you sell dragon pizza?

Expected

No hallucination.

Graceful response.

---

# 50. Error Handling Matrix

| Situation | Expected Behaviour |
|-----------|--------------------|
| Empty message | Validation error |
| Unknown intent | Ask for clarification (not yet implemented) |
| Missing reservation data | Request missing fields |
| Tool timeout | Retry once |
| Tool failure | Graceful error |
| Empty retrieval | Information not found |
| Low confidence | Clarification |
| Invalid branch | Ask for valid branch |
| Invalid date | Validation error |
| Invalid API payload | HTTP 422 |

---

# 51. Logging Strategy

Every important event should be logged.

Planner

↓

Execution Plan

↓

Router Decision

↓

Retrieved Documents

↓

Selected Tool

↓

Execution Time

↓

Validation Result

↓

Final Response

Logging should support debugging rather than analytics.

---

# 52. Configuration

All configuration values are centralized.

settings.py

Contains

OLLAMA_MODEL_NAME (qwen2.5:3b-instruct-q3_K_S)

OLLAMA_BASE_URL (http://localhost:11434)

EMBEDDING_MODEL (BAAI/bge-small-en-v1.5)

TOP_K (4)

CHUNK_SIZE (500)

CHUNK_OVERLAP (100)

CONFIDENCE_THRESHOLD (0.7)

COLLECTION_NAME (restaurant_documents)

SQLITE_DATABASE (data/checkpointer.db)

DATA_DIRECTORY (data)

LOG_LEVEL (INFO)

---

# 53. Definition of Done

## Graph Module

Done when

✓ Graph executes successfully

✓ Parallel execution works

✓ Routing works

✓ Memory persists

--------------------------------------------------

## Planner

Done when

✓ Generates execution plans via keyword + LLM

✓ Detects mixed requests

✓ Falls back to LLM when no keywords match

--------------------------------------------------

## RAG Module

Done when

✓ Documents indexed

✓ Chroma populated

✓ Retrieval returns relevant chunks

✓ Sources attached

✓ Hallucination tests pass

--------------------------------------------------

## Operations Module

Done when

✓ Tools execute correctly

✓ Structured outputs returned

✓ Invalid inputs handled

--------------------------------------------------

## Validation Module

Done when

✓ Grounding validation passes

✓ Tool consistency verified

✓ Confidence evaluated

✓ Invalid responses rejected

--------------------------------------------------

## Formatter

Done when

✓ Final response readable

✓ Sources displayed

✓ Tool outputs formatted

--------------------------------------------------

## API

Done when

✓ /chat operational

✓ /reset operational

✓ /health operational

--------------------------------------------------

## Repository

Done when

✓ Clean folder structure

✓ README completed

✓ PROJECT_MAP completed

✓ Example conversations included

✓ Tests pass

---

# 54. Development Roadmap

Phase 1

Project Bootstrap

Deliverables

✓ Repository

✓ Virtual environment

✓ Dependencies

✓ FastAPI skeleton

✓ Configuration

--------------------------------------------------

Phase 2

Knowledge Base

Deliverables

✓ Documents

✓ Loader

✓ Chunking

✓ Embeddings

✓ Chroma indexing

--------------------------------------------------

Phase 3

RAG Engine

Deliverables

✓ Retriever

✓ Context Builder

✓ Prompt

✓ Structured RAG output

--------------------------------------------------

Phase 4

Tool Engine

Deliverables

✓ Tool Registry

✓ Tool implementations

✓ Structured outputs

--------------------------------------------------

Phase 5

Graph Engine

Deliverables

✓ GraphState

✓ Nodes

✓ Builder

✓ Router

✓ Conditional edges

--------------------------------------------------

Phase 6

Memory

Deliverables

✓ SQLite Checkpointer

✓ Conversation history

✓ Context restoration

--------------------------------------------------

Phase 7

Validation

Deliverables

✓ Grounding

✓ Confidence

✓ Tool validation

✓ Formatter

--------------------------------------------------

Phase 8

API

Deliverables

✓ REST endpoints

✓ Request schemas

✓ Response schemas

--------------------------------------------------

Phase 9

Testing

Deliverables

✓ Unit tests

✓ Integration tests

✓ End-to-End tests

--------------------------------------------------

Phase 10

Documentation

Deliverables

✓ README

✓ Architecture section

✓ Setup guide

✓ Example requests

✓ Example responses

---

# 55. Example User Flows

Example 1

User

Do you have grilled chicken?

↓

Planner

↓

Router

↓

RAG

↓

Validator

↓

Formatter

↓

Assistant

--------------------------------------------------

Example 2

User

Book a table tomorrow.

↓

Planner

↓

Router

↓

Operations

↓

Validator

↓

Formatter

↓

Assistant

--------------------------------------------------

Example 3

User

Do you have grilled chicken?
Reserve a table tomorrow.

↓

Planner

↓

Router

↓

Parallel Execution

↓

Merge

↓

Validator

↓

Formatter

↓

Assistant

---

# 56. Future Extensions

The architecture allows future expansion without redesign.

Possible additions

Recommendation Agent

Inventory Agent

Delivery Agent

CRM Agent

Analytics Agent

Voice Assistant

WhatsApp Integration

Real MCP Server

These extensions are intentionally excluded from the current assessment implementation.

---

# 57. Final Architecture Summary

The final system consists of:

✓ One Orchestrator

✓ One Knowledge Agent

✓ One Operations Agent

✓ One Shared Graph State

✓ One Validation Layer

✓ One Memory Layer

✓ One Graph Workflow

✓ One API Layer

Each component owns a single responsibility.

All communication flows through the Orchestrator.

Restaurant knowledge is retrieved exclusively through RAG.

Operational actions are executed exclusively through backend tools.

Every response is validated before reaching the user.

This architecture fully satisfies the assessment requirements while remaining modular, maintainable, extensible, and production-oriented.

---

# END OF PROJECT MAP

Smart Restaurant Assistant
Multi-Agent RAG System

Version 1.0
