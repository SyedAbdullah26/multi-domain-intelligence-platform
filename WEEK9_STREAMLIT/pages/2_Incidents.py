import streamlit as st
from datetime import date
from app_backend.incidents import get_all_incidents, insert_incident

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(
    page_title="Incident Management",
    page_icon="🛡",
    layout="wide"
)

# Access control
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in to view this page.")
    if st.button("Back to Login"):
        st.switch_page("Home.py")
    st.stop()

# Cyber-themed styling
st.markdown("""
<style>
    .stApp {
        background-color: #02040a;
        color: #00ff9d;
        font-family: "Consolas", "Fira Code", monospace;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Page Title
# -----------------------------
st.title("🛡 Incident Management Console")

# -----------------------------
# Tabs (View / Add Incident)
# -----------------------------
tab_view, tab_add = st.tabs([
    "📁 View Incidents",
    "➕ Add New Incident"
])

# =======================
# VIEW INCIDENTS TAB
# =======================
with tab_view:
    st.subheader("All Recorded Incidents")

    try:
        df = get_all_incidents()
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Could not load incidents: {e}")

# =======================
# ADD INCIDENT TAB
# =======================
with tab_add:
    st.subheader("Log a New Security Incident")

    with st.form("add_incident_form"):
        inc_date = st.date_input("Date of Incident", date.today())
        inc_type = st.text_input("Incident Type (e.g., Phishing, Malware)")
        severity = st.selectbox("Severity Level", ["Low", "Medium", "High"])
        status = st.selectbox("Current Status", ["Open", "Closed"])
        description = st.text_area("Detailed Description")

        submit = st.form_submit_button("Create Incident")

    if submit:
        try:
            insert_incident(
                inc_date.isoformat(),
                inc_type,
                severity,
                status,
                description,
                st.session_state.username
            )
            st.success("Incident successfully logged!")
            st.balloons()
            st.rerun()
        except Exception as e:
            st.error(f"Failed to add incident: {e}")
