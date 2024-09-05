#!/usr/bin/env python3
"""
Authentication module for handling user authorization
and authentication in a Flask app.
"""
from api.v1.auth.session_auth import SessionAuth
from uuid import uuid4
from models.user import User
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """SessionExpAuth authentication class with session expiration."""

    def __init__(self):
        """Initialize the session duration from the environment variable."""
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION'))
        except (TypeError, ValueError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a session and store the creation time."""
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve the user ID for a session, considering expiration."""
        if not session_id:
            return None
        session_dictionary = self.user_id_by_session_id.get(session_id)
        if not session_dictionary:
            return None

        if 'created_at' not in session_dictionary:
            return None

        if self.session_duration <= 0:
            return session_dictionary.get("user_id")

        created_at = session_dictionary.get("created_at")
        allowed_window = created_at + timedelta(seconds=self.session_duration)

        # Expired session: Clean it up and return None
        if allowed_window < datetime.now():
            del self.user_id_by_session_id[session_id]  # Optional cleanup
            return None

        return session_dictionary.get("user_id")
