#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(BASE_DIR / '.env')

# patch for opentelemetry-instrumentation-psycopg2
# psycopg2-binary をインストールしていると動作しないため回避
# https://github.com/open-telemetry/opentelemetry-python-contrib/issues/610#issuecomment-953168011
import opentelemetry.instrumentation.dependencies
orig_get_dependency_conflicts = opentelemetry.instrumentation.dependencies.get_dependency_conflicts
def psycopg2_or_psycopg2_binary_dependency_conficts(deps):
    if 'psycopg2 >= 2.7.3.1' in deps:
        conflict = orig_get_dependency_conflicts(deps)
        if conflict and not conflict.found:
            return orig_get_dependency_conflicts(['psycopg2-binary>=2.7.3.1'])
    return orig_get_dependency_conflicts(deps)
opentelemetry.instrumentation.dependencies.get_dependency_conflicts = psycopg2_or_psycopg2_binary_dependency_conficts

# setup exporter
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

resource = Resource(attributes={
    SERVICE_NAME: "django-backend"
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

# span exporter
# https://github.com/open-telemetry/opentelemetry.io/blob/dfadc50/content/en/docs/instrumentation/python/exporters.md
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint="localhost:4317", insecure=True))
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
    PeriodicExportingMetricReader(OTLPMetricExporter(endpoint="localhost:4317", insecure=True)),
])
metrics.set_meter_provider(provider)


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    # Postgres
    from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
    Psycopg2Instrumentor().instrument(enable_commenter=True, commenter_options={})

    # This call is what makes the Django application be instrumented
    from opentelemetry.instrumentation.django import DjangoInstrumentor
    DjangoInstrumentor().instrument()

    # Logging（ログ出力へのtrace_id等差し込み）
    from opentelemetry.instrumentation.logging import LoggingInstrumentor
    LoggingInstrumentor().instrument()

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
