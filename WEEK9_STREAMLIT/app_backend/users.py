import hashlib
from app_backend.db import connect_database

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password, role="analyst"):
    conn = connect_database()
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                    (username, hash_password(password), role))
        conn.commit()
        return True, "User registered successfully"
    except:
        return False, "Username already exists"
    finally:
        conn.close()

def login_user(username, password):
    conn = connect_database()
    cur = conn.cursor()

    cur.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    row = cur.fetchone()

    conn.close()

    if row is None:
        return False, "User not found"

    if row[0] == hash_password(password):
        return True, "Login successful"
    return False, "Invalid password"
