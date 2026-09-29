import os
from dotenv import load_dotenv
import google.generativeai as genai
from vector_store import init_vector_db, query_policies

load_dotenv()
init_vector_db()

API_KEY = os.getenv("GEMINI_API_KEY")
model_is_active = False

if API_KEY and API_KEY != "your_api_key_here":
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        model_is_active = True
    except Exception as e:
        print("AI setup failed:", e)

def generate_mock_explanation(decision, req, dti, free_cash, monthly_payment, risk_score):
    if decision == "DECLINED":
        if dti > 0.60:
            return f"Declined. The calculated DTI of {int(dti*100)}% exceeds our strict 60% policy threshold. Risk profile too high for approval."
        elif free_cash < monthly_payment:
            return f"Declined. Insufficient free monthly cash flow (${int(free_cash)}) to safely cover the loan installment (${int(monthly_payment)})."
        else:
            return f"Declined. Alternative Risk Score ({risk_score}) did not meet the minimum viable threshold."
    else:
        return f"Approved! The requested ${int(req)} fits safely within our max DTI limits ({int(dti*100)}%). The unstructured employment profile demonstrates sufficient cash flow stability."

def calculate_ntc_score(income, expenses, alt_score, requested_amount, employment_notes):
    try:
        inc = float(income)
        exp = float(expenses)
        alt = float(alt_score)
        req = float(requested_amount)
    except ValueError:
        return 0, 0, "DECLINED", "Application Error: Invalid financial numbers provided.", ""

    # 1. Unstructured Data Extraction & Vector Policy Query
    notes_lower = employment_notes.lower()
    policy_context = query_policies(employment_notes)
    
    sentiment_score = 7 
    high_stability_words = ["salary", "full time", "stable", "permanent", "engineer", "doctor", "corporate"]
    low_stability_words = ["freelance", "crypto", "gig", "part time", "temporary", "unemployed", "uber", "doordash"]

    if any(word in notes_lower for word in high_stability_words):
        sentiment_score = 9
    elif any(word in notes_lower for word in low_stability_words):
        sentiment_score = 4

    # 2. Mathematical Underwriting
    free_cash = inc - exp
    monthly_payment = req / 12  
    dti = (exp + monthly_payment) / inc if inc > 0 else 1.0
    dti_health = max(0, 100 - (dti * 100))
    
    risk_score = int((alt * 0.45) + (dti_health * 3.5) + (sentiment_score * 12.5))
    risk_score = min(850, risk_score) 

    # 3. Policy Threshold Guardrails
    if dti > 0.60:
        decision = "DECLINED"
    elif free_cash < monthly_payment:
        decision = "DECLINED"
    elif risk_score < 550:
        decision = "DECLINED"
    else:
        decision = "APPROVED"

    # 4. LLM Decision Rationale Generation (NO PARROTING)
    if model_is_active:
        try:
            prompt = f"""
            Act as a SynchLend Senior Underwriter. 
            Loan: ${int(req)}. DTI: {int(dti*100)}%. Risk Score: {risk_score}/850.
            Decision: {decision}. 
            Policy Matched: "{policy_context}"
            Write a 2-sentence explanation to the applicant. 
            CRITICAL RULE: Synthesize the reasoning. DO NOT copy or repeat the policy text word-for-word. Explain WHY they were approved/declined based on their numbers. No markdown.
            """
            response = model.generate_content(prompt)
            explanation = response.text.strip()
        except Exception:
            explanation = generate_mock_explanation(decision, req, dti, free_cash, monthly_payment, risk_score)
    else:
        explanation = generate_mock_explanation(decision, req, dti, free_cash, monthly_payment, risk_score)

    return risk_score, sentiment_score, decision, explanation, policy_context