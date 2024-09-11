#!/usr/bin/env python3
"""
Flask app that returns a welcome message.
"""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def bienvenue():
    """
    Returns a welcome message in JSON format.
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
