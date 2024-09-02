#!/usr/bin/env python3
"""
Authentication module for handling user authorization
and authentication in a Flask app.
"""
from api.v1.auth.auth import Auth


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
