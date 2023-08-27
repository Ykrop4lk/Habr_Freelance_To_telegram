import sqlite3
import os

conn = sqlite3.connect("database/tasks.db")
cur = conn.cursor()

cur.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            task_id TEXT,
            title TEXT,
            price TEXT,
            "date" TEXT,
            responce TEXT,
            description TEXT,
            tags TEXT,
            href TEXT
        )
    ''')

conn.commit()


def add_task(task_id: str, title: str, price: str,
             date: str, responce: str, description: str,
             tags, href: str):
    cur.execute("SELECT * FROM tasks WHERE task_id=?", (task_id,))
    task = cur.fetchone()
    if not task:
        cur.execute(
            "INSERT INTO tasks ("
            "task_id, title, price,"
            "date, responce, description,"
            "tags, href) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (task_id, title, price, date, responce, description, tags, href))
        conn.commit()

def get_task_id(id):
    cur.execute("SELECT task_id FROM tasks WHERE id=?", (id,))
    task = cur.fetchone()
    return task[0]

def is_link_in_db(link):
    cur.execute("SELECT * FROM tasks WHERE href=?", (link,))
    task = cur.fetchone()
    if not task:
        return False
    return True

def get_url_by_task_id(task_id):
    cur.execute("SELECT href FROM tasks WHERE task_id=?", (task_id,))
    task = cur.fetchone()
    return task[0]

def get_title_by_task_id(task_id):
    cur.execute("SELECT title FROM tasks WHERE task_id=?", (task_id,))
    task = cur.fetchone()
    return task[0]

def get_price_by_task_id(task_id):
    cur.execute("SELECT price FROM tasks WHERE task_id=?", (task_id,))
    task = cur.fetchone()
    return task[0]

def get_date_by_task_id(task_id):
    cur.execute("SELECT date FROM tasks WHERE task_id=?", (task_id,))
    task = cur.fetchone()
    return task[0]

def get_responce_by_task_id(task_id):
    cur.execute("SELECT responce FROM tasks WHERE task_id=?", (task_id,))
    task = cur.fetchone()
    return task[0]

def get_desc_by_task_id(task_id):
    cur.execute("SELECT description FROM tasks WHERE task_id=?", (task_id,))
    task = cur.fetchone()
    return task[0]

def get_tags_by_task_id(task_id):
    cur.execute("SELECT tags FROM tasks WHERE task_id=?", (task_id,))
    task = cur.fetchone()
    return task[0]