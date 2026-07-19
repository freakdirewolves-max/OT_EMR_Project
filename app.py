import streamlit as dict
import streamlit as st
import database
import functions

# I-set up ang pahina ng app
st.set_page_config(layout="wide") # Ginagawang malawak ang screen para sa split-screen

st.title("🩺 Occupational Therapy - EMR System")
st.write("---")

# 1. SIDEBAR: Para sa pagpili o pag-add ng Pasyente
st.sidebar.header("👤 Patient Selection")

# Para sa demo, maglalagay muna tayo ng default Patient ID (si Baby Juan)
# Sa susunod na hakbang, gagawa tayo ng drop-down para sa lahat ng pasyente.
patient_id = 1 
st.sidebar.write(f"**Current Patient ID:** {patient_id}")
st.sidebar.info("Tip: Dito mo mapipili ang pangalan ng bata sa susunod nating update!")

# 2. SPLIT-SCREEN LAYOUT (Gagawa ng 2 Columns: Kaliwa at Kanan)
col_soap, col_goals = st.columns([3, 2]) # 3:2 ratio para mas malawak ang SOAP notes

# --- KALIWANG COLUMN: SOAP NOTES ---
with col_soap:
    st.header("📝 Daily Session Note (SOAP)")
    
    # Mga input fields para sa SOAP
    s_input = st.text_area("Subjective (S)", placeholder="Ano ang sinabi ng magulang o bata ngayon?", height=80)
    o_input = st.text_area("Objective (O)", placeholder="Performance sa laro, buttoning, fine motor tasks...", height=120)
    a_input = st.text_area("Assessment (A)", placeholder="Clinical reasoning. Bakit naging ganun ang performance?", height=100)
    p_input = st.text_area("Plan (P)", placeholder="Ano ang gagawin sa susunod na session?", height=80)
    
    # Button para mag-save
    if st.button("💾 Save SOAP Note", type="primary"):
        # Tatawagin natin ang utusan sa functions.py para i-save sa sqlite
        functions.save_soap_note(patient_id, s_input, o_input, a_input, p_input)
        st.success("Yehey! Matagumpay na nai-save ang SOAP Note sa database natin!")

# --- KANANG COLUMN: GOALS AND TARGETS ---
with col_goals:
    st.header("🎯 Target Goals")
    st.write("Gantt/Target monitoring para sa session ngayon:")
    
    # Mag-add ng mabilisang form para magdagdag ng bagong goal ng bata
    with st.expander("➕ Magdagdag ng Bagong Goal"):
        new_goal_desc = st.text_input("Goal Description", placeholder="e.g., Button 3 large buttons independently")
        if st.button("Add Goal"):
            if new_goal_desc:
                functions.add_goal(patient_id, new_goal_desc)
                st.success("Bagong goal naidagdag!")
                st.rerun() # I-refresh ang screen para lumitaw agad ang bagong goal
    
    # Kunin at ipakita ang mga Active Goals ni Baby Juan mula sa database
    active_goals = functions.get_active_goals(patient_id)
    
    if not active_goals:
        st.warning("Walang aktibong goal si Baby Juan sa kasalukuyan. Magdagdag sa itaas!")
    else:
        for goal_id, description in active_goals:
            # Ipakita ang bawat goal na may checkbox para pwedeng i-track
            st.checkbox(f"**Goal #{goal_id}:** {description}", key=f"goal_{goal_id}")