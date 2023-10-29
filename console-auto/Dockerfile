FROM python:3.11-slim-bookworm

WORKDIR /code

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=constraints.txt,target=constraints.txt \
    --mount=type=bind,source=console-auto/requirements.txt,target=requirements.txt \
    pip install --upgrade pip \
    pip install -r requirements.txt -c constraints.txt

COPY ./console-auto/ /code/

ENV OTEL_RESOURCE_ATTRIBUTES=deployment.environment=demo,service.namespace=myapp
ENV OTEL_SERVICE_NAME=console-auto

ENV OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SERVER_REQUEST=content_type,traceparent,tracestatus
ENV OTEL_PYTHON_TRACER_PROVIDER=sdk_tracer_provider
ENV OTEL_PYTHON_METER_PROVIDER=sdk_meter_provider
ENV OTEL_PYTHON_LOGGER_PROVIDER=sdk_logger_provider
ENV OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
ENV OTEL_PYTHON_LOG_CORRELATION=true
ENV OTEL_PYTHON_LOG_LEVEL=debug

ENV OTEL_PROPAGATORS="tracecontext,baggage"
ENV OTEL_TRACES_EXPORTER="otlp"
ENV OTEL_METRICS_EXPORTER="otlp"
ENV OTEL_LOGS_EXPORTER="otlp"
ENV OTEL_EXPORTER_OTLP_ENDPOINT=localhost:4317
ENV OTEL_EXPORTER_OTLP_INSECURE=true

CMD opentelemetry-instrument python client.py
