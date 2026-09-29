import sqlite3

def init_db():
    conn = sqlite3.connect('synchlend.db')
    c = conn.cursor()
    
    # 🔥 THIS LINE NUKES THE OLD TABLE SO WE CAN REBUILD IT
    c.execute('DROP TABLE IF EXISTS applications')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            income REAL,
            alt_score REAL,
            expenses REAL,
            requested_amount REAL,
            employment_notes TEXT,
            sentiment_score INTEGER,
            final_decision TEXT,
            risk_score INTEGER,
            policy_context TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_application(data, decision, risk_score, sentiment_score, policy_context, timestamp):
    conn = sqlite3.connect('synchlend.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO applications 
        (name, email, income, alt_score, expenses, requested_amount, employment_notes, sentiment_score, final_decision, risk_score, policy_context, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('applicant_name'), 
        data.get('email'), 
        data.get('monthly_income'), 
        data.get('credit_score'), 
        data.get('monthly_expenses'), 
        data.get('requested_loan_amount'),
        data.get('employment_notes'),
        sentiment_score,
        decision, 
        risk_score,
        policy_context,
        timestamp
    ))
    conn.commit()
    conn.close()