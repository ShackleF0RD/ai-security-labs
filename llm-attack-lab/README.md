# Phase 3 – LLM Attack Lab (Semantic Detection, Guardrails, and Monitoring)

## Overview

This project simulates real-world LLM security risks and implements defensive controls in a local environment.

It extends a Retrieval-Augmented Generation (RAG) system by introducing:

- prompt injection attacks
- automated red-team testing
- semantic detection using embeddings
- policy-engine guardrails
- response validation
- logging and monitoring
- attack success rate tracking

All components run locally using Ollama and Chroma to allow safe and controlled experimentation.

---

## Objectives

- Identify and simulate common LLM attack vectors
- Detect attacks using both rule-based and semantic methods
- Prevent malicious input and unsafe output
- Measure attack success rate
- Build a repeatable AI security testing workflow

---

## Architecture Diagram

```mermaid
flowchart LR
    U[User Input] --> GR[Guardrails Engine]

    GR -->|Blocked| B[Reject Request]
    GR -->|Allowed| DET[Hybrid Detector]

    DET -->|Flagged| B
    DET -->|Safe| Q[Query Pipeline]

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

# Phase 4 – LLM Security Lab (Production-Style AI Security Pipeline)

## Overview

This project simulates real-world LLM security risks and implements a **production-style, defense-in-depth architecture**.

It extends a Retrieval-Augmented Generation (RAG) system with:

- prompt injection detection
- semantic input and output filtering
- document trust scoring
- secure retrieval controls
- automated red-team testing
- logging and monitoring
- attack success rate tracking

All components run locally using Ollama and Chroma, allowing safe experimentation with malicious inputs and adversarial scenarios.

---

## Objectives

- Simulate real-world AI attack vectors
- Implement layered security controls across the LLM pipeline
- Detect attacks using both rules and semantic similarity
- Prevent unsafe output and data leakage
- Measure system effectiveness with real metrics
- Build a production-style AI security system

---

## Architecture

```mermaid
flowchart LR
    U[User Input] --> IG[Input Guardrails]
    IG --> DET[Hybrid Detector]

    DET -->|Blocked| RB1[Reject Request]
    DET -->|Allowed| RET[Retriever]

    RET --> TF[Trust Filter + Scoring]
    TF --> PROMPT[Secure Prompt Builder]

    PROMPT --> LLM[Ollama Local Model]

    LLM --> OG[Output Guardrails]
    OG -->|Blocked| RB2[Reject Response]

    OG -->|Allowed| LOG[Logger]
    LOG --> DASH[Dashboard]

    DATA[Documents] --> INGEST[ingest.py]
    INGEST --> RET