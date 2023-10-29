"""setup opentelemetry exporters and instrumentors

https://github.com/open-telemetry/opentelemetry-python/blob/e1a4c38/docs/examples/django/client.py
"""
import sys
import logging
from os import environ
from urllib.parse import parse_qsl

from opentelemetry.sdk import resources
from opentelemetry.sdk.environment_variables import OTEL_RESOURCE_ATTRIBUTES
from opentelemetry.instrumentation.distro import BaseDistro
from opentelemetry.instrumentation.auto_instrumentation._load import (
    _load_configurators,
    _load_distro,
)
from pkg_resources import EntryPoint, iter_entry_points

logger = logging.getLogger(__name__)


def update_resources(resources: dict[str, str]):
    sep = ","
    env_resource_dict = dict(parse_qsl(environ.get(OTEL_RESOURCE_ATTRIBUTES, ""), separator=sep))
    env_resource_dict.update(resources)
    environ[OTEL_RESOURCE_ATTRIBUTES] = sep.join(
        f"{key}={value}"
        for key, value in env_resource_dict.items()
    )


def load_instrumentors():
    instrumentors = {}
    for entry_point in iter_entry_points("opentelemetry_instrumentor"):
        instrumentors[entry_point.name] = entry_point
    return instrumentors


def load_instrumentor_by_name(
    distro: BaseDistro,
    entry_point_name: str,
    **kwargs
) -> EntryPoint:
    instrumentors = load_instrumentors()
    if entry_point_name not in instrumentors:
        logger.warning("Skipping instrumentation %s: %s", entry_point_name, "Not Found")
        return
    entry_point = instrumentors[entry_point_name]
    distro.load_instrumentor(entry_point, **kwargs)
    logger.debug("Instrumented %s", entry_point.name)


def setup():
    update_resources({
        # https://opentelemetry.io/docs/reference/specification/resource/semantic_conventions/process/
        resources.PROCESS_RUNTIME_NAME: sys.implementation.name,
        resources.PROCESS_RUNTIME_VERSION: '.'.join(map(str, sys.implementation.version)),
        resources.PROCESS_COMMAND_ARGS: " ".join(sys.argv),
    })
    distro = _load_distro()
    distro.configure()
    _load_configurators()

    load_instrumentor_by_name(distro, "requests")
    load_instrumentor_by_name(distro, "urllib")
    load_instrumentor_by_name(distro, "urllib3")
