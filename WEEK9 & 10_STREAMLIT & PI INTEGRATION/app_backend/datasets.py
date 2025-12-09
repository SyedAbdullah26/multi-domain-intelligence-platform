# app_backend/datasets.py
import pandas as pd
from app_backend.db import connect_database

def load_datasets():
    """Return dataset metadata table as a DataFrame."""
    conn = connect_database()
    df = pd.read_sql("SELECT * FROM datasets_metadata", conn)
    conn.close()
    return df
