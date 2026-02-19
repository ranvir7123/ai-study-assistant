AI Study Assistant – Intelligent Tutor Backend

This project implements an intelligent tutoring backend built on a multi-stage RAG architecture. Traditional RAG systems retrieve context and generate answers directly, assuming the user understands all prerequisites. This often leads to over-explanation, shallow learning, or undetected misconceptions.

This system introduces a diagnosis stage before teaching. Instead of answering immediately, it generates diagnostic questions, analyzes user responses, and produces a structured Gap Report that classifies conceptual weaknesses (prerequisite, mechanism, application, misconception).

Teaching is then performed selectively, retrieving and explaining only the missing concepts. Detected misconceptions are persisted and influence future diagnostic behavior, making the system adaptive over time.

1. System Overview

This backend transforms a standard RAG pipeline into a reasoning-driven tutoring system. Rather than answering directly, the system inserts a structured diagnosis stage that evaluates user understanding before generating explanations.

The architecture separates retrieval, diagnosis, analysis, teaching, and memory into distinct services. A structured Gap Report acts as the boundary between reasoning and generation, ensuring modularity, observability, and extensibility.

The result is a system that teaches selectively instead of exhaustively, detects conceptual weaknesses explicitly, and adapts future diagnostics based on persistent misconception patterns.

2. Architecture Flow

The system follows a multi-stage pipeline:

User Topic
    ↓
Canonical Knowledge Retrieval (Embeddings + Similarity)
    ↓
Diagnostic Question Generation
    ↓
User Answers
    ↓
Answer Analysis & Gap Classification
    ↓
Structured Gap Report
    ↓
Targeted Teaching (Precision RAG)
    ↓
Misconception Memory Update

Service Responsibilities

routes/
Handles HTTP requests and response formatting.

retrieval_service.py
Performs embedding-based similarity search over stored knowledge.

embedding_service.py
Converts text into vector embeddings.

diagnose_service.py

Generates diagnostic questions

Evaluates answers

Produces structured Gap Reports

teaching_service.py
Performs selective retrieval and generates focused explanations.

db_service.py
Manages database interactions and misconception aggregation.

db/models.py
Defines persistence models, including MisconceptionRecord.

Each service has a single responsibility and does not directly control other services.

3. Gap Classification Strategy

The system explicitly categorizes conceptual weaknesses into four types:

Prerequisite Gaps
Missing foundational knowledge required to understand the topic.

Mechanism Gaps
Knows definitions but does not understand how the concept works internally.

Application Gaps
Understands theory but cannot apply it to solve problems.

Misconceptions
Holds an incorrect mental model of the concept.

This classification creates a structured intermediate representation (Gap Report), enabling:

Independent testing of diagnosis

Memory persistence

Selective teaching

Future analytics

Without structured classification, the system would collapse into a monolithic answer generator.

4. Multi-Stage RAG Design

This system uses RAG at multiple stages:

Stage 1 — Grounded Diagnosis

Retrieves canonical knowledge before generating diagnostic questions to prevent hallucinated probing.

Stage 2 — Structured Evaluation

Compares user responses against retrieved canonical context.

Stage 3 — Precision Teaching

Retrieves only missing concepts identified in the Gap Report and generates minimal, focused explanations.

This layered RAG approach ensures:

Controlled reasoning

Reduced over-generation

Clear separation between analysis and teaching

5. Misconception Memory Layer

The system persists recurring misconceptions using a MisconceptionRecord model containing:

Topic

Concept

Gap type

Frequency count

Last detected timestamp

When a misconception frequency increases, future diagnostic generation adapts by explicitly probing that weakness.

This enables:

Adaptive tutoring behavior

Pattern aggregation

Long-term system improvement

No embeddings are used for memory storage; structured aggregation is sufficient.

6. Architectural Tradeoffs
Why SQLite?

Fast iteration

Low operational complexity

Suitable for single-instance backend development

Why No LangChain / Agent Frameworks?

Manual orchestration ensures full control over reasoning flow

Avoids abstraction leakage

Improves interview explainability

Why Separate Services?

Enables modular testing

Supports future scalability

Prevents tight coupling between reasoning and generation

The system prioritizes clarity and architectural discipline over rapid feature expansion.

7. Scaling Strategy

To scale this system:

Replace SQLite with PostgreSQL

Introduce a vector database (e.g., pgvector / dedicated vector store)

Add async request handling

Cache frequent retrieval queries

Add user session tracking for personalization

Separate diagnosis and teaching onto different model tiers

The current design supports this transition because orchestration and reasoning layers are modular.

8. Future Extensions (Agentic Direction)

Future iterations may introduce:

Multi-step adaptive tutoring loops

Difficulty adjustment based on performance trends

Automated concept dependency graphs

Agent-based planning for curriculum sequencing

Evaluation pipelines for gap detection accuracy

The existing Gap Report abstraction enables these extensions without architectural overhaul.