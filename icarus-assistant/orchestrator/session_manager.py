"""
session_manager.py

SessionManager: Manage conversation sessions, timeouts, and cleanup.
"""
from typing import Dict, List, Optional
import time

class SessionManager:
    """Manage conversation sessions, timeouts, and cleanup."""
    def __init__(self, memory_manager):
        self.memory = memory_manager
        self.active_sessions = {}
        self.session_timeout = 300  # 5 minutes

    def create_session(self, session_id: str, session_name: Optional[str] = None) -> None:
        """Create new conversation session.

        Args:
            session_id (str): Unique session identifier.
            session_name (Optional[str]): Optional session name.
        """
        self.active_sessions[session_id] = {
            'session_id': session_id,
            'session_name': session_name or f"Session-{session_id[:8]}",
            'created_at': time.time(),
            'last_activity': time.time(),
        }

    def get_active_session(self, session_id: str) -> Optional[Dict]:
        """Get active session information.

        Args:
            session_id (str): Session identifier.

        Returns:
            Optional[Dict]: Session info if active, else None.
        """
        return self.active_sessions.get(session_id)

    def update_session_activity(self, session_id: str) -> None:
        """Update session last activity timestamp.

        Args:
            session_id (str): Session identifier.
        """
        if session_id in self.active_sessions:
            self.active_sessions[session_id]['last_activity'] = time.time()

    def cleanup_expired_sessions(self) -> None:
        """Clean up sessions that have timed out."""
        now = time.time()
        expired = [sid for sid, sess in self.active_sessions.items()
                   if now - sess['last_activity'] > self.session_timeout]
        for sid in expired:
            del self.active_sessions[sid]

    def list_sessions(self) -> List[Dict]:
        """List all sessions with metadata.

        Returns:
            List[Dict]: List of session metadata dicts.
        """
        return list(self.active_sessions.values()) 