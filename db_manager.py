# db_manager.py
import os
import psycopg2
from psycopg2 import sql

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('PGHOST'),
        database=os.getenv('PGDATABASE'),
        user=os.getenv('PGUSER'),
        password=os.getenv('PGPASSWORD'),
        port=os.getenv('PGPORT')
    )

def init_db():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql.SQL('''
            CREATE TABLE IF NOT EXISTS users (
                id BIGINT PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                username TEXT,
                chat_id BIGINT,
                last_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                mood_score INTEGER DEFAULT 0
            )
        '''))
        conn.commit()
    except Exception as e:
        print(f"Error initializing DB: {e}")
    finally:
        if conn:
            conn.close()

def add_user(user_id: int, first_name: str, last_name: str = None, username: str = None, chat_id: int = None):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql.SQL("INSERT INTO users (id, first_name, last_name, username, chat_id) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING"),
                       (user_id, first_name, last_name, username, chat_id))
        conn.commit()
    except Exception as e:
        print(f"Error adding user: {e}")
    finally:
        if conn:
            conn.close()

def get_user_data(user_id: int) -> dict:
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql.SQL("SELECT * FROM users WHERE id = %s"), (user_id,))
        row = cursor.fetchone()
        if row:
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, row))
        return None
    except Exception as e:
        print(f"Error getting user data: {e}")
        return None
    finally:
        if conn:
            conn.close()

def update_user_data(user_id: int, **kwargs):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        set_clause = sql.SQL(", ").join(
            sql.SQL("{} = %s").format(sql.Identifier(key)) for key in kwargs.keys()
        )
        values = list(kwargs.values())
        values.append(user_id)
        cursor.execute(sql.SQL(f"UPDATE users SET {set_clause} WHERE id = %s"), tuple(values))
        conn.commit()
    except Exception as e:
        print(f"Error updating user data: {e}")
    finally:
        if conn:
            conn.close()
