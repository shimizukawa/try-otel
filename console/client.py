# https://github.com/open-telemetry/opentelemetry-python/blob/e1a4c38/docs/examples/django/client.py

import requests

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

resource = Resource(attributes={
    SERVICE_NAME: "console client"
})
trace.set_tracer_provider(TracerProvider(resource=resource))

# console exporter
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)
trace.get_tracer_provider().add_span_processor(
    SimpleSpanProcessor(ConsoleSpanExporter())
)

# otelp span exporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint="localhost:4317", insecure=True))
)

# from https://github.com/open-telemetry/opentelemetry-python/blob/69c9e39/docs/examples/logs/example.py
from opentelemetry.sdk._logs import LogEmitterProvider, set_log_emitter_provider
from opentelemetry.sdk._logs.export import BatchLogProcessor, SimpleLogProcessor, ConsoleLogExporter
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
log_emitter_provider = LogEmitterProvider(resource=resource)
set_log_emitter_provider(log_emitter_provider)
log_emitter_provider.add_log_processor(
    BatchLogProcessor(OTLPLogExporter(endpoint="localhost:4317", insecure=True))
)
log_emitter_provider.add_log_processor(
    SimpleLogProcessor(ConsoleLogExporter())
)

# add handler in logging_config

# setup logging
from logging.config import dictConfig
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
import logging
logger = logging.getLogger(__name__)

tracer = trace.get_tracer_provider().get_tracer(__name__)


def main():
    # requests instrumentation
    import opentelemetry.instrumentation.requests
    opentelemetry.instrumentation.requests.RequestsInstrumentor().instrument()

    # Logging (inject trace_id etc into logger)
    from opentelemetry.instrumentation.logging import LoggingInstrumentor
    LoggingInstrumentor().instrument()

    logger.info('Hello')

    with tracer.start_as_current_span("requests"):
        # inject will do in otel framework.
        # from opentelemetry.propagate import inject
        # headers = {}; inject(headers)

        # action
        response = requests.get(
            'http://localhost:8000/',
            params={'param': 1234},
        )
        assert response.status_code == 200


if __name__ == '__main__':
    with tracer.start_as_current_span("client"):
        main()
    log_emitter_provider.shutdown()
