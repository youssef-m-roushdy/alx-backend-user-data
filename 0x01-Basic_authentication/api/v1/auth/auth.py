#!/usr/bin/env python3
"""
Authentication module for handling user authorization
and authentication in a Flask app.
"""
from flask import request
from typing import List, TypeVar
import re


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

        for excluded_path in excluded_paths:
            pattern = re.sub(r'\*$', '.*', excluded_path)

            # Add optional trailing slash to the pattern
            if excluded_path[-1] != '/':
                pattern += '/?'

            # Check if the path matches the regex pattern
            if re.match(pattern, path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the request.
        """
        if not request:
            return None

        if not request.headers.get('Authorization'):
            return None
        else:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user from the request.
        """
        return None
