#!/usr/bin/env python3
"""
Module for filtering sensitive information from log messages.
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Replaces sensitive fields in a log message with a redaction.
    """
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}'.format(field, separator),
                         f'{field}={redaction}{separator}', message)
    return message
