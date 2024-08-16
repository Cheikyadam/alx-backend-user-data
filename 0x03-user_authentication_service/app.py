#!/usr/bin/env python3
"""flask app"""
from flask import Flask, url_for, redirect, Response, abort, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


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
            AUTH.register_user(email, pwd)
            return jsonify({"email": email, "message": "user created"})
        except ValueError:
            return jsonify({"message": "email already registered"}), 400
    except Exception as e:
        return jsonify({"error": "wrong format"}), 404


@app.route("/sessions", methods=["POST"])
def login() -> Response:
    """login function"""
    try:
        email = request.form.get("email")
        pwd = request.form.get("password")
        if not email or not pwd:
            abort(401)
        if AUTH.valid_login(email, pwd):
            session_id = AUTH.create_session(email)
            out = jsonify({"email": email, "message": "logged in"})
            out.set_cookie("session_id", session_id)
            return out
        else:
            abort(401)
    except Exception as e:
        abort(401)


@app.route("/sessions", methods=["DELETE"])
def logout():
    """logout function"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    else:
        AUTH.destroy_session(user.id)
        return redirect(url_for("index"))


@app.route("/profile", methods=["GET"])
def profile() -> str:
    """get profile"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        return jsonify({}), 403
    else:
        return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token() -> str:
    """get reset pwd token"""
    try:
        email = request.form.get("email")
        session_id = AUTH.create_session(email)
        if session_id is None:
            return jsonify({}), 403
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except Exception:
        return jsonify({}), 403


@app.route("/reset_password", methods=["PUT"])
def update_password() -> str:
    """get reset pwd token"""
    try:
        email = request.form.get("email")
        token = request.form.get("reset_token")
        pwd = request.form.get("new_password")
        AUTH.update_password(token, pwd)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except Exception as e:
        return jsonify({"error": "bad token"}), 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
