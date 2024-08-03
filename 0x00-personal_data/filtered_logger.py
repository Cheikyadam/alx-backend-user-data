#!/usr/bin/env python3
"""filtering logger data"""
import re


def filter_datum(fields, redaction, message, separator) -> str:
    """function def here"""
    for field in fields:
        message = re.sub(rf'{field}=[^;]+', f"{field}={redaction}", message)
    return message
