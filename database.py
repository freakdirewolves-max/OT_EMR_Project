import sqlite3

# Ito ang gagawa ng koneksyon sa database file mo
conn = sqlite3.connect("ot_emr.db")
cursor = conn.cursor()

# 1. Gawa ng table para sa SOAP Notes (May kasama nang created_at timestamp!)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS soap_notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        subjective TEXT,
        objective TEXT,
        assessment TEXT,
        plan TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# 2. Gawa ng table para sa Target Goals (Para sa checklist sa kanan)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        description TEXT,
        status TEXT DEFAULT 'active'
    )
""")

# I-save ang mga pagbabago at isara ang koneksyon
conn.commit()
conn.close()

print("Database initialized successfully with 'created_at' column! 🎉")