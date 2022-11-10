#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path

import environ

# first: setup environment
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(BASE_DIR / '.env')


def main():
    """Run administrative tasks."""
    # second: define settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    # third: setup opentelemetry exporters and instrumentors
    from config import otel
    otel.setup("django-backend", "myapp")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
