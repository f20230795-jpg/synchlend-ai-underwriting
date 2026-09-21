# SynchLend AI: Contextual Underwriting Engine for NTC Borrowers

## Overview
SynchLend AI is an enterprise-grade, multi-modal underwriting microservice designed to evaluate New-to-Credit (NTC) applicants. It bridges the gap between traditional financial risk metrics and alternative data by ingesting unstructured user employment notes, running real-time Natural Language Processing (NLP) sentiment extraction via Google Gemini, and feeding those insights into a deterministic risk scoring model.

## Core Architecture & Tech Stack
- **Frontend:** React.js, Vite, Responsive CSS Dashboard (`App.jsx`).
- **Backend:** FastAPI (Python API service), Pydantic Data Validation, Uvicorn ASGI Server.
- **Database:** SQLite Relational Schema (Designed with foreign keys and structure ready for PostgreSQL/pgvector migration)[cite: 2].
- **AI / LLM Layer:** Google Gemini 1.5 Flash API with prompt templates, guardrails, and dynamic sentiment-scoring fallback mechanisms.
- **Security & Guardrails:** Strict Pydantic input sanitization, environment variable protection (`.env`), CORS middleware, and safe credential management.

## Engineering Highlights
- **Clean & Modular Codebase:** Separated concerns cleanly into `main.py` (API routing), `database.py` (Persistence), and `scoring.py` (Algorithm & NLP logic).
- **Explainable AI (XAI):** Generates transparent audit traces and human-readable explanations for every approval or decline decision instead of opaque black-box scoring.
- **Unit Testing:** Automated unit testing suite built via Python's `unittest` framework to verify deterministic scoring accuracy.

---

## Setup & Run Instructions

### 1. Backend Setup (FastAPI)
Open your terminal, navigate to the backend directory, and install dependencies:
```bash
cd backend
pip install fastapi uvicorn pydantic google-generativeai python-dotenv
# SynchLend AI: Contextual Underwriting Engine for NTC Borrowers

## Overview
SynchLend AI is an enterprise-grade, multi-modal underwriting microservice designed to evaluate New-to-Credit (NTC) and gig-economy applicants. It bridges the gap between traditional financial risk metrics and alternative behavioral data by ingesting unstructured user narratives, running real-time Natural Language Processing (NLP) sentiment extraction, and fusing those insights into a deterministic risk-scoring engine.

---

## 🏗️ Detailed System Architecture Diagram
```text
================================================================================
                         SYNCHLEND AI: SYSTEM ARCHITECTURE
================================================================================

 [ CLIENT / USER LAYER ]
       │
       ▼
 ┌────────────────────────────────────────────────────────────────────────┐
 │ Frontend Presentation Tier (React.js & Vite SPA)                       │
 │ • Responsive Tailwind/CSS UI Dashboard                                 │
 │ • Dynamic Form State Management & Real-time AI Feedback Display        │
 └──────────────────────────────────┬─────────────────────────────────────┘
                                    │ HTTP / REST (JSON Payloads)
                                    ▼
 ┌────────────────────────────────────────────────────────────────────────┐
 │ API Gateway & Security Tier (FastAPI Python Service)                   │
 │ • CORS Middleware & Secure Request Routing                             │
 │ • Pydantic Strict Data Validation & Sanitization Guardrails            │
 │ • Secure Environment Variable (.env) Secret Management                 │
 └──────────────────┬───────────────────┬──────────────────────────────────┘
                    │                                  │
                    ▼                                  ▼
 ┌──────────────────────────────────────┐   ┌─────────────────────────────┐
 │ AI Intelligence Layer                │   │ Persistence & Storage Tier  │
 │ • Google Gemini 1.5 Flash LLM        │   │ • Relational SQLite Schema  │
 │ • Prompt Templates & Guardrails      │   │ • Prepared for PostgreSQL / │
 │ • Automated Keyword Sentiment Fallback│   │   pgvector Migration        │
 └──────────────────┬───────────────────┘   └──────────────┬──────────────┘
                    │                                      │
                    └──────────────────┬───────────────────┘
                                       │
                                       ▼
 ┌────────────────────────────────────────────────────────────────────────┐
 │ Verification & Engineering Quality Tier                                │
 │ • Automated Unit Testing Suite (`test_scoring.py` via Python unittest) │
 │ • Explainable AI (XAI) Transparent Audit Trail & Logging             │
 └────────────────────────────────────────────────────────────────────────┘