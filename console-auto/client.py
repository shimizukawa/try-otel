"""
client for Django API

https://github.com/open-telemetry/opentelemetry-python/blob/e1a4c38/docs/examples/django/client.py
"""
from pathlib import Path
import logging

import environ
import requests
from opentelemetry.trace import get_tracer_provider
from opentelemetry.sdk._logs import LoggingHandler as OtelLoggingHandler

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(BASE_DIR / '.env')

import log
log.setup()

logger = logging.getLogger("console-auto.client")

# get tracer for main process
tracer = get_tracer_provider().get_tracer("console-auto")


def main():
    logger.info('Hello')

    with tracer.start_as_current_span("get users"):
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
