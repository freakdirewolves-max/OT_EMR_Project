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
        st.rerun() # I-refresh para lumitaw agad ang bagong save sa history sa ibaba!

    st.write("---")
    st.subheader("📜 Past Session Notes History")
    
    # Kuhanin ang mga lumang notes ng bata
    soap_history = functions.get_soap_history(patient_id)
    
    if not soap_history:
        st.info("No previous records found for this patient. Start by adding a note above!")
    else:
        for note_id, s, o, a, p, date_created in soap_history:
            # Ipakita ang bawat session gamit ang dropdown boxes para malinis tingnan
            with st.expander(f"📅 Session Note #{note_id} - {date_created}"):
                st.markdown(f"**🗣️ Subjective (S):**\n{s if s else '*No entry*'}")
                st.markdown(f"**🎯 Objective (O):**\n{o if o else '*No entry*'}")
                st.markdown(f"**🧠 Assessment (A):**\n{a if a else '*No entry*'}")
                st.markdown(f"**📋 Plan (P):**\n{p if p else '*No entry*'}")