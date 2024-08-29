#!/usr/bin/env python3
"""
Filter message
"""
import re


def filter_datum(fields, redaction, message, separator):
    for field in fields:
        pattern = r'{}=.*?{}'.format(re.escape(field), re.escape(separator))
        message = re.sub(pattern, f'{field}={redaction}{separator}', message)
    return message
