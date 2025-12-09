import streamlit as st
import pandas as pd
from datetime import date

from app_backend.theme import apply_cyber_theme, render_sidebar
from app_backend.tickets import (
    load_tickets,
    load_deleted_tickets,
    insert_ticket,
    update_ticket,
    delete_ticket,
    restore_ticket,
    purge_ticket,
)
from app_backend.db import connect_database

st.set_page_config(page_title="IT Tickets", page_icon="🎫", layout="wide")
apply_cyber_theme()
render_sidebar()

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Login required.")
    st.stop()

st.title("🎫 IT Tickets (CRUD + Search + Bin)")


def get_schema():
    conn = connect_database()
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(it_tickets)")
    info = cur.fetchall()
    conn.close()
    cols = [x[1] for x in info]
    pk = [x[1] for x in info if x[5] == 1]
    return cols, pk[0] if pk else cols[0]


cols, pk_col = get_schema()

tab1, tab2, tab3 = st.tabs(
    ["📄 Active (Search / Edit / Delete)", "➕ Add Ticket", "🗑 Recycle Bin"]
)

# ================= ACTIVE ================= #
with tab1:
    df = load_tickets()
    st.subheader("📄 Active Tickets")

    if df is None or df.empty:
        st.info("No active tickets.")
    else:
        search = st.text_input("🔎 Search tickets", "")
        priority_filter = st.multiselect(
            "Filter by Priority",
            ["Low", "Medium", "High", "Critical"] if "priority" in df.columns else [],
        )
        status_filter = st.multiselect(
            "Filter by Status",
            ["Open", "Closed", "In Progress"] if "status" in df.columns else [],
        )

        filtered = df.copy()
        if search.strip():
            mask = pd.Series(False, index=filtered.index)
            for col in ["ticket_id", "description", "assigned_to", "status", "priority"]:
                if col in filtered.columns:
                    mask |= filtered[col].astype(str).str.contains(
                        search, case=False, na=False
                    )
            filtered = filtered[mask]

        if priority_filter and "priority" in filtered.columns:
            filtered = filtered[filtered["priority"].isin(priority_filter)]

        if status_filter and "status" in filtered.columns:
            filtered = filtered[filtered["status"].isin(status_filter)]

        st.dataframe(filtered, use_container_width=True)

        if not filtered.empty:
            st.markdown("### ✏ Edit or ❌ Delete Ticket")
            selected_id = st.selectbox("Select Ticket:", filtered[pk_col].tolist())
            row = df[df[pk_col] == selected_id].iloc[0]

            with st.form("edit_ticket"):
                updated = {}
                for col in cols:
                    val = row[col]
                    if col == pk_col:
                        st.text_input(col, value=str(val), disabled=True)
                    elif col == "date_created":
                        try:
                            d_val = date.fromisoformat(str(val))
                        except:
                            d_val = date.today()
                        updated[col] = st.date_input(col, d_val).isoformat()
                    else:
                        updated[col] = st.text_input(
                            col, value=str(val) if val else ""
                        )

                c1, c2 = st.columns(2)
                save_btn = c1.form_submit_button("💾 Save Changes")
                del_btn = c2.form_submit_button("🗑 Move to Recycle Bin")

            if save_btn:
                update_ticket(pk_col, selected_id, updated)
                st.success("Ticket updated ✔")
                st.experimental_rerun()

            if del_btn:
                delete_ticket(pk_col, selected_id)
                st.warning("Ticket moved to Recycle Bin ♻")
                st.experimental_rerun()

# ================= ADD ================= #
with tab2:
    st.subheader("➕ Add Ticket")

    ticket_id = st.text_input("Ticket ID (unique)")
    date_created = st.date_input("Date Created", date.today())
    priority = st.text_input("Priority (e.g. Low/Medium/High)")
    status = st.text_input("Status (e.g. Open/Closed)")
    description = st.text_area("Description")
    assigned_to = st.text_input("Assigned To")

    if st.button("💾 Save Ticket"):
        if ticket_id.strip():
            insert_ticket(
                ticket_id,
                date_created.isoformat(),
                priority,
                status,
                description,
                assigned_to,
            )
            st.success("Ticket added ✔")
            st.experimental_rerun()
        else:
            st.error("Ticket ID cannot be empty ❌")

# ================= BIN ================= #
with tab3:
    st.subheader("🗑 Recycle Bin — Tickets")

    deleted_df = load_deleted_tickets()
    if deleted_df is None or deleted_df.empty:
        st.info("Recycle Bin is empty.")
    else:
        st.dataframe(deleted_df, use_container_width=True)

        selected_deleted = st.selectbox(
            "Select deleted ticket:", deleted_df[pk_col].tolist()
        )

        c1, c2 = st.columns(2)
        restore_btn = c1.button("♻ Restore Ticket")
        purge_btn = c2.button("🔥 Delete Permanently")

        if restore_btn:
            restore_ticket(pk_col, selected_deleted)
            st.success("Ticket restored ✔")
            st.experimental_rerun()

        if purge_btn:
            purge_ticket(pk_col, selected_deleted)
            st.error("Ticket permanently deleted ❌")
            st.experimental_rerun()
