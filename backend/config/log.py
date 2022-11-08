"""
setup logging
"""

import logging

from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk._logs import LoggerProvider, set_logger_provider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor, SimpleLogRecordProcessor, ConsoleLogExporter
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.trace.propagation import get_current_span
from opentelemetry.trace import get_tracer_provider


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

        # spanが無い場合、自分で組み立てて送信するか？

        # "span_id": translated_record.span_id,
        # "trace_flags": translated_record.trace_flags,
        # "trace_id": translated_record.trace_id,
        # attributes = {
        #     key.lower().replace("-", "_"): value
        #     for (key, value) in translated_record.attributes.items()
        #     if not (key.startswith('otel') or key == "headers")
        # } | {
        #     # https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/trace/semantic_conventions/http.md#http-request-and-response-headers
        #     "http.request.header." + key.lower().replace("-", "_"): value
        #     for (key, value) in translated_record.attributes.get("headers", {}).items()
        # }
        # if translated_record.attributes.get("otelServiceName"):
        #     resource = attributes.setdefault("resource", {}).setdefault("attributes", {})
        #     resource["service.name"] = translated_record.attributes["otelServiceName"]
        # from pprint import pprint
        # print("## attributes (something NG)")
        # pprint(attributes)


def setup(resource: Resource|None = None):
    if resource is None:
        resource = get_tracer_provider().resource

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
    # add handler in settings.LOGGING
