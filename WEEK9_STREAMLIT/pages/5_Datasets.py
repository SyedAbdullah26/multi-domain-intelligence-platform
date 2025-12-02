# pages/5_Datasets.py
import streamlit as st
from app_backend.theme import apply_cyber_theme, render_sidebar
from app_backend.datasets import load_datasets

st.set_page_config(page_title="Datasets", page_icon="📚", layout="wide")

apply_cyber_theme()
render_sidebar()

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Login required.")
    st.stop()

st.title("📚 Dataset Metadata")

df = load_datasets()

col1, col2, col3 = st.columns(3)
col1.metric("Datasets", len(df))
col2.metric("Unique Sources", df["source"].nunique() if "source" in df.columns else 0)
col3.metric("Total Records", int(df["record_count"].sum()) if "record_count" in df.columns else 0)

st.divider()

colA, colB = st.columns(2)
with colA:
    st.subheader("Source Distribution")
    if "source" in df.columns and not df.empty:
        st.bar_chart(df["source"].value_counts())
    else:
        st.info("No source data available.")

with colB:
    st.subheader("Record Count per Dataset")
    if "dataset_name" in df.columns and "record_count" in df.columns and not df.empty:
        st.bar_chart(df[["dataset_name", "record_count"]].set_index("dataset_name"))
    else:
        st.info("No dataset/record_count data available.")

st.divider()
st.subheader("📄 Full Dataset Table")
st.dataframe(df, use_container_width=True)
