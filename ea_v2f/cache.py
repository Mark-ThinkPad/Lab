from flask_caching import Cache
from settings import BASE_DIR

config = {
    'CACHE_TYPE': 'filesystem',  # Flask-Caching related configs
    'CACHE_DEFAULT_TIMEOUT': 60 * 60 * 24 * 1,  # cache files save for 1 day
    'CACHE_IGNORE_ERRORS': True,
    'CACHE_DIR': BASE_DIR + '/cache',
    'CACHE_THRESHOLD': 128,
}

cache = Cache(config=config)
