import pandas as pd
from app_backend.db import connect_database

def get_all_incidents():
    conn = connect_database()
    df = pd.read_sql("SELECT * FROM cyber_incidents", conn)
    conn.close()
    return df

def insert_incident(date, inc_type, severity, status, desc, reporter):
    conn = connect_database()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO cyber_incidents (date_reported, incident_type, severity, status, description, reported_by) VALUES (?, ?, ?, ?, ?, ?)",
        (date, inc_type, severity, status, desc, reporter)
    )

    conn.commit()
    incident_id = cur.lastrowid
    conn.close()

    return incident_id
