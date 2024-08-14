#!/usr/bin/env python3
"""flask app"""
from flask import Flask, jsonify
app = Flask(__name__)


@app.route("/")
def index():
    """task 6"""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
