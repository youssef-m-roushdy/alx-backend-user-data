#!/usr/bin/env python3
"""
Hash a password
"""
import bcrypt


def _hash_password(password: str):
    """ Hash a password using bcrypt """
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password
