#!/usr/bin/env python3
"""
Authentication module for handling user authorization
and authentication in a Flask app.
"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    A class for basic authentication that inherits from Auth.
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Extracts the Base64 encoded authorization token
        from the Authorization header.
        """
        if not authorization_header:
            return None
        if not isinstance(authorization_header, str):
            return None

        # Split the authorization header into its components
        data = authorization_header.split(" ")

        # Check if the scheme is "Basic"
        if data[0] != "Basic":
            return None

        # Return the Base64 encoded token
        return data[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """
        Method returns the decoded value of a Base64 string.
        """
        if not base64_authorization_header:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            # Decode the base64 part
            decoded_bytes = base64.b64decode(base64_authorization_header)
            # Convert bytes to UTF-8 string
            return decoded_bytes.decode('utf-8')
        except (IndexError, base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """
        Method returns the user email
        and password from the Base64 decoded value.
        """
        if not decoded_base64_authorization_header:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        return (decoded_base64_authorization_header.split(":")[0],
                decoded_base64_authorization_header.split(":")[1])

    def user_object_from_credentials(self, user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """
        Method returns the User instance based
        on his email and password.
        """
        if type(user_email) is not str:
            return None
        if type(user_pwd) is not str:
            return None
        users = User.search({'email': user_email})

        # If no users are found with the given email, return None
        if not users:
            return None

        user = users[0]

        # Check if the provided password is valid for the found user
        if not user.is_valid_password(user_pwd):
            return None

        return user
