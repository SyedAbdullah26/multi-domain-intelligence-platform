import streamlit as st
from datetime import date, datetime
import pandas as pd

from app_backend.theme import apply_cyber_theme, render_sidebar
from app_backend.incidents import (
    load_incidents,
    load_deleted_incidents,
    insert_incident,
    update_incident,
    delete_incident,
    restore_incident,
    purge_incident,
)
from app_backend.db import connect_database

st.set_page_config(page_title="Incidents", page_icon="🛡", layout="wide")
apply_cyber_theme()
render_sidebar()

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Login required.")
    st.stop()

st.title("🛡 Incident Management (CRUD + Search + Bin)")


def get_schema():
    conn = connect_database()
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(cyber_incidents)")
    info = cur.fetchall()
    conn.close()
    cols = [x[1] for x in info]
    pk = [x[1] for x in info if x[5] == 1]
    return cols, pk[0] if pk else cols[0]


cols, pk_col = get_schema()

tab1, tab2, tab3 = st.tabs(
    ["📄 Active (Search / Edit / Delete)", "➕ Add Incident", "🗑 Recycle Bin"]
)

# ================= ACTIVE ================= #
with tab1:
    df = load_incidents()
    st.subheader("📄 Active Incidents")

    if df is None or df.empty:
        st.info("No active incidents.")
    else:
        # Search + Filters
        search = st.text_input("🔎 Search text", "")
        severity_filter = st.multiselect(
            "Filter by Severity", ["Low", "Medium", "High", "Critical"]
        )
        status_filter = st.multiselect("Filter by Status", ["Open", "Closed"])

        filtered = df.copy()
        if search.strip():
            mask = pd.Series(False, index=filtered.index)
            for col in ["incident_type", "description", "reported_by", "status", "severity"]:
                if col in filtered.columns:
                    mask |= filtered[col].astype(str).str.contains(
                        search, case=False, na=False
                    )
            filtered = filtered[mask]

        if severity_filter and "severity" in filtered.columns:
            filtered = filtered[filtered["severity"].isin(severity_filter)]

        if status_filter and "status" in filtered.columns:
            filtered = filtered[filtered["status"].isin(status_filter)]

        st.dataframe(filtered, use_container_width=True)

        if not filtered.empty:
            st.markdown("### ✏ Edit or ❌ Delete Incident")
            selected_id = st.selectbox(
                "Select Incident:", filtered[pk_col].tolist()
            )
            row = df[df[pk_col] == selected_id].iloc[0]

            with st.form("edit_inc"):
                updated = {}
                for col in cols:
                    val = row[col]
                    if col == pk_col:
                        st.text_input(col, value=str(val), disabled=True)
                    elif col == "date_reported":
                        try:
                            parsed = datetime.fromisoformat(str(val)).date()
                        except:
                            parsed = date.today()
                        updated[col] = st.date_input(col, parsed).isoformat()
                    elif col == "severity":
                        choices = ["Low", "Medium", "High", "Critical"]
                        updated[col] = st.selectbox(
                            col,
                            choices,
                            index=choices.index(str(val))
                            if val in choices
                            else 0,
                        )
                    elif col == "status":
                        choices = ["Open", "Closed"]
                        updated[col] = st.selectbox(
                            col,
                            choices,
                            index=choices.index(str(val))
                            if val in choices
                            else 0,
                        )
                    else:
                        updated[col] = st.text_input(
                            col, value=str(val) if val else ""
                        )

                c1, c2 = st.columns(2)
                save_btn = c1.form_submit_button("💾 Save Changes")
                del_btn = c2.form_submit_button("🗑 Move to Recycle Bin")

            if save_btn:
                update_incident(pk_col, selected_id, updated)
                st.success("Incident updated ✔")
                st.experimental_rerun()

            if del_btn:
                delete_incident(pk_col, selected_id)
                st.warning("Incident moved to Recycle Bin ♻")
                st.experimental_rerun()

# ================= ADD ================= #
with tab2:
    st.subheader("➕ Add New Incident")

    dt = st.date_input("Date Reported", date.today())
    inc_type = st.text_input("Incident Type")
    severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
    status = st.selectbox("Status", ["Open", "Closed"])
    desc = st.text_area("Description")
    user = st.session_state.get("username", "system")

    if st.button("💾 Save Incident"):
        if inc_type.strip():
            insert_incident(dt.isoformat(), inc_type, severity, status, desc, user)
            st.success("Incident added ✔")
            st.experimental_rerun()
        else:
            st.error("Incident type cannot be empty ❌")

# ================= BIN ================= #
with tab3:
    st.subheader("🗑 Recycle Bin — Incidents")

    deleted_df = load_deleted_incidents()
    if deleted_df is None or deleted_df.empty:
        st.info("Recycle Bin is empty.")
    else:
        st.dataframe(deleted_df, use_container_width=True)

        selected_deleted = st.selectbox(
            "Select deleted incident:", deleted_df[pk_col].tolist()
        )

        c1, c2 = st.columns(2)
        restore_btn = c1.button("♻ Restore Incident")
        purge_btn = c2.button("🔥 Delete Permanently")

        if restore_btn:
            restore_incident(pk_col, selected_deleted)
            st.success("Incident restored ✔")
            st.experimental_rerun()

        if purge_btn:
            purge_incident(pk_col, selected_deleted)
            st.error("Incident permanently deleted ❌")
            st.experimental_rerun()
