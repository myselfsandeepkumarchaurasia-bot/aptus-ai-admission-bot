import sqlite3
from datetime import datetime


DB_NAME = "aptus_leads.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            email TEXT,
            education TEXT,
            interested_course TEXT,
            career_goal TEXT,
            experience TEXT,
            counselling_required TEXT,
            created_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT,
            user_message TEXT,
            bot_response TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_lead(
    name,
    phone,
    email,
    education,
    course,
    career_goal,
    experience,
    counselling
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO leads
        (
            name,
            phone,
            email,
            education,
            interested_course,
            career_goal,
            experience,
            counselling_required,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        phone,
        email,
        education,
        course,
        career_goal,
        experience,
        counselling,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()