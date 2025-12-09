import streamlit as st
import pandas as pd
from datetime import date

from app_backend.theme import apply_cyber_theme, render_sidebar
from app_backend.datasets import (
    load_datasets,
    load_deleted_datasets,
    insert_dataset,
    update_dataset,
    delete_dataset,
    restore_dataset,
    purge_dataset,
)
from app_backend.db import connect_database

st.set_page_config(page_title="Datasets", page_icon="📚", layout="wide")
apply_cyber_theme()
render_sidebar()

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Login required.")
    st.stop()

st.title("📚 Dataset Metadata (CRUD + Search + Bin)")


def get_schema():
    conn = connect_database()
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(datasets_metadata)")
    info = cur.fetchall()
    conn.close()
    cols = [x[1] for x in info]
    pk = [x[1] for x in info if x[5] == 1]
    return cols, pk[0] if pk else cols[0]


cols, pk_col = get_schema()

tab1, tab2, tab3 = st.tabs(
    ["📄 Active (Search / Edit / Delete)", "➕ Add Dataset", "🗑 Recycle Bin"]
)

# ================= ACTIVE ================= #
with tab1:
    df = load_datasets()
    st.subheader("📄 Active Datasets")

    if df is None or df.empty:
        st.info("No active datasets.")
    else:
        search = st.text_input("🔎 Search datasets", "")
        source_filter = st.multiselect(
            "Filter by Source",
            sorted(df["source"].dropna().unique()) if "source" in df.columns else [],
        )

        filtered = df.copy()
        if search.strip():
            mask = pd.Series(False, index=filtered.index)
            for col in ["dataset_name", "source", "description"]:
                if col in filtered.columns:
                    mask |= filtered[col].astype(str).str.contains(
                        search, case=False, na=False
                    )
            filtered = filtered[mask]

        if source_filter and "source" in filtered.columns:
            filtered = filtered[filtered["source"].isin(source_filter)]

        st.dataframe(filtered, use_container_width=True)

        if not filtered.empty:
            st.markdown("### ✏ Edit or ❌ Delete Dataset")
            selected_id = st.selectbox(
                "Select Dataset:", filtered[pk_col].tolist()
            )
            row = df[df[pk_col] == selected_id].iloc[0]

            with st.form("edit_ds"):
                updated = {}
                for col in cols:
                    val = row[col]
                    if col == pk_col:
                        st.text_input(col, value=str(val), disabled=True)
                    elif col == "record_count":
                        try:
                            num = int(val) if val is not None else 0
                        except:
                            num = 0
                        updated[col] = st.number_input(col, value=num, step=1)
                    else:
                        updated[col] = st.text_input(
                            col, value=str(val) if val else ""
                        )

                c1, c2 = st.columns(2)
                save_btn = c1.form_submit_button("💾 Save Changes")
                del_btn = c2.form_submit_button("🗑 Move to Recycle Bin")

            if save_btn:
                update_dataset(pk_col, selected_id, updated)
                st.success("Dataset updated ✔")
                st.experimental_rerun()

            if del_btn:
                delete_dataset(pk_col, selected_id)
                st.warning("Dataset moved to Recycle Bin ♻")
                st.experimental_rerun()

# ================= ADD ================= #
with tab2:
    st.subheader("➕ Add Dataset")

    dataset_name = st.text_input("Dataset Name (unique)")
    source = st.text_input("Source")
    record_count = st.number_input("Record Count", min_value=0, step=1)
    last_updated = st.text_input("Last Updated (text or date)")
    description = st.text_area("Description")

    if st.button("💾 Save Dataset"):
        if dataset_name.strip():
            insert_dataset(dataset_name, source, record_count, last_updated, description)
            st.success("Dataset added ✔")
            st.experimental_rerun()
        else:
            st.error("Dataset name cannot be empty ❌")

# ================= BIN ================= #
with tab3:
    st.subheader("🗑 Recycle Bin — Datasets")

    deleted_df = load_deleted_datasets()
    if deleted_df is None or deleted_df.empty:
        st.info("Recycle Bin is empty.")
    else:
        st.dataframe(deleted_df, use_container_width=True)

        selected_deleted = st.selectbox(
            "Select deleted dataset:", deleted_df[pk_col].tolist()
        )

        c1, c2 = st.columns(2)
        restore_btn = c1.button("♻ Restore Dataset")
        purge_btn = c2.button("🔥 Delete Permanently")

        if restore_btn:
            restore_dataset(pk_col, selected_deleted)
            st.success("Dataset restored ✔")
            st.experimental_rerun()

        if purge_btn:
            purge_dataset(pk_col, selected_deleted)
            st.error("Dataset permanently deleted ❌")
            st.experimental_rerun()
