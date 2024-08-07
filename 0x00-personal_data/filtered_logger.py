#!/usr/bin/env python3
"""filtering data"""
import logging
from typing import List
import re
from os import getenv
import mysql.connector
from mysql.connector import connection

PII_FIELDS = (
        "name", "email", "phone", "ssn",
        "password", "ip", "last_login", "user_agent")


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


def get_db() -> connection.MySQLConnection:
    """get db module"""
    host_name = getenv("PERSONAL_DATA_DB_HOST", "localhost")
    user_name = getenv("PERSONAL_DATA_DB_USERNAME", "root")
    pass_word = getenv("PERSONAL_DATA_DB_PASSWORD", "")
    return mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=pass_word,
            database=getenv("PERSONAL_DATA_DB_NAME"))


def dict_to_string(row):
    """helper func"""
    return ';'.join(f"{key}={value}" for key, value in row.items())

def main() -> None:
    """main function here"""
    message = ""
    log_record = logging.LogRecord(
            "user_data", logging.INFO, None, None, message, None, None)
    formatter = RedactingFormatter(
            fields=("name", "email", "phone", "ssn", "password"))
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()
    for row in rows:
        message = dict_to_string(row)
        log_record.msg = message
        print(formatter.format(log_record))
    cursor.close()
    db.close()

if __name__ == "__main__":
    """exectue main func"""
    main()
