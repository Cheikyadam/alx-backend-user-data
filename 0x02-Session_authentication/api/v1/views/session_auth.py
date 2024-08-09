#!/usr/bin/env python3
"""views for session"""
from flask import jsonify, request
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session():
    """login handler"""
    email = request.form.get("email")
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    user_pass = request.form.get("password")
    if user_pass is None or user_pass == "":
        return jsonify({"error": "password missing"}), 400
    res = (User.search({'email': email}))
    if len(res) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    if res[0].is_valid_password(user_pass) is False:
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(res[0].id)
    user_dict = res[0].to_json()
    out = jsonify(user_dict)
    out.set_cookie(getenv("SESSION_NAME"), session_id)
    return out
