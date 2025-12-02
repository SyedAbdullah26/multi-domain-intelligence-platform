# app_backend/db.py
import sqlite3
from pathlib import Path

DB_PATH = Path(r"C:\Users\syeda\OneDrive - Middlesex University\Cybersecurity\CST1510\modular multi-domain intelligence Week 8-10\WEEK8_BACKEND\DATA\intelligence_platform.db")

def connect_database():
    return sqlite3.connect(DB_PATH)
