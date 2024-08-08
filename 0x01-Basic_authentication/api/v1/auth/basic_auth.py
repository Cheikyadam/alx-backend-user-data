#!/usr/bin/env python3
"""basic auth class"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """basci auth class"""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """extrating base 64"""
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if authorization_header.startswith("Basic ") is False:
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """decode base 64 header"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            value = base64.b64decode(
                    base64_authorization_header, validate=True)
            return value.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """extract user cred"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) is not str:
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        cred = decoded_base64_authorization_header.split(':')
        if len(cred) == 2:
            return (cred[0], cred[1])

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """get connected user"""
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        res = (User.search({'email': user_email}))
        if len(res) == 0:
            return None
        if res[0].is_valid_password(user_pwd):
            return res[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current user"""
        auth_head = self.authorization_header(request)
        base64value = self.extract_base64_authorization_header(auth_head)
        decoded_value = self.decode_base64_authorization_header(base64value)
        user_cred = self.extract_user_credentials(decoded_value)
        return self.user_object_from_credentials(user_cred[0], user_cred[1])
