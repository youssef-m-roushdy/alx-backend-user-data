#!/usr/bin/env python3
"""
Authentication module for handling user authorization
and authentication in a Flask app.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    A class to manage authentication in a web application.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required for a given path.
        """
        if path is None:
            return True
        if not excluded_paths:
            return True

        if path[-1] != '/':
            path += '/'
        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the request.
        """
        if request is None:
            return None

        if request.headers.get('Authorization') is None:
            return None
        else:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user from the request.
        """
        return None
