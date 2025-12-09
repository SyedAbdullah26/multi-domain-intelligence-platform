# pages/2_Incidents.py
import streamlit as st
from datetime import date
from app_backend.theme import apply_cyber_theme, render_sidebar
from app_backend.incidents import load_incidents, insert_incident

st.set_page_config(page_title="Incidents", page_icon="🛡", layout="wide")

apply_cyber_theme()
render_sidebar()

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Login required.")
    st.stop()

st.title("🛡 Incident Management")

tab1, tab2 = st.tabs(["View Incidents", "Add Incident"])

with tab1:
    df = load_incidents()
    st.dataframe(df, use_container_width=True)

with tab2:
    inc_date = st.date_input("Date Reported", date.today())
    inc_type = st.text_input("Incident Type")
    severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
    status = st.selectbox("Status", ["Open", "Closed"])
    desc = st.text_area("Description")

    if st.button("Save Incident"):
        username = st.session_state.get("username", "system")
        insert_incident(
            inc_date.isoformat(),
            inc_type,
            severity,
            status,
            desc,
            username,
        )
        st.success("Incident saved successfully ✔")
