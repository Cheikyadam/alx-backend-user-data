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
        return False

    def authorization_header(self, request=None) -> str:
        """auth funct"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """get current user"""
        return None
