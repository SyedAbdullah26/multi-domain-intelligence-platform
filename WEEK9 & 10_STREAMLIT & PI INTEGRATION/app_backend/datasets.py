import pandas as pd
from app_backend.db import connect_database

# dataset_name TEXT PRIMARY KEY
# source TEXT, record_count INTEGER, last_updated TEXT, description TEXT, deleted_at TEXT

def load_datasets():
    conn = connect_database()
    df = pd.read_sql(
        "SELECT * FROM datasets_metadata WHERE deleted_at IS NULL OR deleted_at = ''",
        conn,
    )
    conn.close()
    return df

def load_deleted_datasets():
    conn = connect_database()
    df = pd.read_sql(
        "SELECT * FROM datasets_metadata WHERE deleted_at IS NOT NULL AND deleted_at <> ''",
        conn,
    )
    conn.close()
    return df

def insert_dataset(dataset_name, source, record_count, last_updated, description):
    conn = connect_database()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO datasets_metadata
        (dataset_name, source, record_count, last_updated, description, deleted_at)
        VALUES (?, ?, ?, ?, ?, NULL)
        """,
        (dataset_name, source, record_count, last_updated, description),
    )
    conn.commit()
    conn.close()

def update_dataset(pk_col, dataset_name, updates: dict):
    conn = connect_database()
    cur = conn.cursor()
    clause = ", ".join([f"{c} = ?" for c in updates.keys()])
    values = list(updates.values()) + [dataset_name]
    cur.execute(f"UPDATE datasets_metadata SET {clause} WHERE {pk_col} = ?", values)
    conn.commit()
    conn.close()

def delete_dataset(pk_col, dataset_name):
    conn = connect_database()
    cur = conn.cursor()
    cur.execute(
        f"UPDATE datasets_metadata SET deleted_at = CURRENT_TIMESTAMP WHERE {pk_col} = ?",
        (dataset_name,),
    )
    conn.commit()
    conn.close()

def restore_dataset(pk_col, dataset_name):
    conn = connect_database()
    cur = conn.cursor()
    cur.execute(
        f"UPDATE datasets_metadata SET deleted_at = NULL WHERE {pk_col} = ?",
        (dataset_name,),
    )
    conn.commit()
    conn.close()

def purge_dataset(pk_col, dataset_name):
    conn = connect_database()
    cur = conn.cursor()
    cur.execute(f"DELETE FROM datasets_metadata WHERE {pk_col} = ?", (dataset_name,))
    conn.commit()
    conn.close()
