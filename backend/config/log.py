"""
setup logging
"""

import logging

from opentelemetry.util.types import Attributes
from opentelemetry.sdk._logs import LoggingHandler
from opentelemetry.semconv.trace import SpanAttributes

ALLOW_TYPES = (bool, str, int, float)


# TODO: use structlog


# https://opentelemetry.io/docs/reference/specification/logs/data-model/
# https://uptrace.dev/opentelemetry/attributes.html
class SafeLoggingHandler(LoggingHandler):

    @staticmethod
    def _get_attributes(record: logging.LogRecord) -> Attributes:
        attributes = LoggingHandler._get_attributes(record)
        # add useful information that they are avoided on LoggingHandler.
        attributes["log.name"] = record.name
        attributes["code.location"] = f"{record.pathname}:{record.lineno} in {record.funcName}"
        attributes[SpanAttributes.CODE_FILEPATH] = record.pathname
        attributes[SpanAttributes.CODE_LINENO] = record.lineno
        attributes[SpanAttributes.CODE_FUNCTION] = record.funcName

        # TODO: include local variables to stacktrace if it can be.

        # convert values to allowed types
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
