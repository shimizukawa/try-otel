"""setup opentelemetry exporters and instrumentors

https://github.com/open-telemetry/opentelemetry-python/blob/e1a4c38/docs/examples/django/client.py
"""

from django.http import HttpRequest, HttpResponse
from opentelemetry.sdk.trace import Span


# Psycopg2
# psycopg2-binary をインストールしていると動作しないため skip_dep_check=True で回避
# https://github.com/open-telemetry/opentelemetry-python-contrib/issues/610#issuecomment-1295391610
# "psycopg2", enable_commenter=True, commenter_options={}, skip_dep_check=True,

# Django
# https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/django/django.html#request-and-response-hooks
# "django", is_sql_commentor_enabled=True, request_hook=request_hook, response_hook=response_hook,

def request_hook(span: Span, request: HttpRequest):
    import json
    attributes = {
        "custom.http.get": json.dumps(request.GET),
        "custom.http.post": json.dumps(request.POST),
    }
    # span.add_event() is better than logger.debug() because Uptrace tab is separated to EVENT
    span.add_event(
        "Django request params",
        attributes,
    )

def response_hook(span: Span, request: HttpRequest, response: HttpResponse):
    attributes = {
        "custom.http.response": response.content[:1000],
    }
    # span.add_event() is better than logger.debug() because Uptrace tab is separated to EVENT
    span.add_event(
        "Django response data",
        attributes,
    )
