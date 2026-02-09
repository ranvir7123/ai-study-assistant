# AI Study Helper – RAG-Enabled Backend API (V2)

## Overview

This project is a backend AI study assistant that uses Retrieval-Augmented Generation (RAG). The system can generate explanations for new topics, store them as persistent knowledge, and later retrieve and reuse this stored information to produce grounded, context-aware answers. Over time, the assistant improves by learning new topics and leveraging existing knowledge instead of generating responses from scratch for every request.

---

## What Problem Does This Project Solve?

Large Language Models (LLMs) are stateless, meaning they do not remember past interactions or previously generated knowledge. As a result, they often produce generic answers, repeat information, or hallucinate facts. This project solves that problem by introducing persistent memory using a database and a retrieval pipeline. By retrieving relevant stored knowledge and injecting it into the prompt, the system produces more reliable, grounded, and consistent responses.

---

## High-Level Architecture

The system follows a clear separation between learning (write path) and remembering (read path).

Request flow:

Client  
→ `/generate` API endpoint  
→ Retrieval (similarity search over stored knowledge)  
→ Decision gate (similarity threshold)  
→ RAG-based generation **or** fresh generation + storage  
→ Response

### Core Components

- **Route Layer**
  - Accepts user input
  - Decides whether to use RAG or generate new knowledge

- **Retrieval Service**
  - Embeds the user query
  - Computes similarity against stored embeddings
  - Ranks relevant records

- **RAG Service**
  - Builds context from retrieved records
  - Injects context into the LLM prompt
  - Produces grounded responses

- **LLM Service**
  - Handles interaction with the local LLM (Ollama)
  - Contains separate functions for write-path and read-path generation

- **Database**
  - Stores explanations and their embeddings
  - Acts as persistent memory for the system

---

## Retrieval-Augmented Generation (RAG)

RAG allows the system to ground LLM responses in previously stored knowledge. Before generating an answer, the system retrieves the most relevant explanations from the database and injects them into the prompt as context. This ensures that responses are based on known information rather than relying solely on the LLM’s internal training data.

A similarity threshold is used to determine whether retrieved knowledge is relevant enough. If it is, the system uses RAG. Otherwise, it generates a new explanation and stores it for future use.

---

## Learning vs Remembering

The system distinguishes between two modes of operation:

### Learning (Write Path)
- Triggered when no relevant knowledge exists
- Generates a new explanation using the LLM
- Embeds and stores the explanation in the database

### Remembering (Read Path)
- Triggered when relevant knowledge is found
- Retrieves stored explanations
- Uses RAG to generate a grounded response
- Does not store or embed the output

This design prevents memory pollution and ensures that only canonical knowledge is stored.

---

## API Endpoint

### `POST /generate`

**Request Body**
```json
{
  "topic": "arrays in C",
  "level": "beginner"
}
