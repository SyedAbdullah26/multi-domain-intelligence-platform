import pandas as pd
from app_backend.db import connect_database

# ticket_id TEXT PRIMARY KEY
# date_created TEXT, priority TEXT, status TEXT, description TEXT, assigned_to TEXT, deleted_at TEXT

def load_tickets():
    conn = connect_database()
    df = pd.read_sql(
        "SELECT * FROM it_tickets WHERE deleted_at IS NULL OR deleted_at = ''",
        conn,
    )
    conn.close()
    return df

def load_deleted_tickets():
    conn = connect_database()
    df = pd.read_sql(
        "SELECT * FROM it_tickets WHERE deleted_at IS NOT NULL AND deleted_at <> ''",
        conn,
    )
    conn.close()
    return df

def insert_ticket(ticket_id, date_created, priority, status, description, assigned_to):
    conn = connect_database()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO it_tickets
        (ticket_id, date_created, priority, status, description, assigned_to, deleted_at)
        VALUES (?, ?, ?, ?, ?, ?, NULL)
        """,
        (ticket_id, date_created, priority, status, description, assigned_to),
    )
    conn.commit()
    conn.close()

def update_ticket(pk_col, ticket_id, updates: dict):
    conn = connect_database()
    cur = conn.cursor()
    clause = ", ".join([f"{c} = ?" for c in updates.keys()])
    values = list(updates.values()) + [ticket_id]
    cur.execute(f"UPDATE it_tickets SET {clause} WHERE {pk_col} = ?", values)
    conn.commit()
    conn.close()

def delete_ticket(pk_col, ticket_id):
    conn = connect_database()
    cur = conn.cursor()
    cur.execute(
        f"UPDATE it_tickets SET deleted_at = CURRENT_TIMESTAMP WHERE {pk_col} = ?",
        (ticket_id,),
    )
    conn.commit()
    conn.close()

def restore_ticket(pk_col, ticket_id):
    conn = connect_database()
    cur = conn.cursor()
    cur.execute(
        f"UPDATE it_tickets SET deleted_at = NULL WHERE {pk_col} = ?",
        (ticket_id,),
    )
    conn.commit()
    conn.close()

def purge_ticket(pk_col, ticket_id):
    conn = connect_database()
    cur = conn.cursor()
    cur.execute(f"DELETE FROM it_tickets WHERE {pk_col} = ?", (ticket_id,))
    conn.commit()
    conn.close()
