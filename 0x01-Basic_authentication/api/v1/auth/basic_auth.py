#!/usr/bin/env python3
"""basic auth class"""
from api.v1.auth.auth import Auth


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
