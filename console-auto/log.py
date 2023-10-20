"""
setup logging
"""

from logging.config import dictConfig


def setup():
    # logging_config
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': ('%(levelname)s [%(asctime)s] %(name)s %(message)s'),
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'standard'
            },
            'otel': {
                'level': 'DEBUG',
                'class': 'opentelemetry.sdk._logs.LoggingHandler',
                'formatter': 'standard'
            },
        },
        'root': {  # Catch all
            'handlers': ['console', 'otel'],
            'level': 'NOTSET',
        },
    }
    dictConfig(logging_config)
