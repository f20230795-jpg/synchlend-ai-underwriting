import sqlite3

def init_db():
    conn = sqlite3.connect('synchlend.db')
    c = conn.cursor()
    # We added employment_notes and sentiment_score to our memory!
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
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_application(data, decision, risk_score, sentiment_score, timestamp):
    conn = sqlite3.connect('synchlend.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO applications 
        (name, email, income, alt_score, expenses, requested_amount, employment_notes, sentiment_score, final_decision, risk_score, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('name'), 
        data.get('email'), 
        data.get('input1'), 
        data.get('input2'), 
        data.get('input3'), 
        data.get('input4'),
        data.get('employment_notes'),
        sentiment_score,
        decision, 
        risk_score, 
        timestamp
    ))
    conn.commit()
    conn.close()