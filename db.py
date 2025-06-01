import sqlite3
import hashlib
import os
import csv
import re

DB_NAME = "employwe.db"

def connect_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            role TEXT
        )
    """)
    conn.commit()
    conn.close()

def hash_password(password):
    salt = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt.hex() + ':' + hashed.hex()

def verify_password(password, stored_hash):
    salt, hashed = stored_hash.split(':')
    salt = bytes.fromhex(salt)
    hashed_check = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return hashed == hashed_check.hex()

def username_exists(username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT 1 FROM employees WHERE username = ?", (username,))
    exists = c.fetchone() is not None
    conn.close()
    return exists

def is_valid_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

def add_employee(username, password, email, role):
    if not is_valid_email(email):
        raise Exception("Invalid email format.")

    if username_exists(username):
        raise Exception("Username already exists.")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    hashed_pw = hash_password(password)
    try:
        c.execute("INSERT INTO employees (username, password, email, role) VALUES (?, ?, ?, ?)",
                  (username, hashed_pw, email, role))
        conn.commit()
    finally:
        conn.close()

def get_all_employees():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, username, email, role FROM employees")
    rows = c.fetchall()
    conn.close()
    return rows

def search_employees(keyword):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    query = "SELECT id, username, email, role FROM employees WHERE username LIKE ? OR email LIKE ? OR role LIKE ?"
    keyword = f"%{keyword}%"
    c.execute(query, (keyword, keyword, keyword))
    results = c.fetchall()
    conn.close()
    return results

def update_employee(emp_id, username, email, role):
    if not is_valid_email(email):
        raise Exception("Invalid email format.")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE employees SET username=?, email=?, role=? WHERE id=?",
              (username, email, role, emp_id))
    conn.commit()
    conn.close()

def delete_employee(emp_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM employees WHERE id=?", (emp_id,))
    conn.commit()
    conn.close()

def export_to_csv(filename="employees_export.csv"):
    rows = get_all_employees()
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "Username", "Email", "Role"])
        writer.writerows(rows)
