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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
