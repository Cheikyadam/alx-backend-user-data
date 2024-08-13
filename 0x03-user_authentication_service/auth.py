#!/usr/bin/env python3
"""auth module"""
import bcrypt
from db import DB
from typing import TypeVar, Dict


def _hash_password(password: str) -> bytes:
    """hashing password"""
    password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> TypeVar('User'):
        """register user in db"""
        error = False
        try:
            self._db.find_user_by(email=email)
        except Exception as e:
            error = True

        if error is True:
            hashed_pwd = _hash_password(password)
            return self._db.add_user(email, hashed_pwd)
        else:
            raise ValueError(f"User {email} already exist")
