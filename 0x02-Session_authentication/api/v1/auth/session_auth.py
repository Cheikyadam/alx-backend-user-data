#!/usr/bin/env python3
"""session auth"""
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """
        session auth class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creation session"""
        if user_id is None or type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """get user id by session id"""
        if session_id is None or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """get current user"""
        if request is None:
            return None
        cookie_value = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie_value)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """destroy session"""
        if request is None:
            return False
        cookie_value = self.session_cookie(request)
        if cookie_value is None:
            return False
        user_id = self.user_id_for_session_id(cookie_value)
        if user_id is None:
            return False
        del self.user_id_by_session_id[cookie_value]
        return True
