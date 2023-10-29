"""
setup logging
"""

import logging.config


def config(config):
    """
    Djangoのsettings.LOGGING初期化前に設定されているhandlersを引き継ぐ
    """
    root = logging.getLogger()
    root_handlers = root.handlers[:]

    # dictConfigではどうやってもroot.handlersは消えてしまう
    logging.config.dictConfig(config)

    # バックアップしておいたhandlersを復元
    for h in root_handlers:
        if h not in root.handlers:
            root.addHandler(h)
