"""setup opentelemetry exporters and instrumentors

https://github.com/open-telemetry/opentelemetry-python/blob/e1a4c38/docs/examples/django/client.py
"""
import sys
import logging
from os import environ
from urllib.parse import parse_qsl

import django
from django.http import HttpRequest, HttpResponse
from opentelemetry.sdk import resources
from opentelemetry.sdk.environment_variables import OTEL_RESOURCE_ATTRIBUTES
from opentelemetry.sdk.trace import Span
from opentelemetry.distro import OpenTelemetryDistro, OpenTelemetryConfigurator
from pkg_resources import iter_entry_points
from setuptools_scm import get_version

logger = logging.getLogger(__name__)


class MyDistro(OpenTelemetryDistro):

    def _configure(self, **kwargs):
        super()._configure(**kwargs)
        self.load_instrumentors()

    def load_instrumentors(self):
        instrumentors = {}
        for entry_point in iter_entry_points("opentelemetry_instrumentor"):
            instrumentors[entry_point.name] = entry_point
        self.instrumentors = instrumentors
        logger.debug("available instrumenters %r", sorted(self.instrumentors))

    def load_instrumentor_by_name(
        self, entry_point_name: str, **kwargs
    ):
        if entry_point_name not in self.instrumentors:
            logger.warning("Skipping instrumentation %s: %s", entry_point_name, "Not Found")
            return
        entry_point = self.instrumentors[entry_point_name]
        self.load_instrumentor(entry_point, **kwargs)
        logger.debug("Instrumented %s", entry_point.name)

    def update_resources(self, resources: dict[str, str]):
        sep = ","
        env_resource_dict = dict(parse_qsl(environ.get(OTEL_RESOURCE_ATTRIBUTES, ""), separator=sep))
        env_resource_dict.update(resources)
        environ[OTEL_RESOURCE_ATTRIBUTES] = sep.join(
            f"{key}={value}"
            for key, value in env_resource_dict.items()
        )


def setup():
    distro = MyDistro()
    distro.update_resources({
        # # https://opentelemetry.io/docs/reference/specification/resource/semantic_conventions/#service
        resources.SERVICE_VERSION: get_version(search_parent_directories=True),
        # https://opentelemetry.io/docs/reference/specification/resource/semantic_conventions/process/
        resources.PROCESS_RUNTIME_NAME: sys.implementation.name,
        resources.PROCESS_RUNTIME_VERSION: '.'.join(map(str, sys.implementation.version)),
        resources.PROCESS_COMMAND_ARGS: " ".join(sys.argv),
        # https://opentelemetry.io/docs/reference/specification/resource/semantic_conventions/webengine/
        resources.ResourceAttributes.WEBENGINE_NAME: "django",
        resources.ResourceAttributes.WEBENGINE_VERSION: django.__version__,
    })
    distro.configure()
    OpenTelemetryConfigurator().configure()

    # Psycopg2
    # psycopg2-binary をインストールしていると動作しないため skip_dep_check=True で回避
    # https://github.com/open-telemetry/opentelemetry-python-contrib/issues/610#issuecomment-1295391610
    distro.load_instrumentor_by_name(
        "psycopg2", enable_commenter=True, commenter_options={}, skip_dep_check=True,
    )
    # Django
    # django request_hook / response_hook
    # https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/django/django.html#request-and-response-hooks
    distro.load_instrumentor_by_name(
        "django", is_sql_commentor_enabled=True, request_hook=request_hook, response_hook=response_hook,
    )

    distro.load_instrumentor_by_name("urllib")
    distro.load_instrumentor_by_name("urllib3")


def request_hook(span: Span, request: HttpRequest):
    import json
    attributes = {
        "custom.http.get": json.dumps(request.GET),
        "custom.http.post": json.dumps(request.POST),
    }
    span.add_event(
        "Django request params",
        attributes,
    )

    # add_event is better than logging because Uptrace tab is separated to EVENT
    # import logging
    # logger = logging.getLogger(__name__)
    # logger.debug("Django request params", extra=attributes)


def response_hook(span: Span, request: HttpRequest, response: HttpResponse):
    attributes = {
        "custom.http.response": response.content[:1000],
    }
    span.add_event(
        "Django response data",
        attributes,
    )

    # add_event is better than logging because Uptrace tab is separated to EVENT
    # import logging
    # logger = logging.getLogger(__name__)
    # logger.debug("Django response data", extra=attributes)
