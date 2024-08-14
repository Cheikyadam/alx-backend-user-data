#!/usr/bin/env python3
"""flask app"""
from flask import Flask, abort, jsonify, request
from auth import Auth

app = Flask(__name__)
auth = Auth()


@app.route("/")
def index() -> str:
    """task 6"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users() -> str:
    """register user"""
    try:
        email = request.form.get("email")
        pwd = request.form.get("password")
        try:
            auth.register_user(email, pwd)
            return jsonify({"email": email, "message": "user created"})
        except ValueError:
            return jsonify({"message": "email already registered"}), 400
    except Exception as e:
        print(f"error: {e}")
        return jsonify({"error": "wrong format"}), 404


@app.route("/sessions", methods=["POST"])
def login() -> str:
    """login func"""
    try:
        email = request.form.get("email")
        pwd = request.form.get("password")
        if auth.valid_login(email, pwd):
            session_id = auth.create_session(email)
            out = jsonify({"email": email, "message": "logged in"})
            out.set_cookie("session_id", session_id)
            return out
        else:
            abort(401)
    except Exception as e:
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
