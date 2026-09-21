from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
import datetime

from database import init_db, save_application
from scoring import calculate_ntc_score

app = FastAPI(title="SynchLend Enterprise API")
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ApplicationRequest(BaseModel):
    applicant_name: str = Field(..., min_length=2)
    email: EmailStr = Field(...)
    monthly_income: float = Field(..., gt=0)
    credit_score: float = Field(..., ge=300, le=850)
    monthly_expenses: float = Field(..., ge=0)
    requested_loan_amount: float = Field(..., gt=0)
    employment_notes: str = Field(..., min_length=5)

@app.post("/api/v1/underwrite")
async def submit_application(data: ApplicationRequest):
    risk_score, sentiment_score, decision, explanation = calculate_ntc_score(
        income=data.monthly_income,
        expenses=data.monthly_expenses,
        alt_score=data.credit_score,
        requested_amount=data.requested_loan_amount,
        employment_notes=data.employment_notes
    )
    
    timestamp = datetime.datetime.now().isoformat()
    
    # Save to database
    safe_data_dict = data.model_dump()
    save_application(safe_data_dict, decision, risk_score, sentiment_score, timestamp)
    
    return {
        "decision": decision,
        "applicant": data.applicant_name,
        "riskScore": risk_score,
        "sentimentScore": sentiment_score,
        "aiExplanation": explanation,
        "timestamp": timestamp
    }