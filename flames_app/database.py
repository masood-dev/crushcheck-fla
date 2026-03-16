"""Database module for Secret Admirer Notes (SQLite)."""

import os
import secrets
import sqlite3
from datetime import datetime, timedelta

from werkzeug.security import check_password_hash, generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'secret_notes.db')


def current_timestamp():
    return datetime.now().isoformat(sep=' ', timespec='seconds')


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS secret_notes (
            id TEXT PRIMARY KEY,
            message TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            sender_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            view_count INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()


def create_note(message, password, sender_name=None, expire_days=30):
    conn = get_db_connection()
    note_id = secrets.token_urlsafe(8)
    password_hash = generate_password_hash(password)
    expires_at = (datetime.now() + timedelta(days=expire_days)).isoformat(sep=' ', timespec='seconds')
    
    conn.execute('''
        INSERT INTO secret_notes (id, message, password_hash, sender_name, expires_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (note_id, message, password_hash, sender_name, expires_at))
    
    conn.commit()
    conn.close()
    return note_id


def get_note(note_id):
    conn = get_db_connection()
    note = conn.execute(
        '''
        SELECT id, message, sender_name, created_at, view_count
        FROM secret_notes
        WHERE id = ? AND (expires_at IS NULL OR expires_at >= ?)
        ''',
        (note_id, current_timestamp())
    ).fetchone()
    conn.close()
    return note


def verify_password(note_id, password):
    conn = get_db_connection()
    note = conn.execute(
        '''
        SELECT password_hash
        FROM secret_notes
        WHERE id = ? AND (expires_at IS NULL OR expires_at >= ?)
        ''',
        (note_id, current_timestamp())
    ).fetchone()
    
    if note and check_password_hash(note['password_hash'], password):
        # Increment view count
        conn.execute(
            'UPDATE secret_notes SET view_count = view_count + 1 WHERE id = ?',
            (note_id,)
        )
        conn.commit()
        conn.close()
        return True
    
    conn.close()
    return False


def cleanup_expired_notes():
    conn = get_db_connection()
    conn.execute('DELETE FROM secret_notes WHERE expires_at < ?', (current_timestamp(),))
    conn.commit()
    conn.close()
