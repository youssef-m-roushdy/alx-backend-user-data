#!/usr/bin/env python3
"""
Manage the API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Manage auth path
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Manage auth authorization header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Manage current user auth
        """
        return None
