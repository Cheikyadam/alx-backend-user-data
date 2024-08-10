#!/usr/bin/env python3
"""expiration - session"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """session with exp date"""

    def __init__(self):
        """init meth"""
        duration = 0
        try:
            duration = int(getenv("SESSION_DURATION", "0"))
        except Exception:
            pass
        self.session_duration = duration

    def create_session(self, user_id=None):
        """create session"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        sess_dic = {"user_id": user_id, "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = sess_dic
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """user_id for session"""
        if session_id is None:
            return None
        sess_dict = self.user_id_by_session_id.get(session_id)
        if sess_dict is None:
            return None
        if self.session_duration <= 0:
            return sess_dict.get("user_id")
        created_at = sess_dict.get("created_at")
        if created_at is None:
            return None
        t1 = created_at + timedelta(seconds=self.session_duration)
        t2 = datetime.now()
        if t1 - t2 <= timedelta(0):
            return None
        return sess_dict.get("user_id")
