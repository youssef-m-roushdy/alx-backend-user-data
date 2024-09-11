#!/usr/bin/env python3
"""
Hash a password
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt."""
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password


def _generate_uuid() -> str:
    """Generate a UUID string."""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user.

        Args:
            email (str): User's email.
            password (str): User's password.

        Returns:
            User: User instance created.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = self._db.add_user(email, _hash_password(password))
            return user
        else:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Validates user login by checking email and password.

        Args:
            email (str): User's email.
            password (str): User's password.

        Returns:
            bool: True if valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
            return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Creates a session for a user by generating a session ID.

        Args:
            email (str): User's email.

        Returns:
            str: Generated session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Retrieves a user based on their session ID.

        Args:
            session_id (str): User's session ID.

        Returns:
            User: User instance if session ID is valid, None otherwise.
        """
        if not session_id:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys a user's session.

        Args:
            user_id (int): User's ID.
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except Exception:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """Generates a reset password token for 
        the user with the specified email.

        Args:
            email (str): User's email.

        Returns:
            str: Generated reset password token.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        reset_token = _generate_uuid()
        self._db.update_user(user.id, session_id=reset_token)
        return reset_token
