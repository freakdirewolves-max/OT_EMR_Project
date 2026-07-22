import streamlit as st
import functions

st.set_page_config(page_title="OT EMR System", layout="wide")

st.title("Occupational Therapy EMR System")

# --- PATIENT SELECTION / INPUT ---
st.sidebar.header("Patient Selection")
patient_id = st.sidebar.number_input("Enter Patient ID:", min_value=1, value=1, step=1)

st.header(f"Patient Record - ID #{patient_id}")

# Layout: 2 Columns (Left: SOAP Notes & History, Right: Goals)
col1, col2 = st.columns([0.6, 0.4])

# --- LEFT COLUMN: SOAP NOTES ---
with col1:
    st.subheader("📝 New Session SOAP Note")
    
    with st.form(key="soap_form", clear_on_submit=True):
        subjective = st.text_area("Subjective (S)", placeholder="Patient's complaints, statements...")
        objective = st.text_area("Objective (O)", placeholder="Clinical observations, measurements...")
        assessment = st.text_area("Assessment (A)", placeholder="Progress analysis, clinical opinion...")
        plan = st.text_area("Plan (P)", placeholder="Future treatment plan, next session goals...")
        
        submit_soap = st.form_submit_button("💾 Save SOAP Note", type="primary")
        
        if submit_soap:
            if subjective or objective or assessment or plan:
                functions.add_soap_note(patient_id, subjective, objective, assessment, plan)
                st.success("SOAP Note saved successfully!")
                st.rerun()
            else:
                st.warning("Please fill in at least one field before saving.")

    st.write("---")
    st.subheader("📅 Past Session Notes History")
    
    # Fetch previous notes
    soap_history = functions.get_soap_history(patient_id)
    
    if not soap_history:
        st.info("No previous records found for this patient. Start by adding a note above!")
    else:
        for note_id, s, o, a, p, created_at in soap_history:
            with st.expander(f"Session Note #{note_id} - {created_at}"):
                # 1. View Mode
                st.markdown(f"**🗣️ Subjective (S):**\n{s if s else '*No entry*'}")
                st.markdown(f"**🎯 Objective (O):**\n{o if o else '*No entry*'}")
                st.markdown(f"**🧠 Assessment (A):**\n{a if a else '*No entry*'}")
                st.markdown(f"**📋 Plan (P):**\n{p if p else '*No entry*'}")
                
                st.write("---")
                
                # 2. Edit Section
                with st.expander("✏️ Edit this Note"):
                    with st.form(key=f"edit_form_{note_id}"):
                        edit_s = st.text_area("Subjective (S)", value=s if s else "", key=f"es_{note_id}")
                        edit_o = st.text_area("Objective (O)", value=o if o else "", key=f"eo_{note_id}")
                        edit_a = st.text_area("Assessment (A)", value=a if a else "", key=f"ea_{note_id}")
                        edit_p = st.text_area("Plan (P)", value=p if p else "", key=f"ep_{note_id}")
                        
                        save_edit = st.form_submit_button("💾 Save Changes", type="primary")
                        if save_edit:
                            functions.update_soap_note(note_id, edit_s, edit_o, edit_a, edit_p)
                            st.success("Note updated successfully!")
                            st.rerun()
                
                # 3. Delete Button
                if st.button("🗑️ Delete Note", key=f"del_note_{note_id}"):
                    functions.delete_soap_note(note_id)
                    st.success("Note deleted!")
                    st.rerun()

# --- RIGHT COLUMN: GOALS AND TARGETS ---
with col2:
    st.subheader("🎯 Active Target Goals")
    
    # Add new goal form
    with st.form(key="add_goal_form", clear_on_submit=True):
        new_goal = st.text_input("Add New Goal:", placeholder="e.g., Improve fine motor coordination")
        submit_goal = st.form_submit_button("➕ Add Goal")
        
        if submit_goal:
            if new_goal.strip():
                functions.add_goal(patient_id, new_goal)
                st.success("Goal added!")
                st.rerun()
            else:
                st.warning("Please type a goal description.")
                
    st.write("---")
    
    # Fetch active goals
    active_goals = functions.get_active_goals(patient_id)
    
    if not active_goals:
        st.info("No active goals yet. Add one above!")
    else:
        for goal_id, description in active_goals:
            col_text, col_del = st.columns([0.85, 0.15])
            
            with col_text:
                st.checkbox(f"**Goal #{goal_id}:** {description}", key=f"goal_{goal_id}")
                
            with col_del:
                if st.button("🗑️", key=f"del_{goal_id}"):
                    functions.delete_goal(goal_id)
                    st.rerun()