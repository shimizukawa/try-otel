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

# otelp exporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint="localhost:4317", insecure=True))
)

# setup logging
from logging.config import dictConfig

config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': ('%(levelname)s [%(asctime)s] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] %(name)s %(message)s'),
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'root': {  # 全てキャッチする
        'handlers': ['console'],
        'level': 'NOTSET',
    },
}
dictConfig(config)


def main():
    # requests instrumentation
    import opentelemetry.instrumentation.requests
    opentelemetry.instrumentation.requests.RequestsInstrumentor().instrument()

    # Logging（ログ出力へのtrace_id等差し込み）
    from opentelemetry.instrumentation.logging import LoggingInstrumentor
    LoggingInstrumentor().instrument()

    # action
    response = requests.get('http://localhost:8000/')
    assert response.status_code == 200


if __name__ == '__main__':
    main()