#!/usr/bin/env python3
"""
Authentication module for handling user authorization
and authentication in a Flask app.
"""
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """Session-based authentication class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Method that creates a Session ID for a user_id
        """
        if not user_id or type(user_id) != str:
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Method that returns a User ID based on a Session ID
        """
        if not session_id or not isinstance(session_id, str):
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        print(user_id)
        return user_id

    def current_user(self, request=None):
        """
        Overload method that returns a User instance based on a cookie value
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if user_id:
            return User.get(user_id)
        return None

    def destroy_session(self, request=None):
        """
        Deletes the session associated with the provided request.
        """
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_by_session_id.get(session_id)
        if not user_id:
            return False
        del self.user_id_by_session_id[session_id]
        return True
