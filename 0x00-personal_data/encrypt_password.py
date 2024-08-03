#!/usr/bin/env python3
"""encryption with bcrypt"""
import bcrypt


def hash_password(password: str) -> bytes:
    """hashing password"""
    password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """to check if the password id valid"""
    if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
        return True
    else:
        return False
