-- Enable pgvector extension for semantic search over unstructured document embeddings
CREATE EXTENSION IF NOT EXISTS vector;

-- Table 1: Applicants (Stores demographic & income profiles)
CREATE TABLE IF NOT EXISTS applicants (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    monthly_income NUMERIC(12, 2) NOT NULL,
    employment_status VARCHAR(50) NOT NULL,
    is_ntc BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table 2: Document Embeddings (Stores parsed text and vector embeddings)
CREATE TABLE IF NOT EXISTS document_embeddings (
    id SERIAL PRIMARY KEY,
    applicant_id INT REFERENCES applicants(id) ON DELETE CASCADE,
    document_type VARCHAR(50) NOT NULL,
    extracted_text TEXT NOT NULL,
    embedding vector(1536),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table 3: Credit Assessments (Stores dynamic underwriting decisions and SHAP attributions)
CREATE TABLE IF NOT EXISTS credit_assessments (
    id SERIAL PRIMARY KEY,
    applicant_id INT REFERENCES applicants(id) ON DELETE CASCADE,
    calculated_score INT NOT NULL,
    approved_limit NUMERIC(12, 2) NOT NULL,
    risk_category VARCHAR(20) NOT NULL,
    feature_attributions JSONB NOT NULL,
    status VARCHAR(20) DEFAULT 'APPROVED',
    assessed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);