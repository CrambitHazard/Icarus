"""
memory_manager.py

Simple memory manager for persistent conversation context without LangChain dependency.
"""
import sqlite3
import datetime, json
from typing import Optional, List, Dict

class MemoryManager:
    """Manages conversation memory using SQLite only."""
    def __init__(self, db_path: str = 'data/memory.sqlite'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY,
            session_id TEXT UNIQUE,
            created_at TIMESTAMP,
            last_activity TIMESTAMP,
            context_summary TEXT,
            session_name TEXT
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY,
            session_id TEXT,
            role TEXT,
            content TEXT,
            timestamp TIMESTAMP,
            metadata TEXT
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS tool_executions (
            id INTEGER PRIMARY KEY,
            session_id TEXT,
            tool_name TEXT,
            parameters TEXT,
            result TEXT,
            timestamp TIMESTAMP,
            success BOOLEAN
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS context_embeddings (
            id INTEGER PRIMARY KEY,
            session_id TEXT,
            content_hash TEXT,
            embedding BLOB,
            timestamp TIMESTAMP
        )''')
        conn.commit()
        conn.close()

    def store_message(self, session_id: str, role: str, content: str, metadata: Optional[dict] = None) -> None:
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''INSERT INTO messages (session_id, role, content, timestamp, metadata)
                     VALUES (?, ?, ?, ?, ?)''',
                  (session_id, role, content, datetime.datetime.now().isoformat(), json.dumps(metadata) if metadata else None))
        c.execute('''UPDATE sessions SET last_activity = ? WHERE session_id = ?''', (datetime.datetime.now().isoformat(), session_id))
        conn.commit()
        conn.close()

    def get_history(self, session_id: str) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''SELECT role, content, timestamp, metadata FROM messages WHERE session_id = ? ORDER BY timestamp ASC''', (session_id,))
        rows = c.fetchall()
        conn.close()
        return [{'role': r, 'content': c, 'timestamp': t, 'metadata': m} for r, c, t, m in rows]

    def create_session(self, session_id: str, session_name: Optional[str] = None) -> None:
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''INSERT OR IGNORE INTO sessions (session_id, created_at, last_activity, session_name) VALUES (?, ?, ?, ?)''',
                  (session_id, datetime.datetime.now().isoformat(), datetime.datetime.now().isoformat(), session_name))
        conn.commit()
        conn.close()

    def set_session_name(self, session_id: str, session_name: str) -> None:
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''UPDATE sessions SET session_name = ? WHERE session_id = ?''', (session_name, session_id))
        conn.commit()
        conn.close()

    def summarize_session(self, session_id: str) -> str:
        """Summarize a long conversation for context window management."""
        history = self.get_history(session_id)
        # Simple summary: join last 10 messages
        summary = '\n'.join([f"{m['role']}: {m['content']}" for m in history[-10:]])
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''UPDATE sessions SET context_summary = ? WHERE session_id = ?''', (summary, session_id))
        conn.commit()
        conn.close()
        return summary

    def get_context_window(self, session_id: str, max_messages: int = 10) -> str:
        """Get recent conversation context for LLM input."""
        history = self.get_history(session_id)
        recent_messages = history[-max_messages:]
        return '\n'.join([f"{m['role']}: {m['content']}" for m in recent_messages])

    def clear_session(self, session_id: str) -> None:
        """Clear all messages for a session."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''DELETE FROM messages WHERE session_id = ?''', (session_id,))
        conn.commit()
        conn.close()

    def get_session_info(self, session_id: str) -> Optional[Dict]:
        """Get session information."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''SELECT session_id, created_at, last_activity, session_name FROM sessions WHERE session_id = ?''', (session_id,))
        row = c.fetchone()
        conn.close()
        if row:
            return {
                'session_id': row[0],
                'created_at': row[1],
                'last_activity': row[2],
                'session_name': row[3]
            }
        return None 