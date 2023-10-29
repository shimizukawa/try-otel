"""
API client for Django API

https://github.com/open-telemetry/opentelemetry-python/blob/e1a4c38/docs/examples/django/client.py
"""
import logging

import requests
from opentelemetry.trace import get_tracer_provider

# get logger
logger = logging.getLogger(__name__)


def main():
    # get tracer for main process
    # **IMPORTANT**: it shoud not be called at module global
    tracer = get_tracer_provider().get_tracer(__name__)

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
        logger.debug("response raw body: %r", response.content)
        assert response.status_code == 200
        data = response.json()
        logger.debug('response data: %r', data)
