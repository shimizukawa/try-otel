"""
setup logging
"""

import logging.config


def setup():
    """
    settings.LOGGING初期化前に設定されているhandlersを引き継ぐ
    """
    root = logging.getLogger()
    root_handlers = root.handlers[:]

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
        },
        'root': {  # Catch all
            'handlers': ['console'],
            'level': 'NOTSET',
        },
    }

    # dictConfigではどうやってもroot.handlersは消えてしまう
    logging.config.dictConfig(logging_config)

    # バックアップしておいたhandlersを復元
    for h in root_handlers:
        if h not in root.handlers:
            root.addHandler(h)
