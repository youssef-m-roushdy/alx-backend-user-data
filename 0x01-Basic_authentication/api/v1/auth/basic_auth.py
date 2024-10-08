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

        last_colon_index = decoded_base64_authorization_header.find(':')

        user_email = decoded_base64_authorization_header[:last_colon_index]
        user_pass = decoded_base64_authorization_header[last_colon_index+1:]
        return (user_email,
                user_pass)

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
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        if not users or not users[0].is_valid_password(user_pwd):
            return None

        return users[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the user from a request.
        """
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)
