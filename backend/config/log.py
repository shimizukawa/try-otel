"""
setup logging
"""

import logging

from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk._logs import LogEmitterProvider, set_log_emitter_provider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogProcessor, SimpleLogProcessor, ConsoleLogExporter
from opentelemetry.sdk._logs.severity import std_to_otlp
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.trace.propagation import get_current_span
from opentelemetry.trace import get_tracer_provider


class SpanLoggingHandler(LoggingHandler):

    def emit(self, record: logging.LogRecord) -> None:
        translated_record = self._translate(record)
        attributes = {
            key: value
            for (key, value) in translated_record.attributes.items()
            if not key.startswith('otel')
        } | dict(
            severity_text = record.levelname,
            severity_number = std_to_otlp(record.levelno).value,
        )
        span = get_current_span()
        span.add_event(
            translated_record.body,
            attributes,
            translated_record.timestamp
        )


def setup(resource: Resource|None = None):
    if resource is None:
        resource = get_tracer_provider().resource

    # setup log exporter
    # from https://github.com/open-telemetry/opentelemetry-python/blob/69c9e39/docs/examples/logs/example.py
    log_emitter_provider = LogEmitterProvider(resource=resource)
    set_log_emitter_provider(log_emitter_provider)
    log_emitter_provider.add_log_processor(
        BatchLogProcessor(OTLPLogExporter(endpoint="localhost:4317", insecure=True))
    )
    log_emitter_provider.add_log_processor(
        SimpleLogProcessor(ConsoleLogExporter())
    )
    # add handler in settings.LOGGING
