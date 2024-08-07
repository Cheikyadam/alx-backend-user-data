#!/usr/bin/env python3
"""basic auth class"""
from api.v1.auth.auth import Auth
import base64


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
