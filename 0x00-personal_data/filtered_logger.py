#!/usr/bin/env python3
"""
Module for filtering sensitive information from log messages.
"""
import re


def filter_datum(fields, redaction, message, separator):
    """
    Replaces sensitive fields in a log message with a redaction.
    """
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}'.format(field, separator),
                         f'{field}={redaction}{separator}', message)
    return message
