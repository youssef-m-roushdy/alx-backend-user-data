#!/usr/bin/env python3
"""
Flask app that returns a welcome message.
"""

from flask import Flask, jsonify, request, abort, make_response, redirect
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
    """ New user signup endpoint
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
    Validates user login using email and password with creating a session.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(401)
    else:
        session_id = AUTH.create_session(email)
        response = make_response(
            jsonify({"email": email, "message": "logged in"}))
        response.set_cookie(session_id)
        return response


@app.route('/sessions/<session_id>', methods=['DELETE'])
def logout(session_id: str):
    """
    Deletes a user session based on the provided session ID.
    """
    session_id = request.cookies.get('session_id')
    
    if not session_id:
        abort(403)  # Forbidden if no session ID is present

    try:
        user = Auth.get_user_from_session_id(session_id)
        if user:
            Auth.destroy_session(session_id)
            response = make_response(redirect('/'))
            response.set_cookie('session_id', '', expires=0)  # Clear the session cookie
            return response
        else:
            abort(403)  # Forbidden if the session ID does not match any user
    except Exception as e:
        # Optionally log the exception
        print(f"Error during logout: {e}")
        abort(403)  # Forbidden if an error occurs


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
