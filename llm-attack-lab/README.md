# Phase 3 – LLM Attack Lab (Prompt Injection, Guardrails, and Monitoring)

## Overview

This project simulates real-world LLM security risks and implements defensive controls in a local environment.

It extends a Retrieval-Augmented Generation (RAG) system by introducing:

- prompt injection attacks
- automated red-team testing
- policy-engine guardrails
- response validation
- logging and monitoring
- attack success rate tracking

All components run locally using Ollama and Chroma to allow safe and controlled experimentation.

---

## Objectives

- Identify and simulate common LLM attack vectors
- Test how malicious input and documents impact system behavior
- Implement layered defenses (input, retrieval, output)
- Measure attack success rate
- Build a repeatable AI security testing workflow

---

## Architecture Diagram

```mermaid
flowchart LR
    U[User Input] --> GR[Guardrails Engine]

    GR -->|Blocked| B[Reject Request]
    GR -->|Allowed| Q[Query Pipeline]

    Q --> EMB[Embedding Model]
    EMB --> DB[Chroma Vector DB]

    DB --> RET[Retrieved Documents]
    RET --> TF[Trust Filter]

    TF --> PROMPT[Secure Prompt Builder]
    PROMPT --> LLM[Ollama Local LLM]

    LLM --> OUT[Response]
    OUT --> ORG[Output Guardrails]

    ORG -->|Blocked| RB[Reject Response]
    ORG -->|Allowed| LOG[Logger]

    LOG --> DASH[Dashboard]

    DATA[Local Documents] --> INGEST[ingest.py]
    INGEST --> DB