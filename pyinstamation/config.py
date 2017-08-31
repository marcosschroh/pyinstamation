import sys
import yaml
import logging
import logging.config

SAVE_SOURCE = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file_handler': {
            'level': 'INFO',
            'filename': './pyinstamation.log',
            'class': 'logging.FileHandler',
            'formatter': 'standard'
        }
    },
    'loggers': {
        'pyinstamation': {
            'handlers': ['default', 'file_handler'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}

logging.config.dictConfig(LOGGING)

CONFIG = {}


def load_config(filepath=None):
    global CONFIG

    if CONFIG and filepath is None:
        return
    if filepath is None:
        filepath = './config.yaml'

    with open(filepath, 'r') as stream:
        try:
            CONFIG.update(yaml.load(stream))
        except yaml.YAMLError as exc:
            sys.exit(exc)


load_config()
