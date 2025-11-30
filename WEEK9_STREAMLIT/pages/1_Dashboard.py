import streamlit as st
import pandas as pd
from app_backend.incidents import get_all_incidents

# Page & Style Setup

st.set_page_config(
    page_title="Cyber Threat Dashboard",
    page_icon="🧬",
    layout="wide"
)

# Ensure user is logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must log in to access the dashboard.")
    if st.button("Back to Login"):
        st.switch_page("Home.py")
    st.stop()

# Cyber styling
st.markdown("""
<style>
    .stApp {
        background-color: #02040a;
        color: #00ff9d;
        font-family: "Consolas", "Fira Code", monospace;
    }
</style>
""", unsafe_allow_html=True)

# Dashboard Header

st.title("🧬 Cyber Threat Intelligence Dashboard")
st.caption(f"Analyst logged in: {st.session_state.username}")

# Load Incident Data

try:
    incidents = get_all_incidents()
    incidents["date_reported"] = pd.to_datetime(incidents["date_reported"], errors="coerce")
except Exception as e:
    st.error(f"Unable to load database data: {e}")
    st.stop()

# Sidebar Filtering

with st.sidebar:
    st.header("Filters")

    severities = ["All"] + sorted(incidents["severity"].dropna().unique().tolist())
    selected_sev = st.selectbox("Severity", severities)

    statuses = ["All"] + sorted(incidents["status"].dropna().unique().tolist())
    selected_status = st.selectbox("Status", statuses)

    # Date filtering
    min_d, max_d = incidents["date_reported"].min(), incidents["date_reported"].max()
    date_range = st.date_input("Date Range", (min_d, max_d))

# Apply filters
df = incidents.copy()

if selected_sev != "All":
    df = df[df["severity"] == selected_sev]

if selected_status != "All":
    df = df[df["status"] == selected_status]

if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    df = df[(df["date_reported"] >= start) & (df["date_reported"] <= end)]

# KPI Metrics

total = len(df)
open_cases = (df["status"] == "Open").sum()
critical = (df["severity"].isin(["High", "Critical"])).sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total Incidents", total)
col2.metric("Open Incidents", open_cases)
col3.metric("High Severity", critical)

st.divider()

# Charts

colA, colB = st.columns(2)

with colA:
    st.subheader("📊 Severity Breakdown")
    st.bar_chart(df["severity"].value_counts())

with colB:
    st.subheader("📈 Incidents Over Time")
    trend = df.set_index("date_reported").resample("D").size()
    st.line_chart(trend)

st.divider()

# Table

with st.expander("🗄 Raw Incident Data"):
    st.dataframe(df, use_container_width=True)

# Logout

if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.success("You have been logged out.")
    st.switch_page("Home.py")
