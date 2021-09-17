#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# patch mysql
import pymysql
pymysql.version_info = (1, 4, 2, "final", 0)
pymysql.install_as_MySQLdb()

# setup exporter
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

# console exporter
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)
trace.set_tracer_provider(TracerProvider())
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
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'otel.settings')

    # This call is what makes the Django application be instrumented
    from opentelemetry.instrumentation.django import DjangoInstrumentor
    DjangoInstrumentor().instrument()

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
