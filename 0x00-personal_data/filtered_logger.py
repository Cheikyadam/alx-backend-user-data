#!/usr/bin/env python3
"""filtering logger data"""
import re
from typing import List


def filter_datum(
        fields: List[str],
        redaction: str, message: str, separator: str) -> str:
    """Redacts specified fields in a message string."""
    for field in fields:
        message = re.sub(
                rf'{field}=[^;{separator}]+', f'{field}={redaction}', message)
    return message
