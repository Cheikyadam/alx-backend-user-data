#!/usr/bin/env python3
"""auth module"""
import bcrypt
from db import DB
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    """hashing password"""
    password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt)


def _generate_uuid() -> str:
    """uuid genereation"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
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

    def valid_login(self, email: str, password: str) -> bool:
        """valid login"""
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode("utf-8"), user.hashed_password):
                return True
            else:
                return False
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """session creation"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user.session_id = session_id
            my_dict = {"session_id": session_id}
            self._db.update_user(user.id, **my_dict)
            return session_id
        except Exception:
            pass

    def get_user_from_session_id(self, session_id: str) -> User:
        """get user from session"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception as e:
            return None

    def destroy_session(self, user_id: int) -> None:
        """destroy session"""
        my_dict = {"session_id": None}
        self._db.update_user(user_id, **my_dict)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """get reset pwd token"""
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            user.reset_token = token
            my_dict = {"reset_token": token}
            self._db.update_user(user.id, **my_dict)
            return token
        except Exception:
            pass

        raise ValueError()

    def update_password(self, reset_token: str, password: str) -> None:
        """update pwd"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            my_dict1 = {"reset_token": None}
            my_dict2 = {"hashed_password": _hash_password(password)}
            self._db.update_user(user.id, **my_dict1)
            self._db.update_user(user.id, **my_dict2)
            return None
        except Exception as e:
            pass

        raise ValueError("Not found")
