# Phase 2 - Secure RAG Assistant

## Overview
This project builds a local retrieval-augmented generation (RAG) assistant using Ollama and Chroma. The goal is to retrieve relevant document chunks from a local vector database and use them as grounded context for local LLM responses.

## Features
- Local document ingestion
- Text chunking
- Local embeddings with Ollama
- Vector storage with Chroma
- Retrieval of relevant chunks
- Grounded answering from approved context only

## Files
- `ingest.py` - ingests text files into Chroma
- `query.py` - retrieves relevant chunks and answers questions
- `app.py` - simple interactive interface
- `data/` - source documents
- `chroma_db/` - persistent vector database

## Setup
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
ollama pull qwen3:4b
ollama pull nomic-embed-text
python ingest.py
python app.py