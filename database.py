import sqlite3

def init_db():
    # Gagawa ito ng file na 'ot_emr.db' sa mismong folder mo kung wala pa ito.
    # Kung meron na, ikokonekta lang niya ang Python doon.
    conn = sqlite3.connect("ot_emr.db")
    cursor = conn.cursor()

    # 1. Gagawa ng Table para sa PATIENTS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        birth_date TEXT
    )
    """)

    # 2. Gagawa ng Table para sa GOALS ng bawat pasyente
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        description TEXT NOT NULL,
        status TEXT DEFAULT 'Active',
        FOREIGN KEY (patient_id) REFERENCES patients (id)
    )
    """)

    # 3. Gagawa ng Table para sa SOAP NOTES ng bawat session
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS soap_notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        session_date TEXT DEFAULT CURRENT_DATE,
        subjective TEXT,
        objective TEXT,
        assessment TEXT,
        plan TEXT,
        FOREIGN KEY (patient_id) REFERENCES patients (id)
    )
    """)

    # I-save ang mga pagbabago at isara ang koneksyon
    conn.commit()
    conn.close()
    print("Awesome! Ang SQLite Database at Tables ay matagumpay na nagawa!")

# Patakbuhin ang function para magawa na ang database
if __name__ == "__main__":
    init_db()