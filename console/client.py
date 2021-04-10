import requests

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
trace.set_tracer_provider(TracerProvider())

# console exporter
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)
trace.get_tracer_provider().add_span_processor(
    SimpleSpanProcessor(ConsoleSpanExporter())
)

# opencensus exporter
from opentelemetry.exporter.opencensus.trace_exporter import (
    OpenCensusSpanExporter,
)
from opentelemetry.sdk.trace.export import BatchSpanProcessor
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(OpenCensusSpanExporter(endpoint="localhost:55678"))
)


def main():
    # instrumentation
    import opentelemetry.instrumentation.requests
    opentelemetry.instrumentation.requests.RequestsInstrumentor().instrument()

    # action
    response = requests.get('http://localhost:8000/')
    assert response.status_code == 200


if __name__ == '__main__':
    main()