# app_backend/incidents.py
import pandas as pd
from app_backend.db import connect_database

def load_incidents():
    """Return cyber_incidents table as a DataFrame."""
    conn = connect_database()
    df = pd.read_sql("SELECT * FROM cyber_incidents", conn)
    conn.close()
    return df

def insert_incident(date_reported, incident_type, severity, status, description, reported_by):
    """Insert a new cyber incident into the database."""
    conn = connect_database()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO cyber_incidents
        (date_reported, incident_type, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (date_reported, incident_type, severity, status, description, reported_by),
    )
    conn.commit()
    incident_id = cur.lastrowid
    conn.close()
    return incident_id
