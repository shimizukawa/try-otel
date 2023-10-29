FROM python:3.11-slim-bookworm

WORKDIR /code

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=constraints.txt,target=constraints.txt \
    --mount=type=bind,source=backend/requirements.txt,target=requirements.txt \
    pip install --upgrade pip \
    pip install -r requirements.txt -c constraints.txt

COPY ./backend/ /code/

# Django App
ENV DATABASE_URL "postgres://postgres:postgres@postgres:5432/backend"
ENV DJANGO_SETTINGS_MODULE "config.settings"

# https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/
# https://opentelemetry.io/docs/reference/specification/sdk-environment-variables/
# https://opentelemetry.io/docs/reference/specification/resource/sdk/
# https://opentelemetry.io/docs/reference/specification/resource/semantic_conventions/
ENV OTEL_RESOURCE_ATTRIBUTES "deployment.environment=demo,service.namespace=myapp"
ENV OTEL_SERVICE_NAME "django"

# Python Provider
ENV OTEL_PYTHON_TRACER_PROVIDER "sdk_tracer_provider"
ENV OTEL_PYTHON_METER_PROVIDER "sdk_meter_provider"
ENV OTEL_PYTHON_LOGGER_PROVIDER "sdk_logger_provider"
ENV OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED "true"
ENV OTEL_PYTHON_LOG_CORRELATION "true"
ENV OTEL_PYTHON_LOG_LEVEL "debug"

# Django Instrumentation
# https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/django/django.html#request-attributes
ENV OTEL_PYTHON_DJANGO_TRACED_REQUEST_ATTRS "path_info,content_type"
# https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/django/django.html#request-headers
ENV OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SERVER_REQUEST "content_type,traceparent,tracestatus"

# Exporter
ENV OTEL_PROPAGATORS "tracecontext,baggage"
ENV OTEL_TRACES_EXPORTER "otlp"
ENV OTEL_METRICS_EXPORTER "otlp"
ENV OTEL_LOGS_EXPORTER "otlp"
# https://opentelemetry.io/docs/concepts/sdk-configuration/otlp-exporter-configuration/
# https://opentelemetry.io/docs/reference/specification/protocol/exporter/#configuration-options
ENV OTEL_EXPORTER_OTLP_ENDPOINT "localhost:4317"
ENV OTEL_EXPORTER_OTLP_INSECURE "true"

CMD opentelemetry-instrument python manage.py runserver 0.0.0.0:8000 --noreload
