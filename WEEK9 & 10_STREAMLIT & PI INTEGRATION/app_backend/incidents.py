import pandas as pd
from app_backend.db import connect_database

# ========== READ (active only) ==========
def load_incidents():
    conn = connect_database()
    df = pd.read_sql(
        "SELECT * FROM cyber_incidents WHERE deleted_at IS NULL OR deleted_at = ''",
        conn,
    )
    conn.close()
    return df

# ========== READ (deleted only - recycle bin) ==========
def load_deleted_incidents():
    conn = connect_database()
    df = pd.read_sql(
        "SELECT * FROM cyber_incidents WHERE deleted_at IS NOT NULL AND deleted_at <> ''",
        conn,
    )
    conn.close()
    return df

# ========== CREATE ==========
def insert_incident(date_reported, incident_type, severity, status, description, reported_by):
    conn = connect_database()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO cyber_incidents
        (date_reported, incident_type, severity, status, description, reported_by, deleted_at)
        VALUES (?, ?, ?, ?, ?, ?, NULL)
        """,
        (date_reported, incident_type, severity, status, description, reported_by),
    )
    conn.commit()
    conn.close()

# ========== UPDATE ==========
def update_incident(pk_col, incident_id, updates: dict):
    conn = connect_database()
    cur = conn.cursor()
    clause = ", ".join([f"{col} = ?" for col in updates.keys()])
    values = list(updates.values()) + [incident_id]
    cur.execute(f"UPDATE cyber_incidents SET {clause} WHERE {pk_col} = ?", values)
    conn.commit()
    conn.close()

# ========== SOFT DELETE (move to recycle bin) ==========
def delete_incident(pk_col, incident_id):
    conn = connect_database()
    cur = conn.cursor()
    cur.execute(
        f"UPDATE cyber_incidents SET deleted_at = CURRENT_TIMESTAMP WHERE {pk_col} = ?",
        (incident_id,),
    )
    conn.commit()
    conn.close()

# ========== RESTORE FROM BIN ==========
def restore_incident(pk_col, incident_id):
    conn = connect_database()
    cur = conn.cursor()
    cur.execute(
        f"UPDATE cyber_incidents SET deleted_at = NULL WHERE {pk_col} = ?",
        (incident_id,),
    )
    conn.commit()
    conn.close()

# ========== HARD DELETE (permanent) ==========
def purge_incident(pk_col, incident_id):
    conn = connect_database()
    cur = conn.cursor()
    cur.execute(f"DELETE FROM cyber_incidents WHERE {pk_col} = ?", (incident_id,))
    conn.commit()
    conn.close()
