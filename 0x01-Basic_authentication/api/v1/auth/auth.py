#!/usr/bin/env python3
"""
    Auth class
"""
from flask import request
from typing import List
from typing import TypeVar


class Auth:
    """auth class def and methodes"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require func"""
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1:] != "/":
            path = path + "/"
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """auth funct"""
        if request is None:
            return None
        if request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """get current user"""
        return None
