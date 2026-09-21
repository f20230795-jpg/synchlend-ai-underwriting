# SynchLend AI: Contextual Underwriting Engine

## 🏗️ System Architecture Diagram

             ┌─────────────────────┐
             │   React Frontend    │
             │    Vite Dashboard   │
             └──────────┬──────────┘
                        │ HTTP/JSON
                        ▼
             ┌─────────────────────┐
             │    FastAPI API      │
             │  /api/v1/underwrite │
             └──────────┬──────────┘
                        │ Pydantic Validation
              ┌─────────┴─────────┐
              ▼                   ▼
     ┌─────────────────┐   ┌─────────────────┐
     │ Scoring Engine  │   │ NLP Extraction  │
     │ Math & Logic    │   │ Google Gemini   │
     └────────┬────────┘   └────────┬────────┘
              │                     │
              └──────────┬──────────┘
                         ▼
                ┌─────────────────┐
                │ SQLite Database │
                │ (Audit Logging) │
                └─────────────────┘

## ⚖️ Responsible AI & Governance
- **Human Oversight:** This engine acts as decision support. Automated outputs require appropriate human review for complex edge cases.
- **Fairness & Bias Mitigation:** Risk scoring relies on deterministic financial ratios (DTI, Free Cash). Unstructured text is evaluated strictly for employment stability, avoiding sensitive demographic attributes.
- **Explainability & Transparency:** Every decision generates an auditable, human-readable breakdown explaining the specific financial factors driving the outcome.
- **Data Privacy:** Uses isolated environments and environment variables to secure data.

## 🚀 Setup Instructions
1. **Backend:** 
   * cd backend
   * pip install -r requirements.txt
   * Rename .env.example to .env and add your Gemini API Key
   * uvicorn main:app --reload
2. **Frontend:** 
   * cd frontend
   * npm install
   * npm run dev
3. **Tests:**
   * cd backend
   * python test_scoring.py