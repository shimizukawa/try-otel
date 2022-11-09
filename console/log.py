"""
setup logging
"""

import logging
from logging.config import dictConfig

from opentelemetry.util.types import Attributes
from opentelemetry.sdk._logs import LoggingHandler
from opentelemetry.semconv.trace import SpanAttributes

ALLOW_TYPES = (bool, str, int, float)


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

        # convert values to allowed types
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


def setup():
    # logging_config
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': ('%(levelname)s [%(asctime)s] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] %(name)s %(message)s'),
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'standard'
            },
            'otel_log': {  # Attach OTLP log handler to root logger
                # '()': 'opentelemetry.sdk._logs.LoggingHandler',
                '()': SafeLoggingHandler,
            },
        },
        'root': {  # Catch all
            'handlers': ['console', 'otel_log'],
            'level': 'NOTSET',
        },
    }
    dictConfig(logging_config)
