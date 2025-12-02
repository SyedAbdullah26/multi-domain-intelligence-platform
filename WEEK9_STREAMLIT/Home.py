# Home.py
import streamlit as st
from app_backend.users import register_user, login_user
from app_backend.theme import apply_cyber_theme, render_sidebar

st.set_page_config(page_title="Cyber Portal - Login", page_icon="🟢", layout="centered")

apply_cyber_theme()
render_sidebar()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = "analyst"

st.title("🧬 Cyber Intelligence Portal")

tab1, tab2 = st.tabs(["Login", "Register"])

# ---------------- LOGIN ----------------
with tab1:
    st.subheader("🔐 Sign In")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        success, msg, role = login_user(user, pwd)
        if success:
            st.session_state.logged_in = True
            st.session_state.username = user
            st.session_state.role = role or "analyst"
            st.success("Access Granted ✔")
            st.switch_page("pages/1_Dashboard.py")
        else:
            st.error(msg)

# --------------- REGISTER --------------
def password_strength(password: str):
    score = 0
    if len(password) >= 8:
        score += 1
    if any(c.islower() for c in password) and any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in "!@#$%^&*()-_=+[]{};:,.<>?/\\|" for c in password):
        score += 1

    if score <= 1:
        return "Very Weak"
    elif score == 2:
        return "Weak"
    elif score == 3:
        return "Medium"
    else:
        return "Strong"

with tab2:
    st.subheader("🆕 Register Account")

    new_user = st.text_input("New Username")
    new_pwd = st.text_input("New Password", type="password")
    role_choice = st.selectbox("Role", ["analyst", "admin"])

    if new_pwd:
        strength = password_strength(new_pwd)
        st.markdown(f"**Password strength:** {strength}")

    if st.button("Create Account"):
        success, msg = register_user(new_user, new_pwd, role_choice)
        if success:
            st.success("Account created successfully. You can log in now.")
        else:
            st.error(msg)
