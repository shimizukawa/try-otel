"""
setup logging
"""

from logging.config import dictConfig

from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk._logs import LogEmitterProvider, set_log_emitter_provider
from opentelemetry.sdk._logs.export import BatchLogProcessor, SimpleLogProcessor, ConsoleLogExporter
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter


def setup(resource: Resource):
    # from https://github.com/open-telemetry/opentelemetry-python/blob/69c9e39/docs/examples/logs/example.py
    log_emitter_provider = LogEmitterProvider(resource=resource)
    set_log_emitter_provider(log_emitter_provider)
    log_emitter_provider.add_log_processor(
        BatchLogProcessor(OTLPLogExporter(endpoint="localhost:4317", insecure=True))
    )
    log_emitter_provider.add_log_processor(
        SimpleLogProcessor(ConsoleLogExporter())
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
            'otel': {  # Attach OTLP handler to root logger
                '()': 'opentelemetry.sdk._logs.LoggingHandler',
            }
        },
        'root': {  # Catch all
            'handlers': ['console', 'otel'],
            'level': 'NOTSET',
        },
    }
    dictConfig(logging_config)
