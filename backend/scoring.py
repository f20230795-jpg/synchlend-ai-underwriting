import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
model_is_active = False

if API_KEY and API_KEY != "your_api_key_here":
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        model_is_active = True
    except Exception as e:
        print("AI setup failed:", e)

# Helper function to generate flawless human text if the API fails
def generate_mock_explanation(decision, req, dti, free_cash, monthly_payment, risk_score):
    if decision == "DECLINED":
        if dti > 0.60:
            return f"We are unable to approve your application for ${int(req)}. Adding this loan would push your Debt-to-Income (DTI) ratio to {int(dti*100)}%, exceeding our responsible lending threshold of 60%. Reducing current obligations will help you qualify in the future."
        elif free_cash < monthly_payment:
            return f"We cannot approve your application today. Our analysis shows your estimated free monthly capital (${int(free_cash)}) is insufficient to safely cover the projected loan payments (${int(monthly_payment)}). We invite you to apply again as your financial profile grows."
        else:
            return f"We are unable to approve your loan at this time. Your Alternative Risk Score is {risk_score}. While your profile shows promise, our algorithm requires slightly more consistent alternative data signals before extending credit."
    else:
        return f"Congratulations! Your application for ${int(req)} is approved. Our underwriting algorithm calculated a highly stable DTI ratio of {int(dti*100)}% and successfully processed your unstructured employment profile to generate a strong alternative approval. Welcome to SynchLend."


def calculate_ntc_score(income, expenses, alt_score, requested_amount, employment_notes):
    try:
        inc = float(income)
        exp = float(expenses)
        alt = float(alt_score)
        req = float(requested_amount)
    except ValueError:
        return 0, 0, "DECLINED", "Application Error: Invalid financial numbers provided."

    # 1. Smarter Unstructured Data Extraction
    notes_lower = employment_notes.lower()
    sentiment_score = 7 # Default
    
    # Expanded keyword lists for better dynamic reactions
    high_stability_words = ["salary", "full time", "stable", "permanent", "engineer", "doctor", "corporate"]
    low_stability_words = ["freelance", "crypto", "gig", "part time", "temporary", "unemployed", "uber", "doordash"]

    if any(word in notes_lower for word in high_stability_words):
        sentiment_score = 9
    elif any(word in notes_lower for word in low_stability_words):
        sentiment_score = 4

    # 2. Mathematical Feature Engineering
    free_cash = inc - exp
    monthly_payment = req / 12  
    dti = (exp + monthly_payment) / inc if inc > 0 else 1.0
    dti_health = max(0, 100 - (dti * 100))
    
    risk_score = int((alt * 0.45) + (dti_health * 3.5) + (sentiment_score * 12.5))
    risk_score = min(850, risk_score) 

    # 3. Decision Logic Guardrails
    if dti > 0.60:
        decision = "DECLINED"
        base_reason = f"DTI is {int(dti*100)}%."
    elif free_cash < monthly_payment:
        decision = "DECLINED"
        base_reason = f"Free cash is ${int(free_cash)}."
    elif risk_score < 550:
        decision = "DECLINED"
        base_reason = f"Score is {risk_score}."
    else:
        decision = "APPROVED"
        base_reason = f"Stable financials and sentiment {sentiment_score}/10."

    # 4. Generate Professional Explanation (Zero "System Notes")
    if model_is_active:
        try:
            prompt = f"""
            Act as a professional SynchLend underwriter talking to the applicant.
            Loan: ${int(req)}. DTI: {int(dti*100)}%. Risk Score: {risk_score}.
            Applicant's Notes: "{employment_notes}"
            Decision: {decision}. 
            Write a 2-3 sentence human explanation addressed to them. Do not use asterisks or robotic formatting. 
            Keep it highly professional. Gently reference their employment notes in your reasoning.
            """
            response = model.generate_content(prompt)
            explanation = response.text.strip()
        except Exception:
            # If Google API billing blocks us, we use our flawless mock function
            explanation = generate_mock_explanation(decision, req, dti, free_cash, monthly_payment, risk_score)
    else:
        explanation = generate_mock_explanation(decision, req, dti, free_cash, monthly_payment, risk_score)

    return risk_score, sentiment_score, decision, explanation