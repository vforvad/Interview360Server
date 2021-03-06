import os
import logging
from app.paths import BASE_DIR

HANDLERS_LIST = ['console']
DISABLE_FILE_LOGGING = os.environ.get('DISABLE_FILE_LOGGING', False)

CONSOLE_HANDLER = {
    'level': logging.DEBUG,
    'class': 'logging.StreamHandler',
    'stream': 'stdout'
}

LOGGING = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': u"%(asctime)s [%(levelname)-8s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        }
    },
    'handlers': {
        'console': CONSOLE_HANDLER
    },
    'loggers': {
        'django': {
            'handlers': HANDLERS_LIST,
            'level': logging.DEBUG,
            'propagate': True
        },
    }
}

if not DISABLE_FILE_LOGGING:
    ENV = os.environ.get('DJANGO_DEFAULT_ENV', 'development')
    LOG_FILENAME = '{}.log'.format(
        os.environ.get('DJANGO_DEFAULT_ENV', 'development')
    )
    LOG_DIRECTORY = os.path.join(BASE_DIR, 'app', 'logs')
    LOG_LEVEL = 'INFO' if ENV == 'production' else 'DEBUG'
    FILE_HANDLER = {
        'level': LOG_LEVEL,
        'class': 'logging.FileHandler',
        'filename': os.path.join(LOG_DIRECTORY, LOG_FILENAME),
    }
    LOGGING['handlers']['file'] = FILE_HANDLER
    LOGGING['loggers']['django']['handlers'] += ['file']
