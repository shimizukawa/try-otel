"""setup opentelemetry exporters and instrumentors

https://github.com/open-telemetry/opentelemetry-python/blob/e1a4c38/docs/examples/django/client.py
"""
import sys
import logging
from os import environ
from urllib.parse import parse_qsl

from opentelemetry.sdk import resources
from opentelemetry.sdk.environment_variables import OTEL_RESOURCE_ATTRIBUTES
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
    })
    distro.configure()
    OpenTelemetryConfigurator().configure()

    distro.load_instrumentor_by_name("requests")
    distro.load_instrumentor_by_name("urllib")
    distro.load_instrumentor_by_name("urllib3")

    from log import SafeLoggingHandler
    root = logging.getLogger()
    root.addHandler(
        SafeLoggingHandler(
            level="NOTSET",
            logger_provider=None,
        )
    )
