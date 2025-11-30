import streamlit as st

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please login first!")
    st.stop()

st.title("👤 Profile")

st.write(f"**Username:** {st.session_state.username}")

if st.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.switch_page("Home.py")
