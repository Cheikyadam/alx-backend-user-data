#!/usr/bin/env python3
"""flask app"""
from flask import Flask, Response, abort, jsonify, request
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
        return jsonify({"error": "wrong format"}), 404


@app.route("/sessions", methods=["POST"])
def login() -> Response:
    """login function"""
    try:
        email = request.form.get("email")
        pwd = request.form.get("password")
        if not email or not pwd:
            abort(401)
        if auth.valid_login(email, pwd):
            session_id = auth.create_session(email)
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
    user = auth.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    else:
        auth.destroy_session(user.id)
        return redirect(url_for("index"))


@app.route("/profile", methods=["GET"])
def profile() -> str:
    """get profile"""
    session_id = request.cookies.get("session_id")
    user = auth.get_user_from_session_id(session_id)
    if user is None:
        return jsonify({}), 403
    else:
        return jsonify({"email": user.email}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
