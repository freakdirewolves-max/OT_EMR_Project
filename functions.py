import sqlite3

DB_NAME = "ot_emr.db"

def add_goal(patient_id, description):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO goals (patient_id, description, status)
        VALUES (?, ?, 'active')
    """, (int(patient_id), str(description)))
    conn.commit()
    conn.close()

def get_active_goals(patient_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, description 
        FROM goals 
        WHERE patient_id = ?
    """, (int(patient_id),))
    goals = cursor.fetchall()
    conn.close()
    return goals

def save_soap_note(patient_id, subjective, objective, assessment, plan):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO soap_notes (patient_id, subjective, objective, assessment, plan)
        VALUES (?, ?, ?, ?, ?)
    """, (int(patient_id), subjective, objective, assessment, plan))
    conn.commit()
    conn.close()

def get_soap_history(patient_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, subjective, objective, assessment, plan, created_at 
        FROM soap_notes 
        WHERE patient_id = ? 
        ORDER BY created_at DESC
    """, (int(patient_id),))
    history = cursor.fetchall()
    conn.close()
    return history

def delete_goal(goal_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM goals WHERE id = ?", (int(goal_id),))
    conn.commit()
    conn.close()
def delete_soap_note(note_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM soap_notes WHERE id = ?", (int(note_id),))
    conn.commit()
    conn.close()

def update_soap_note(note_id, s, o, a, p):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE soap_notes 
        SET subjective = ?, objective = ?, assessment = ?, plan = ?
        WHERE id = ?
    """, (s, o, a, p, int(note_id)))
    conn.commit()
    conn.close()