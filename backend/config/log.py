"""
setup logging
"""

import logging

from opentelemetry.util.types import Attributes
from opentelemetry.sdk._logs import LoggingHandler

import structlog

ALLOW_TYPES = (bool, str, int, float)


# use structlog
# TODO: implement LoggingHandler processor/formatter to spread struct into attributes
# https://docs.datadoghq.com/ja/tracing/other_telemetry/connect_logs_and_traces/opentelemetry/?tab=python
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)


class SafeLoggingHandler(LoggingHandler):

    @staticmethod
    def _get_attributes(record: logging.LogRecord) -> Attributes:
        attributes = LoggingHandler._get_attributes(record)
        # add useful information that they are avoided on LoggingHandler.
        attributes["log.name"] = record.name
        attributes["log.location"] = f"{record.pathname}:{record.lineno} in {record.funcName}"
        attributes["log.filepath"] = record.pathname
        attributes["log.lineno"] = record.lineno
        attributes["log.funcname"] = record.funcName

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
