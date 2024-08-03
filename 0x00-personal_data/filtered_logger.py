#!/usr/bin/env python3
"""filtering data"""
import logging
from typing import List
import re
from os import getenv
import mysql.connector


PII_FIELDS = (name, email, phone, ssn, password, ip, last_login, user_agent)


def filter_datum(
        fields: List[str],
        redaction: str, message: str, separator: str) -> str:
    """Redacts specified fields in a message string."""
    for field in fields:
        message = re.sub(
                rf'{field}=[^;{separator}]+', f'{field}={redaction}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """init method"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """formating info"""
        record.msg = filter_datum(
                self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """Returns a logger object configured with RedactingFormatter."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    console_handler = logging.StreamHandler()
    formatter = RedactingFormatter(list(PII_FIELDS))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """get db module"""
    host_name = getenv("PERSONAL_DATA_DB_HOST")
    if host_name is None:
        host_name = "localhost"
    user_name = getenv("PERSONAL_DATA_DB_USERNAME")
    if user_name is None:
        user_name = "root"
    pass_word = getenv("PERSONAL_DATA_DB_PASSWORD")
    if pass_word is None:
        pass_word = ""
    return mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=pass_word,
            database=getenv("PERSONAL_DATA_DB_NAME"))
