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
    """ Hash a password using bcrypt """
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password


def _generate_uuid() -> str:
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Registers new user
            Args:
                - email: user's email
                - password: user's password
            Return:
                - User instance created
        """
        db = self._db
        try:
            user = db.find_user_by(email=email)
        except NoResultFound:
            user = db.add_user(email, _hash_password(password))
            return user
        else:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """
            Validates user login by checking email and password.
        """
        db = self._db
        try:
            user = db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
            else:
                return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        Creates a session for a user by generating a session ID
        """
        db = self._db
        try:
            user = db.find_user_by(email=email)
            session_id = _generate_uuid()
            db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None
