# https://github.com/open-telemetry/opentelemetry-python/blob/e1a4c38/docs/examples/django/client.py
from pathlib import Path
import logging

import environ

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(BASE_DIR / '.env')

import requests

logger = logging.getLogger(__name__)


# setup resource
from opentelemetry.sdk import resources
resource = resources.Resource(attributes={
    resources.SERVICE_NAME: "console-client",
    resources.SERVICE_NAMESPACE: "myapp",
})

# trace exporter
# https://github.com/open-telemetry/opentelemetry.io/blob/dfadc50/content/en/docs/instrumentation/python/exporters.md
from opentelemetry.trace import set_tracer_provider
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor, BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

tracer_provider = TracerProvider(resource=resource)
set_tracer_provider(tracer_provider)
tracer_provider.add_span_processor(
    SimpleSpanProcessor(ConsoleSpanExporter())
)
tracer_provider.add_span_processor(
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


# log exporter
# from https://github.com/open-telemetry/opentelemetry-python/blob/69c9e39/docs/examples/logs/example.py
from opentelemetry.sdk._logs import LoggerProvider, set_logger_provider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor, SimpleLogRecordProcessor, ConsoleLogExporter
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
logger_provider = LoggerProvider(resource=resource)
set_logger_provider(logger_provider)
logger_provider.add_log_record_processor(
    BatchLogRecordProcessor(OTLPLogExporter(endpoint="lvh.me:4317", insecure=True))
)
logger_provider.add_log_record_processor(
    SimpleLogRecordProcessor(ConsoleLogExporter())
)
# and add 'opentelemetry.sdk._logs.LoggingHandler' handler in settings.LOGGING
import log
log.setup()


# get tracer for main process
tracer = tracer_provider.get_tracer(__name__)


def main():
    # requests instrumentation
    import opentelemetry.instrumentation.requests
    opentelemetry.instrumentation.requests.RequestsInstrumentor().instrument()

    # Logging (inject trace_id etc into logger)
    from opentelemetry.instrumentation.logging import LoggingInstrumentor
    LoggingInstrumentor().instrument()

    logger.info('Hello')

    with tracer.start_as_current_span("get users"):
        # inject will do in otel framework.
        # from opentelemetry.propagate import inject
        # headers = {}; inject(headers)

        # action
        response = requests.get(
            'http://api.lvh.me/api/users',
            params={'param': 1234},
        )
        assert response.status_code == 200
        data = response.json()
        logger.debug('response data: %r', data)
        users = data["users"]
        assert len(users) > 0

    with tracer.start_as_current_span("update a user"):
        user = users[0]
        user["key"] = "value"  # TODO
        response = requests.post(
            f"http://api.lvh.me/api/users/{user['id']}",
            data=user,
        )
        logger.debug(response.content)
        assert response.status_code == 200
        data = response.json()
        logger.debug('response data: %r', data)


if __name__ == '__main__':
    with tracer.start_as_current_span("client"):
        main()

    from opentelemetry.sdk._logs import get_logger_provider
    get_logger_provider().shutdown()
