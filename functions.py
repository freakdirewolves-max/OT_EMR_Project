import sqlite3

DB_NAME = "ot_emr.db"

# 1. UTUSAN: Mag-add ng bagong pasyente
def add_patient(first_name, last_name, birth_date):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO patients (first_name, last_name, birth_date)
        VALUES (?, ?, ?)
    """, (first_name, last_name, birth_date))
    conn.commit()
    patient_id = cursor.lastrowid  # Kunin ang ID na binigay ng database
    conn.close()
    return patient_id

# 2. UTUSAN: Mag-add ng goal para sa pasyente
def add_goal(patient_id, description):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO goals (patient_id, description)
        VALUES (?, ?)
    """, (patient_id, description))
    conn.commit()
    conn.close()

# 3. UTUSAN: Kuhanin lahat ng Active Goals ng isang pasyente
def get_active_goals(patient_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, description FROM goals 
        WHERE patient_id = ? AND status = 'Active'
    """, (patient_id,))
    goals = cursor.fetchall()  # Ibabalik nito ang listahan ng goals
    conn.close()
    return goals

# 4. UTUSAN: Mag-save ng SOAP Note
def save_soap_note(patient_id, subjective, objective, assessment, plan):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO soap_notes (patient_id, subjective, objective, assessment, plan)
        VALUES (?, ?, ?, ?, ?)
    """, (patient_id, subjective, objective, assessment, plan))
    conn.commit()
    conn.close()
    print("SOAP Note successfully saved!")