"""
setup logging
"""

import logging

from opentelemetry.util.types import Attributes
from opentelemetry.sdk._logs import LoggingHandler

ALLOW_TYPES = (bool, str, int, float)


# TODO: use structlog


class SafeLoggingHandler(LoggingHandler):

    @staticmethod
    def _get_attributes(record: logging.LogRecord) -> Attributes:
        attributes = LoggingHandler._get_attributes(record)
        # TODO: add log.name
        # TODO: include local variables to stacktrace if it can be.
        for key, value in attributes.items():
            if isinstance(value, ALLOW_TYPES):
                pass
            elif isinstance(value, (list, tuple)):
                attributes[key] = type(value)([
                    v if isinstance(v, ALLOW_TYPES) else str(v)
                    for v in value
                ])
            else:
                attributes[key] = str(value)

        return attributes
