import sqlite3
from pathlib import Path

# 👉 FULL, EXACT PATH to your DB (copy-paste this)
DB_PATH = Path(r"C:\Users\syeda\OneDrive - Middlesex University\Cybersecurity\CST1510\modular multi-domain intelligence Week 8-10\WEEK8_BACKEND\DATA\intelligence_platform.db")

# --- DO NOT CHANGE BELOW ---
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

print("\n📌 TABLE STRUCTURES (PRAGMA)")
print("-----------------------------------")

tables = ["cyber_incidents", "it_tickets", "datasets_metadata", "users"]

for table in tables:
    print(f"\n🔽 {table}:")
    try:
        cur.execute(f"PRAGMA table_info({table})")
        for row in cur.fetchall():
            print(row)
    except:
        print(f"⚠️ Table not found: {table}")

conn.close()
