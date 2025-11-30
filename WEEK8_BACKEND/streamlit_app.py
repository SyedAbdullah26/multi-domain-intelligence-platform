# streamlit_app.py — Streamlit interface with role-based auth (Admin / Analyst)
import streamlit as st
from pathlib import Path
import pandas as pd
import io
import sqlite3
import traceback

# Import your backend functions / modules
# Make sure your project package structure is in PYTHONPATH (or run from project root)
from app.data.db import connect_database
from main import load_all_csv_data          # from the enhanced main.py we created
from app.services.user_service import register_user, login_user
from app.data.incidents import insert_incident, get_all_incidents

# -----------------------------
# App Config / Constants
# -----------------------------
st.set_page_config(page_title="Incident Dashboard", layout="wide")
DATA_DIR = Path("DATA")
DATA_DIR.mkdir(exist_ok=True)


# -----------------------------
# Helper functions
# -----------------------------
def get_conn():
    """Return a new DB connection using your project's connect_database."""
    return connect_database()


def init_session_state():
    """Initialize keys used in session_state."""
    if "user" not in st.session_state:
        st.session_state.user = None  # dict with keys: username, role
    if "login_error" not in st.session_state:
        st.session_state.login_error = ""
    if "message" not in st.session_state:
        st.session_state.message = ""


def require_login():
    """Return True if logged in, otherwise show notice and return False."""
    if st.session_state.user is None:
        st.warning("Please log in to access the dashboard.")
        return False
    return True


def show_table_from_sql(conn, table_name, limit=500):
    """Utility to display a table from the DB."""
    try:
        df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT {limit}", conn)
        st.dataframe(df)
        return df
    except Exception as e:
        st.error(f"Error reading table {table_name}: {e}")
        return pd.DataFrame()


def upload_and_process_file(uploaded_file):
    """
    Save uploaded CSV to DATA_DIR and call load_all_csv_data.
    We save the file exactly with its filename so the loader can find it.
    """
    try:
        if uploaded_file is None:
            st.info("No file uploaded.")
            return 0

        save_path = DATA_DIR / uploaded_file.name
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"Saved uploaded file to {save_path}. Running CSV loader...")
        conn = get_conn()
        rows = load_all_csv_data(conn)
        conn.close()
        st.success(f"Loader finished. {rows} rows imported/updated (total from all CSVs).")
        return rows
    except Exception as e:
        st.error(f"Upload or processing failed: {e}")
        traceback.print_exc()
        return 0


# -----------------------------
# UI: Authentication Pages
# -----------------------------
def register_page():
    st.title("Register a new user")
    st.info("Create an account — choose role: Admin or Analyst")

    with st.form("register_form", clear_on_submit=True):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["analyst", "admin"])
        submitted = st.form_submit_button("Register")

    if submitted:
        if not username or not password:
            st.error("Please provide username and password.")
            return

        try:
            success, msg = register_user(username, password, role)
            if success:
                st.success(f"Registered {username} as {role}. You may now log in.")
            else:
                st.error(msg)
        except Exception as e:
            st.error(f"Registration failed: {e}")
            traceback.print_exc()


def login_page():
    st.title("Login")
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        try:
            success, msg = login_user(username, password)
            if success:
                # assume login_user returns (True, role_or_message) or (True, "Logged in")
                # To be safe, if login_user returns a message only, we need to fetch role from DB
                # but many user_service implementations return (True, "role") or (True, "OK")
                # We'll fetch role from users table if needed.
                conn = get_conn()
                df = pd.read_sql_query("SELECT username, role FROM users WHERE username = ?", conn, params=(username,))
                conn.close()
                if not df.empty:
                    role = df.iloc[0]["role"]
                else:
                    # default fallback
                    role = "analyst"
                st.session_state.user = {"username": username, "role": role}
                st.success(f"Logged in as {username} ({role})")
            else:
                st.session_state.login_error = msg or "Login failed"
                st.error(st.session_state.login_error)
        except Exception as e:
            st.error(f"Login error: {e}")
            traceback.print_exc()


def logout():
    st.session_state.user = None
    st.success("Logged out.")


# -----------------------------
# UI: Dashboard Pages
# -----------------------------
def dashboard_home():
    st.title("Incident Dashboard")
    st.write("Welcome, ", st.session_state.user["username"], f" — role: {st.session_state.user['role']}")

    conn = get_conn()
    # Quick KPIs
    try:
        incidents_df = pd.read_sql_query("SELECT * FROM cyber_incidents", conn)
        tickets_df = pd.read_sql_query("SELECT * FROM it_tickets", conn)
        datasets_df = pd.read_sql_query("SELECT * FROM datasets_metadata", conn)
    except Exception:
        incidents_df = get_all_incidents()
        tickets_df = pd.DataFrame()
        datasets_df = pd.DataFrame()

    col1, col2, col3 = st.columns(3)
    col1.metric("Incidents", len(incidents_df))
    col2.metric("IT Tickets", len(tickets_df))
    col3.metric("Datasets", len(datasets_df))

    conn.close()

    st.markdown("---")
    st.subheader("Quick Actions")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.button("Refresh data", on_click=lambda: st.experimental_rerun())
    with c2:
        st.button("Open add incident panel", on_click=lambda: st.session_state.update({"open_add_incident": True}))
    with c3:
        st.button("Upload CSV", on_click=lambda: st.session_state.update({"open_upload": True}))


def view_incidents():
    st.header("Cyber Incidents")
    conn = get_conn()
    try:
        df = pd.read_sql_query("SELECT rowid as id, * FROM cyber_incidents", conn)
    except Exception:
        df = get_all_incidents()
        df = df.reset_index().rename(columns={"index": "id"})
    finally:
        conn.close()

    st.write(f"Total: {len(df)} incidents")

    # Simple search/filter
    q = st.text_input("Search description / incident type")
    if q:
        df = df[df.apply(lambda r: q.lower() in str(r.to_dict()).lower(), axis=1)]

    st.dataframe(df)

    if st.session_state.user["role"] == "admin":
        st.markdown("**Admin actions**")
        row_to_delete = st.number_input("Row id to delete (rowid)", min_value=0, step=1, value=0)
        if st.button("Delete row (admin)"):
            try:
                conn = get_conn()
                conn.execute("DELETE FROM cyber_incidents WHERE rowid = ?", (row_to_delete,))
                conn.commit()
                conn.close()
                st.success(f"Deleted row {row_to_delete}. Refresh to see updates.")
            except Exception as e:
                st.error(f"Delete failed: {e}")
                traceback.print_exc()


def add_incident_form():
    st.header("Add Incident")
    with st.form("add_incident_form"):
        date_reported = st.date_input("Date reported")
        incident_type = st.text_input("Incident type")
        severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
        status = st.selectbox("Status", ["Open", "Investigating", "Resolved", "Closed"])
        description = st.text_area("Description")
        submitted = st.form_submit_button("Create Incident")

    if submitted:
        try:
            # insert_incident signature in your code: (date, type, severity, status, description, reported_by)
            incident_id = insert_incident(
                date_reported.isoformat(), incident_type, severity, status, description, st.session_state.user["username"]
            )
            st.success(f"Created incident ID: {incident_id}")
        except Exception as e:
            st.error(f"Failed to create incident: {e}")
            traceback.print_exc()


def view_it_tickets():
    st.header("IT Tickets")
    conn = get_conn()
    df = show_table_from_sql(conn, "it_tickets")
    conn.close()


def view_datasets():
    st.header("Datasets Metadata")
    conn = get_conn()
    df = show_table_from_sql(conn, "datasets_metadata")
    conn.close()


def upload_csv_ui():
    st.header("Upload CSV file (will save to DATA/ and run loader)")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    if st.button("Upload and process"):
        if uploaded_file:
            rows = upload_and_process_file(uploaded_file)
            st.success(f"Loader processed files and imported {rows} rows total (across all CSVs).")
        else:
            st.error("Please choose a file first.")


def manage_users():
    st.header("User Management (Admin only)")
    conn = get_conn()
    df = pd.read_sql_query("SELECT username, role FROM users", conn)
    conn.close()
    st.dataframe(df)

    st.markdown("**Create a user**")
    with st.form("create_user_form"):
        username = st.text_input("Username for new user")
        password = st.text_input("Password for new user", type="password")
        role = st.selectbox("Role", ["analyst", "admin"])
        submitted = st.form_submit_button("Create user")
    if submitted:
        try:
            success, msg = register_user(username, password, role)
            if success:
                st.success(f"User {username} created.")
            else:
                st.error(msg)
        except Exception as e:
            st.error(f"Create failed: {e}")
            traceback.print_exc()


# -----------------------------
# App Layout & Routing
# -----------------------------
def main():
    init_session_state()
    st.sidebar.title("Navigation")
    if st.session_state.user is None:
        page = st.sidebar.selectbox("Go to", ["Login", "Register", "About"])
    else:
        page = st.sidebar.selectbox(
            "Go to",
            ["Home", "Incidents", "Add Incident", "IT Tickets", "Datasets", "Upload CSV", "About", "Logout"]
        )

    if page == "Login":
        login_page()
    elif page == "Register":
        register_page()
    elif page == "About":
        st.title("About this App")
        st.markdown(
            """
            Incident management demo dashboard.
            - Role-based access (admin / analyst)
            - Upload CSVs (saved to DATA/)
            - Uses your backend DB & service functions
            """
        )
    else:
        # Require login for everything beyond auth pages
        if not require_login():
            return

        # Show Logout button in header for convenience
        col1, col2 = st.columns([8, 2])
        col1.markdown(f"### Hello, **{st.session_state.user['username']}** ({st.session_state.user['role']})")
        if col2.button("Logout"):
            logout()
            st.experimental_rerun()

        # Route to pages
        if page == "Home":
            dashboard_home()
        elif page == "Incidents":
            view_incidents()
        elif page == "Add Incident":
            add_incident_form()
        elif page == "IT Tickets":
            view_it_tickets()
        elif page == "Datasets":
            view_datasets()
        elif page == "Upload CSV":
            upload_csv_ui()
        elif page == "Logout":
            logout()
            st.experimental_rerun()

        # Admin-only section
        if st.session_state.user["role"] == "admin":
            st.markdown("---")
            manage_users()


if __name__ == "__main__":
    main()
