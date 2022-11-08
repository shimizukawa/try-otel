"""
setup logging
"""

import logging

from opentelemetry.util.types import Attributes
from opentelemetry.sdk._logs import LoggingHandler

ALLOW_TYPES = (bool, str, int, float)


class SafeLoggingHandler(LoggingHandler):

    @staticmethod
    def _get_attributes(record: logging.LogRecord) -> Attributes:
        attributes = LoggingHandler._get_attributes(record)
        for key, value in attributes.items():
            if isinstance(value, ALLOW_TYPES):
                pass
            elif isinstance(value, (list, tuple)):
                for v in value:
                    if not isinstance(v, ALLOW_TYPES):
                        raise ValueError()
            else:
                attributes[key] = str(value)

        return attributes
