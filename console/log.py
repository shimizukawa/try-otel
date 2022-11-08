"""
setup logging
"""

import logging
from logging.config import dictConfig

from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk._logs import LoggerProvider, set_logger_provider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor, SimpleLogRecordProcessor, ConsoleLogExporter
from opentelemetry.sdk._logs.severity import std_to_otlp
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.trace.propagation import get_current_span


class SpanLoggingHandler(LoggingHandler):

    def emit(self, record: logging.LogRecord) -> None:
        translated_record = self._translate(record)
        attributes = {
            "body": translated_record.body,
            "severity_text": translated_record.severity_text,
            "severity_number": translated_record.severity_number.value,
        }

        span = get_current_span()
        span.add_event(
            record.name,
            attributes,
            translated_record.timestamp
        )

        # if span is not exist?
        # attributes = {
        #     key: value
        #     for (key, value) in translated_record.attributes.items()
        #     if not key.startswith('otel')
        # )


def setup(resource: Resource):
    # setup log exporter
    # from https://github.com/open-telemetry/opentelemetry-python/blob/69c9e39/docs/examples/logs/example.py
    log_emitter_provider = LoggerProvider(resource=resource)
    set_logger_provider(log_emitter_provider)
    log_emitter_provider.add_log_record_processor(
        BatchLogRecordProcessor(OTLPLogExporter(endpoint="lvh.me:4317", insecure=True))
    )
    log_emitter_provider.add_log_record_processor(
        SimpleLogRecordProcessor(ConsoleLogExporter())
    )
    # add handler in logging_config

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
                '()': 'opentelemetry.sdk._logs.LoggingHandler',
            },
            'otel_span': {  # Attach OTLP span handler to root logger
                '()': SpanLoggingHandler,
            },
        },
        'root': {  # Catch all
            'handlers': ['console', 'otel_log', 'otel_span'],
            'level': 'NOTSET',
        },
    }
    dictConfig(logging_config)
