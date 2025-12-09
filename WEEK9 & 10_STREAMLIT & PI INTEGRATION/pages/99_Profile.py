# pages/99_Profile.py
import streamlit as st
from app_backend.theme import apply_cyber_theme, render_sidebar

st.set_page_config(page_title="Profile", page_icon="👤", layout="centered")

apply_cyber_theme()
render_sidebar()

st.title("👤 User Profile")

username = st.session_state.get("username", "Unknown")
role = st.session_state.get("role", "analyst")

st.subheader(f"Logged in as: `{username}`")
st.markdown(f"**Role:** `{role}`")

st.markdown("---")
st.markdown("This profile page demonstrates role-based access control and session management.")

if st.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = "analyst"
    st.success("You have been logged out.")
    st.switch_page("Home.py")
