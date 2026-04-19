# Phase 3 – LLM Attack Lab (Prompt Injection & RAG Security)

## Overview

This project builds a local LLM attack and defense lab on top of a Retrieval-Augmented Generation (RAG) system. The goal is to simulate real-world LLM vulnerabilities such as prompt injection, malicious context retrieval, and unsafe outputs, and then implement basic detection and mitigation strategies.

All components run locally using Ollama and Chroma to allow safe, controlled experimentation without external APIs.

---

## Objectives

- Simulate prompt injection attacks against an LLM system
- Test how malicious documents influence RAG pipelines
- Implement basic detection and blocking mechanisms
- Log model interactions for analysis
- Establish a foundation for AI red teaming and security engineering

---

## Architecture Diagram

```mermaid
flowchart LR
    U[User Input] --> DET[Prompt Injection Detector]
    DET -->|Clean| APP[Query Handler]
    DET -->|Blocked| BLOCK[Reject Request]

    APP --> EMB[Embedding Model: nomic-embed-text]
    EMB --> DB[Chroma Vector Database]

    DB --> RET[Retrieved Context Chunks]
    RET --> FILTER[Trust Filter]

    FILTER -->|Trusted Only| PROMPT[Prompt Builder]
    FILTER -->|Malicious Removed| PROMPT

    PROMPT --> LLM[Ollama Local LLM: qwen3:4b]
    LLM --> RESP[Response]

    RESP --> LOG[Event Logger]
    LOG --> OUTPUT[User Output]

    DATA[Local Documents] --> INGEST[ingest.py]
    INGEST --> DB