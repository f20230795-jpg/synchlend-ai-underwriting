import React, { useState } from 'react';
import './App.css'; 

function App() {
  const [formData, setFormData] = useState({
    applicant_name: 'Dhruv Singh',
    email: 'f20230795@pilani.bits-pilani.ac.in',
    monthly_income: '10000',
    credit_score: '680',
    monthly_expenses: '3000',
    requested_loan_amount: '12000',
    employment_notes: 'I work full time as a lead software engineer at a corporate firm.'
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

  const getBadgeClass = (status) => {
    if (status === 'APPROVED') return 'status-badge badge-approved';
    if (status === 'DECLINED') return 'status-badge badge-declined';
    return 'status-badge badge-pending';
  };

  return (
    <div style={{ padding: '3rem 1rem' }}>
      
      {/* 🚀 FIXED HEADER (No Overlap) */}
      <div style={{ textAlign: 'center', marginBottom: '3rem', padding: '0 1rem' }}>
        <h1 style={{ 
          fontSize: '2.6rem', 
          lineHeight: '1.2', 
          margin: '0 auto 0.8rem auto', 
          maxWidth: '800px',
          color: '#1e3a8a',
          fontWeight: '800',
          letterSpacing: '-1px'
        }}>
          SynchLend Enterprise Underwriting Engine
        </h1>
        <p className="subtitle" style={{ 
          margin: '0 auto', 
          lineHeight: '1.5',
          maxWidth: '600px'
        }}>
          RAG Vector-Enhanced Credit Decisioning for NTC Borrowers
        </p>
      </div>

      <div style={{ display: 'flex', gap: '2rem', maxWidth: '1200px', margin: '0 auto', flexWrap: 'wrap', justifyContent: 'center' }}>
        
        {/* LEFT PANEL: Data Ingestion */}
        <div className="dashboard-card" style={{ flex: '1', minWidth: '350px' }}>
          <h2 style={{ fontSize: '1.2rem', color: '#0f172a', marginBottom: '1.5rem', borderBottom: '2px solid #e2e8f0', paddingBottom: '0.5rem' }}>📄 Applicant Telemetry</h2>
          <form onSubmit={handleSubmit}>
            <div className="input-group">
              <label>Applicant Name</label>
              <input type="text" name="applicant_name" value={formData.applicant_name} onChange={handleChange} required />
            </div>
            <div className="input-group">
              <label>Email Address</label>
              <input type="email" name="email" value={formData.email} onChange={handleChange} required />
            </div>
            
            <div style={{ display: 'flex', gap: '1rem' }}>
              <div className="input-group" style={{ flex: 1 }}>
                <label>Monthly Income ($)</label>
                <input type="number" name="monthly_income" value={formData.monthly_income} onChange={handleChange} required />
              </div>
              <div className="input-group" style={{ flex: 1 }}>
                <label>Monthly Expenses ($)</label>
                <input type="number" name="monthly_expenses" value={formData.monthly_expenses} onChange={handleChange} required />
              </div>
            </div>

            <div style={{ display: 'flex', gap: '1rem' }}>
              <div className="input-group" style={{ flex: 1 }}>
                <label>Requested Loan ($)</label>
                <input type="number" name="requested_loan_amount" value={formData.requested_loan_amount} onChange={handleChange} required />
              </div>
              <div className="input-group" style={{ flex: 1 }}>
                <label>Alt Credit Score</label>
                <input type="number" name="credit_score" value={formData.credit_score} onChange={handleChange} required />
              </div>
            </div>
            
            <div className="input-group">
              <label>Alternative Data / Cash Flow Notes</label>
              <textarea name="employment_notes" value={formData.employment_notes} onChange={handleChange} required style={{ minHeight: '80px', resize: 'vertical' }} />
            </div>
            
            <button type="submit" className="submit-btn" disabled={isLoading}>
              {isLoading ? 'Processing Neural Engine...' : 'Run Diagnostics & Underwrite'}
            </button>
          </form>
        </div>

        {/* RIGHT PANEL: AI Decision Output */}
        <div className="dashboard-card" style={{ flex: '1', minWidth: '350px' }}>
          <h2 style={{ fontSize: '1.2rem', color: '#0f172a', marginBottom: '1.5rem', borderBottom: '2px solid #e2e8f0', paddingBottom: '0.5rem' }}>🧠 Neural Decision Matrix</h2>
          
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <div>
              <p style={{ fontSize: '0.85rem', fontWeight: 700, color: '#64748b', margin: '0 0 5px 0' }}>FINAL VERDICT</p>
              <div className={getBadgeClass(decisionData.decision)}>
                {decisionData.decision || "AWAITING DATA"}
              </div>
            </div>
            <div style={{ textAlign: 'right' }}>
              <p style={{ fontSize: '0.85rem', fontWeight: 700, color: '#64748b', margin: '0 0 5px 0' }}>RISK SCORE</p>
              <p style={{ fontSize: '1.8rem', fontWeight: 800, color: '#0f172a', margin: 0 }}>
                {decisionData.riskScore ? `${decisionData.riskScore}` : "---"}<span style={{fontSize: '1rem', color: '#94a3b8'}}>/850</span>
              </p>
            </div>
          </div>

          {/* Hacker-Style Terminal Box for Vector RAG */}
          <div className="rag-box">
            <div className="rag-label">⚡ ChromaDB Vector Search Match</div>
            <p className="rag-text">
              {decisionData.policyContext ? `> ${decisionData.policyContext}` : "> Waiting for embedding query..."}
            </p>
          </div>

          {/* Clean Insight Box for AI Explanation */}
          <div className="ai-box">
            <div className="ai-label">✨ Generative AI Rationale</div>
            <p className="ai-text">
              {decisionData.aiExplanation || "Submit an application to view the LLM's dynamic reasoning trace."}
            </p>
          </div>
          
          <div style={{ marginTop: '2rem', textAlign: 'center', color: '#94a3b8', fontSize: '0.85rem', fontWeight: 600 }}>
            Session ID: {decisionData.timestamp ? new Date(decisionData.timestamp).getTime() : "---"} | Secure
          </div>
          
        </div>
      </div>
    </div>
  );
}

export default App;