#!/usr/bin/env python3
"""Module of Users views."""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """Handles user login via session authentication."""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            resp = jsonify(user.to_json())
            session_name = os.getenv('SESSION_NAME')
            resp.set_cookie(session_name, session_id)
            return resp

    return jsonify({"error": "wrong password"}), 401


@app_views.route('/api/v1/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def delete_session() -> str:
    """
    Deletes the user's session by invoking the destroy_session method.
    If the session is not found or
    cannot be deleted, a 404 error is returned.

    Returns:
        Empty JSON response with a 200 status if the session
        is successfully deleted.
        Otherwise, returns a 404 error if the session could not be destroyed.
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
