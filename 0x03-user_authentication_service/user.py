#!/usr/bin/env python3
"""
This module defines the User model for SQLAlchemy ORM.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    User model that represents the 'users' table in the database.

    Attributes:
        id (int): Primary key for the user.
        email (str): User's email, must be unique and not nullable.
        hashed_password (str): Hashed version of the user's password.
        session_id (str): ID of the current session for the user.
        reset_token (str): Token used for password reset.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))
