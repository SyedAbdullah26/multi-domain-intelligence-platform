import sqlite3
from pathlib import Path

DB_PATH = Path(r"C:\Users\syeda\OneDrive - Middlesex University\Cybersecurity\CST1510\modular multi-domain intelligence Week 8-10\WEEK8_BACKEND\DATA\intelligence_platform.db")

def add_deleted_at_column(table_name: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info({table_name})")
    cols = [row[1] for row in cur.fetchall()]
    if "deleted_at" not in cols:
        print(f"➕ Adding deleted_at to {table_name}")
        cur.execute(f"ALTER TABLE {table_name} ADD COLUMN deleted_at TEXT")
        conn.commit()
    else:
        print(f"✔ {table_name} already has deleted_at")
    conn.close()

if __name__ == "__main__":
    for t in ["cyber_incidents", "it_tickets", "datasets_metadata"]:
        add_deleted_at_column(t)
    print("✅ Migration complete.")
