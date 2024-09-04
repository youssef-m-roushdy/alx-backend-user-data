#!/usr/bin/env python3
"""
Authentication module for handling user authorization
and authentication in a Flask app.
"""
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """Session-based authentication class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Method that creates a Session ID for a user_id
        """
        if not user_id or type(user_id) != str:
            return None

        session_id = uuid4()
        self.user_id_by_session_id[session_id] = user_id
        return session_id
