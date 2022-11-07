# https://github.com/open-telemetry/opentelemetry-python/blob/e1a4c38/docs/examples/django/client.py
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(BASE_DIR / '.env')

import requests

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk import resources

resource = resources.Resource(attributes={
    resources.SERVICE_NAME: "console-client",
    resources.SERVICE_NAMESPACE: "myapp",
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
# https://github.com/open-telemetry/opentelemetry.io/blob/dfadc50/content/en/docs/instrumentation/python/exporters.md
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint="lvh.me:4317", insecure=True))
)

# metrics exporter
# https://github.com/open-telemetry/opentelemetry.io/blob/dfadc50/content/en/docs/instrumentation/python/exporters.md
# https://github.com/open-telemetry/opentelemetry-python/tree/main/docs/examples/metrics
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader, ConsoleMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

provider = MeterProvider(resource=resource, metric_readers=[
    PeriodicExportingMetricReader(ConsoleMetricExporter()),
    PeriodicExportingMetricReader(OTLPMetricExporter(endpoint="lvh.me:4317", insecure=True)),
])
metrics.set_meter_provider(provider)


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
            'http://api.lvh.me/api/users',
            params={'param': 1234},
        )
        assert response.status_code == 200


if __name__ == '__main__':
    with tracer.start_as_current_span("client"):
        main()

    from opentelemetry.sdk._logs import get_logger_provider
    get_logger_provider().shutdown()
