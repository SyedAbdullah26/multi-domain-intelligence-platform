# app_backend/users.py
import hashlib
from app_backend.db import connect_database

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def register_user(username: str, password: str, role: str = "analyst"):
    """Register a new user with role (default: analyst)."""
    conn = connect_database()
    cur = conn.cursor()
    try:
        cur.execute("SELECT username FROM users WHERE username = ?", (username,))
        if cur.fetchone() is not None:
            return False, "Username already exists"

        cur.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, hash_password(password), role)
        )
        conn.commit()
        return True, "User registered successfully"
    except Exception as e:
        return False, f"Error during registration: {e}"
    finally:
        conn.close()

def login_user(username: str, password: str):
    """
    Return (success: bool, message: str, role: str|None)
    """
    conn = connect_database()
    cur = conn.cursor()
    try:
        cur.execute("SELECT password_hash, role FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        if row is None:
            return False, "User not found", None

        stored_hash, role = row
        if stored_hash == hash_password(password):
            return True, "Login successful", role
        return False, "Invalid password", None
    finally:
        conn.close()
