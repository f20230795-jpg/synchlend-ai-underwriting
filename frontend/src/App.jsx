import React, { useState } from 'react';
import './App.css'; 

function App() {
  const [formData, setFormData] = useState({
    applicant_name: 'Dhruv Singh',
    email: 'f20230795@pilani.bits-pilani.ac.in',
    monthly_income: '10000',
    credit_score: '400',
    monthly_expenses: '5000',
    requested_loan_amount: '20000',
    employment_notes: 'I work full time with a stable salary.'
  });

  const [decisionData, setDecisionData] = useState({});
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/underwrite', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const data = await response.json();
      setDecisionData(data); 
    } catch (error) {
      console.error("Error connecting to backend:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ backgroundColor: '#f1f5f9', minHeight: '100vh', padding: '3rem 1rem', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      
      <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
        <h1 style={{ color: '#1e3a8a', fontSize: '2.5rem', fontWeight: '800', marginBottom: '0.5rem' }}>
          SynchLend AI Underwriting
        </h1>
        <p style={{ color: '#64748b', fontSize: '1.1rem' }}>
          Multi-Modal contextual credit decisioning for NTC customers.
        </p>
      </div>

      <div style={{ display: 'flex', gap: '2rem', maxWidth: '1000px', margin: '0 auto', flexWrap: 'wrap', justifyContent: 'center' }}>
        
        {/* LEFT COLUMN: Input Form */}
        <div className="dashboard-card" style={{ flex: '1', minWidth: '320px' }}>
          <form onSubmit={handleSubmit}>
            <input type="text" name="applicant_name" value={formData.applicant_name} onChange={handleChange} placeholder="Applicant Name" required />
            <input type="email" name="email" value={formData.email} onChange={handleChange} placeholder="Email" required />
            <input type="number" name="monthly_income" value={formData.monthly_income} onChange={handleChange} placeholder="Monthly Income" required />
            <input type="number" name="credit_score" value={formData.credit_score} onChange={handleChange} placeholder="Credit Score" required />
            <input type="number" name="monthly_expenses" value={formData.monthly_expenses} onChange={handleChange} placeholder="Monthly Expenses" required />
            <input type="number" name="requested_loan_amount" value={formData.requested_loan_amount} onChange={handleChange} placeholder="Requested Amount" required />
            
            {/* NEW: Unstructured Text Area */}
            <textarea 
              name="employment_notes" 
              value={formData.employment_notes} 
              onChange={handleChange} 
              placeholder="Alternative Employment Notes (e.g. Gig worker, Freelance)" 
              required
              style={{ width: '100%', padding: '12px', marginBottom: '1rem', border: '2px solid #94a3b8', borderRadius: '6px', backgroundColor: '#f8fafc', color: '#0f172a', fontSize: '0.95rem', fontWeight: '600', boxSizing: 'border-box', minHeight: '80px', resize: 'vertical' }}
            />
            
            <button type="submit" className="submit-btn" disabled={isLoading}>
              {isLoading ? 'Processing Neural Engine...' : 'Submit Application'}
            </button>
          </form>
        </div>

        {/* RIGHT COLUMN: AI Decision Output */}
        <div className="dashboard-card" style={{ flex: '1', minWidth: '320px', borderTop: '5px solid #10b981' }}>
          
          <div>
            <p className="result-label">Decision:</p>
            <p className="result-value" style={{ color: decisionData.decision === 'APPROVED' ? '#16a34a' : decisionData.decision === 'DECLINED' ? '#dc2626' : '#0f172a' }}>
              {decisionData.decision || "Pending"}
            </p>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <div>
              <p className="result-label">Risk Score:</p>
              <p className="result-value">{decisionData.riskScore || "---"}</p>
            </div>
            {/* NEW: Displaying the AI Extracted Sentiment! */}
            <div>
              <p className="result-label" style={{ color: '#8b5cf6' }}>AI Stability Sentiment:</p>
              <p className="result-value" style={{ color: '#8b5cf6' }}>
                {decisionData.sentimentScore ? `${decisionData.sentimentScore}/10` : "---"}
              </p>
            </div>
          </div>

          <div>
            <p className="result-label">Applicant:</p>
            <p className="result-value" style={{fontSize: '1rem', marginBottom: '1rem'}}>{decisionData.applicant || "---"}</p>
          </div>

          <div>
            <p className="result-label">AI Logic Trace:</p>
            <p className="result-value" style={{ fontWeight: 500, fontSize: "1.05rem", lineHeight: "1.6" }}>
              {decisionData.aiExplanation || "Awaiting multi-modal data ingestion..."}
            </p>
          </div>
          
          <div style={{ marginTop: '2rem', textAlign: 'center', color: '#94a3b8', fontSize: '0.85rem' }}>
            Processed at: {decisionData.timestamp ? new Date(decisionData.timestamp).toLocaleString() : "---"}
          </div>
          
        </div>
      </div>
    </div>
  );
}

export default App;