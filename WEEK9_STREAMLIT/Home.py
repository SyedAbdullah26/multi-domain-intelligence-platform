import streamlit as st
from app_backend.users import register_user, login_user

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(
    page_title="Cyber Login Portal",
    page_icon="🔐",
    layout="centered"
)

# -----------------------------
# Session State Initialization
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# -----------------------------
# Cyber-Themed Styling
# -----------------------------
st.markdown("""
<style>
    .stApp {
        background-color: #02040a;
        color: #00ff9d;
        font-family: "Consolas", "Fira Code", monospace;
    }

    .block-container {
        padding-top: 5%;
    }

    .stTabs [data-baseweb="tab"] {
        color: #00ff9d !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: #00ff9d22 !important;
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #00ff9d33 !important;
        color: white !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: #00ff9d22;
        color: #00ff9d;
        border: 1px solid #00ff9d88;
    }

    .stButton > button:hover {
        background-color: #00ff9d44;
        color: white;
        border-color: #00ff9d;
    }

    input, textarea {
        background-color: #020814 !important;
        color: #00ff9d !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# UI Header
# -----------------------------
st.title("🔐 Cyber Intelligence Access Portal")
st.caption("Authorized Analysts Only. Access is monitored.")

# If user already logged in
if st.session_state.logged_in:
    st.success(f"You are already logged in as **{st.session_state.username}**.")
    if st.button("Go to Dashboard"):
        st.switch_page("pages/1_Dashboard.py")
    st.stop()

# -----------------------------
# Tabs for Login / Register
# -----------------------------
tab_login, tab_register = st.tabs(["Login", "Register"])

# -----------------------------
# Login Tab
# -----------------------------
with tab_login:
    st.subheader("Log in to your analyst account")

    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Log In"):
        success, message = login_user(username, password)
        if success:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful. Loading your dashboard...")
            st.switch_page("pages/1_Dashboard.py")
        else:
            st.error(message)

# -----------------------------
# Register Tab
# -----------------------------
with tab_register:
    st.subheader("Create a new analyst account")

    new_user = st.text_input("Choose a username", key="reg_user")
    new_pass = st.text_input("Choose a password", type="password", key="reg_pass")
    confirm = st.text_input("Confirm password", type="password", key="reg_confirm")

    if st.button("Create Account"):
        if new_pass != confirm:
            st.error("Your passwords do not match. Try again.")
        else:
            success, message = register_user(new_user, new_pass)
            if success:
                st.success("Account created successfully! Please log in.")
            else:
                st.error(message)
