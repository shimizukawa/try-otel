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

# logging setup
import log
import logging
log.setup(resource)
logger = logging.getLogger(__name__)

# get tracer for main process
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

    from opentelemetry.sdk._logs import get_log_emitter_provider
    get_log_emitter_provider().shutdown()
