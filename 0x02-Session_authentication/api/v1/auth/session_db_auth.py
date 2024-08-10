#!/usr/bin/env python3
"""expiration - session - db"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """session db"""

    def create_session(self, user_id=None):
        """create session"""
        session_id = super().create_session(user_id)
        if session_id is not None:
            sess_inf = {"user_id": user_id, "session_id": session_id}
            user_sess = UserSession(**sess_inf)
            user_sess.save()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """user_id_ session"""
        if session_id is not None:
            try:

                res = UserSession.search({"session_id": session_id})
                if len(res) != 0:
                    t1 = res[0].created_at + \
                        timedelta(seconds=self.session_duration)
                    t2 = datetime.now()
                    if t1 - t2 <= timedelta(0):
                        res[0].remove()
                        return None
                    return res[0].user_id
            except Exception as e:
                return None
            return None

    def destroy_session(self, request=None):
        """destroy session"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is not None:
            try:
                res = UserSession.search({"session_id": session_id})
                res[0].remove()
                return True
            except Exception:
                return False
