# app_backend/tickets.py
import pandas as pd
from app_backend.db import connect_database

def load_tickets():
    """Return IT tickets table as a DataFrame."""
    conn = connect_database()
    df = pd.read_sql("SELECT * FROM it_tickets", conn)
    conn.close()
    return df
