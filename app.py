import streamlit as st
import database
import functions

# App page configuration
st.set_page_config(layout="wide") # Wide screen layout for split-screen view

st.title("🩺 Occupational Therapy - EMR System")
st.write("---")

# 1. SIDEBAR: Patient Selection
st.sidebar.header("👤 Patient Selection")

# Temporary default Patient ID for demo purposes
patient_id = 1 
st.sidebar.write(f"**Current Patient ID:** {patient_id}")
st.sidebar.info("Tip: You will be able to select the patient name from a drop-down in the next update!")

# 2. SPLIT-SCREEN LAYOUT (2 Columns: Left and Right)
col_soap, col_goals = st.columns([3, 2]) # 3:2 ratio allocates more space for SOAP notes

# --- LEFT COLUMN: SOAP NOTES ---
with col_soap:
    st.header("📝 Daily Session Note (SOAP)")
    
    # Input fields for SOAP documentation
    s_input = st.text_area("Subjective (S)", placeholder="Patient's/Parent's direct quotes or complaints (e.g., 'Masakit po kamay ko' or 'Hindi nakatulog kagabi')", height=80)
    o_input = st.text_area("Objective (O)", placeholder="Measurable performance in activities, buttoning, fine motor tasks, behavior...", height=120)
    a_input = st.text_area("Assessment (A)", placeholder="Clinical reasoning and analysis. Why was the performance such?", height=100)
    p_input = st.text_area("Plan (P)", placeholder="Interventions and focus for the next session...", height=80)
    
    # Save button
    if st.button("💾 Save SOAP Note", type="primary"):
        functions.save_soap_note(patient_id, s_input, o_input, a_input, p_input)
        st.success("Success! The SOAP Note has been saved to the database.")

# --- RIGHT COLUMN: GOALS AND TARGETS ---
with col_goals:
    st.header("🎯 Target Goals")
    st.write("Goal monitoring for today's session:")
    
    # Expandable form to add new goals
    with st.expander("➕ Add New Goal"):
        new_goal_desc = st.text_input("Goal Description", placeholder="e.g., Button 3 large buttons independently")
        if st.button("Add Goal"):
            if new_goal_desc:
                functions.add_goal(patient_id, new_goal_desc)
                st.success("New goal successfully added!")
                st.rerun() # Refresh screen to update the goal list immediately
    
    # Fetch and display active goals from the database
    active_goals = functions.get_active_goals(patient_id)
    
    if not active_goals:
        st.warning("No active goals found for this patient. Add a new goal above!")
    else:
        for goal_id, description in active_goals:
            # Checkbox interactive checklist for tracking
            st.checkbox(f"**Goal #{goal_id}:** {description}", key=f"goal_{goal_id}")