# Phase 3 Notes – LLM Attack Lab

## Overview

This phase builds a secure LLM pipeline that simulates real-world attack scenarios and implements layered defenses.

The system focuses on:
- prompt injection attacks
- jailbreak attempts
- unsafe output handling
- retrieval (RAG) security
- monitoring and metrics

---

## Environment Setup

- Project location:
  - `C:\AI-Security-Labs\projects\llm-attack-lab`
- Python virtual environment:
  - `.venv`

### Key Commands

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
Purpose
isolates dependencies
ensures reproducibility
mirrors real development environments
Core Tools
Python → main language
Ollama → local LLM + embeddings
ChromaDB → vector database for retrieval
Streamlit → dashboard visualization
Guardrails structure → policy-style control layer
Project Structure
llm-attack-lab
│
├── query.py
├── ingest.py
├── auto_attack.py
├── detector.py
├── semantic_examples.py
├── response_filter.py
├── logger.py
│
├── guardrails/
│   ├── __init__.py
│   ├── guardrails_engine.py
│   ├── config.yml
│   ├── rails.co
│   └── actions.py
│
├── dashboard/
│   └── app.py
│
├── logs/
├── chroma_db/
└── screenshots/
Core Components
ingest.py
reads documents from data/
chunks text
creates embeddings
stores in ChromaDB
adds metadata (source, chunk, trust level)

Purpose:

builds the knowledge base
enables RAG
query.py
main application pipeline
processes user input
applies guardrails
retrieves context
builds secure prompt
calls LLM
validates output
logs results

Purpose:

orchestrates the full secure system
detector.py
detects prompt injection attempts
combines:
keyword scoring
semantic similarity (embeddings)

Returns:

suspicious flag
score
risk level
matches
semantic similarity values

Purpose:

identifies malicious intent even when paraphrased
semantic_examples.py
stores:
malicious prompt examples
benign prompt examples

Purpose:

reference set for semantic comparison
response_filter.py
checks model output for unsafe content

Purpose:

blocks sensitive responses after generation
logger.py
writes events to:
logs/events.jsonl

Tracks:

prompt checks
blocked inputs
retrieval sources
outputs
attack test results

Purpose:

audit trail + dashboard data source
auto_attack.py
runs automated attack tests
includes:
malicious prompts
benign prompts
logs results + summary

Purpose:

repeatable red-team testing
measures system effectiveness
dashboard/app.py
reads logs
displays metrics

Shows:

total attacks
blocked attacks
allowed attacks
benign handling
attack success rate

Purpose:

visualize system performance
Guardrails System
guardrails_engine.py
central policy layer
applies:
input guardrails
output guardrails
logs all decisions

Purpose:

clean separation of security logic
guardrails folder
structured like a policy engine

Includes:

config.yml
rails.co
actions.py

Purpose:

prepares system for scalable rule-based controls
Data Flow
Documents added to data/
ingest.py stores embeddings in ChromaDB
User submits question
Input guardrails evaluate prompt
Detector flags or allows
Chroma retrieves relevant chunks
Only trusted documents are used
Secure prompt is built
LLM generates response
Output guardrails validate response
Logger records event
Dashboard visualizes results
Key Commands
Run app
python query.py
Run attacks
python auto_attack.py
Launch dashboard
streamlit run dashboard\app.py
Semantic Detection
Process
convert prompt → embedding
compare to:
malicious examples
benign examples
compute similarity
flag based on threshold
Why it matters
detects paraphrased attacks
improves accuracy over keyword-only detection
Retrieval Security
documents labeled:
trusted
malicious
retrieval returns both
filter removes malicious content

Purpose:

prevents RAG poisoning
Output Validation
checks model response for sensitive content
blocks unsafe outputs

Purpose:

prevents leakage after generation
Metrics
Attack Success Rate
allowed attacks / total attacks
lower = better security
Key Takeaways
LLM systems require layered defenses
prompt injection is a major risk
semantic detection improves resilience
RAG pipelines can be poisoned without filtering
logging enables tuning and visibility
Limitations
semantic threshold requires tuning
detection is heuristic-based
no ML-trained classifier
no external threat feeds
Summary

Phase 3 transforms a basic LLM system into a security-aware architecture by adding:

hybrid detection (keyword + semantic)
guardrails
automated attack testing
logging
monitoring dashboard

This provides a strong foundation for building secure AI systems.


---

# 🚀 Optional next step

Add it to GitHub:

```powershell
git add notes.md
git commit -m "Add Phase 3 notes documentation"
git push