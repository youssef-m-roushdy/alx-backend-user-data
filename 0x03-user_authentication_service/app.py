#!/usr/bin/env python3
"""
Flask app that returns a welcome message.
"""

from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def home():
    """
    Returns a welcome message in JSON format.
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """
    New user signup endpoint.

    Form fields:
        - email
        - password
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """
    Validates user login using email and password, and creates a session.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = make_response(
        jsonify({"email": email, "message": "logged in"})
    )
    response.set_cookie('session_id', session_id, httponly=True, secure=True)
    return response


@app.route('/sessions', methods=['DELETE'])
def logout():
    """
    Logs out a user by destroying their session and
    redirecting them to the home page.
    """
    session_id = request.cookies.get("session_id")

    if not session_id:
        abort(403)

    try:
        user = AUTH.get_user_from_session_id(session_id)
        if not user:
            abort(403)

        AUTH.destroy_session(session_id)
    except Exception:
        abort(403)

    response = make_response(redirect('/'))
    response.delete_cookie('session_id')
    return response


@app.route('/profile')
def profile():
    """
    Returns the email of the currently logged-in user.
    """
    session_id = request.cookies.get("session_id")

    if not session_id:
        abort(403)

    try:
        user = AUTH.get_user_from_session_id(session_id)
        if not user:
            abort(403)
        return jsonify({"email": user.email})
    except Exception:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """
    Method to reset password_token

    Returns:
        - email and the reset_token
        - Unauthorized
    """
    email = request.form.get('email')
    try:
        token_reset = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token_reset})
    except Exception:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def update_password():
    """
    Updates the user's password.
    Returns:
        - JSON response .
        - 403 status code.
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        token_reset = AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
