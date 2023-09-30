import sqlite3
import os

current_directory = os.getcwd()
db_file_path = os.path.join(current_directory, 'database', 'profiles.db')
print(db_file_path)

conn = sqlite3.connect(db_file_path)
cur = conn.cursor()

cur.execute('''
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY,
            user_id TEXT,
            habr_email TEXT,
            habr_password TEXT,
            categories TEXT,
            std_resp TEXT
        )
    ''')
conn.commit()
def add_user(user_id):
    cur.execute("SELECT * FROM profiles WHERE user_id=?", (str(user_id),))
    user = cur.fetchone()
    if not user:
        cur.execute(
            "INSERT INTO profiles (user_id) VALUES (?)",
            (user_id,))
        conn.commit()
def add_email(user_id, email):
    cur.execute("UPDATE profiles SET habr_email = ? WHERE user_id = ?", (email, str(user_id),))
    conn.commit()

def add_password(user_id, password):
    cur.execute("UPDATE profiles SET habr_password = ? WHERE user_id = ?", (password, str(user_id),))
    conn.commit()

def get_email(user_id):
    cur.execute("SELECT habr_email FROM profiles WHERE user_id=?", (str(user_id),))
    email = cur.fetchone()
    return email

def get_password(user_id):
    cur.execute("SELECT habr_password FROM profiles WHERE user_id=?", (str(user_id),))
    password = cur.fetchone()
    return password