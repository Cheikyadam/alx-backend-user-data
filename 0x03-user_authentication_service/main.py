#!/usr/bin/env python3
"""
Main file
"""
import requests


def register_user(email: str, password: str) -> None:
    """register user"""
    url = "http://localhost:5000/users"
    data = {"email": email, "password": password}
    response = requests.post(url, data)
    res_json = response.json()
    exp = {'email': 'guillaume@holberton.io', 'message': 'user created'}
    assert res_json == exp
    assert response.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """ log in wrong pwd"""
    url = "http://localhost:5000/sessions"
    data = {"email": email, "password": password}
    response = requests.post(url, data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """ log in """
    url = "http://localhost:5000/sessions"
    data = {"email": email, "password": password}
    response = requests.post(url, data)
    assert response.status_code == 200
    res_json = response.json()
    exp = {'email': 'guillaume@holberton.io', 'message': 'logged in'}
    assert res_json == exp
    cookies = response.cookies
    return cookies.get("session_id")


def profile_unlogged() -> None:
    """prof unlog"""
    url = "http://localhost:5000/profile"
    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """profile log"""
    url = "http://localhost:5000/profile"
    cookies = {"session_id": session_id}
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200
    assert {'email': 'guillaume@holberton.io'} == response.json()


def log_out(session_id: str) -> None:
    """log out"""
    url = "http://localhost:5000/sessions"
    cookies = {"session_id": session_id}
    response = requests.delete(url, cookies=cookies)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """rest pwd"""
    url = "http://localhost:5000/reset_password"
    data = {"email": email}
    response = requests.post(url, data)
    assert response.status_code == 200
    res_j = response.json()
    assert res_j["email"] == 'guillaume@holberton.io'
    return res_j["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """upd pwd"""
    url = "http://localhost:5000/reset_password"
    data = {"email": email, "reset_token": reset_token,
            "new_password": new_password}
    response = requests.put(url, data)
    assert response.status_code == 200
    exp = {'email': 'guillaume@holberton.io', 'message': 'Password updated'}
    assert response.json() == exp


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
