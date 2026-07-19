import sqlite3

DB_NAME = "ot_emr.db"

# 1. FUNCTION: Add a new patient
def add_patient(first_name, last_name, birth_date):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO patients (first_name, last_name, birth_date)
        VALUES (?, ?, ?)
    """, (first_name, last_name, birth_date))
    conn.commit()
    patient_id = cursor.lastrowid  # Get the generated ID
    conn.close()
    return patient_id

# 2. FUNCTION: Add a goal for a patient
def add_goal(patient_id, description):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO goals (patient_id, description)
        VALUES (?, ?)
    """, (patient_id, description))
    conn.commit()
    conn.close()

# 3. FUNCTION: Fetch all active goals of a patient
def get_active_goals(patient_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, description FROM goals 
        WHERE patient_id = ? AND status = 'Active'
    """, (patient_id,))
    goals = cursor.fetchall()  # Returns a list of goals
    conn.close()
    return goals

# 4. FUNCTION: Save a SOAP Note
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

# 5. NEW FUNCTION: Fetch SOAP note history for a patient (latest first)
def get_soap_history(patient_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Ginagamit ang created_at (o timestamp) para mauna ang pinakabagong session note
    cursor.execute("""
        SELECT id, subjective, objective, assessment, plan, created_at 
        FROM soap_notes 
        WHERE patient_id = ? 
        ORDER BY created_at DESC
    """, (patient_id,))
    history = cursor.fetchall()
    conn.close()
    return history