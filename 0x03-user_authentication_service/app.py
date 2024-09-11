#!/usr/bin/env python3
"""
Flask app that returns a welcome message.
"""

from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def bienvenue():
    """
    Returns a welcome message in JSON format.
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """
    Register a new user with email and password.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        AUTH.register_user(email, password)
        return jsonify({"message": "User created", "email": email}), 200
    except Exception:
        return jsonify({"message": "Email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
