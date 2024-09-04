#!/usr/bin/env python3
"""
Authentication module for handling user authorization
and authentication in a Flask app.
"""
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """Session-based authentication class"""
    pass
