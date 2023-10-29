"""
client (auto instrumentation) for Django API

https://github.com/open-telemetry/opentelemetry-python/blob/e1a4c38/docs/examples/django/client.py
"""
from pathlib import Path

import environ
from opentelemetry.trace import get_tracer_provider

import log
import main

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(BASE_DIR / '.env')

log.setup()

# get tracer for main process
tracer = get_tracer_provider().get_tracer(__name__)

if __name__ == '__main__':
    with tracer.start_as_current_span("client"):
        main.main()
