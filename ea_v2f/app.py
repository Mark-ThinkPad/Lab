from flask import Flask
from flask_caching import Cache
from api import api
from views import views
from settings import BASE_DIR

config = {
    'CACHE_TYPE': 'filesystem',  # Flask-Caching related configs
    'CACHE_DEFAULT_TIMEOUT': 60 * 60 * 24 * 1,  # cache files save for 1 day
    'CACHE_IGNORE_ERRORS': True,
    'CACHE_DIR': BASE_DIR + '/cache',
    'CACHE_THRESHOLD': 128,
}

app = Flask(__name__)
app.register_blueprint(views)
app.register_blueprint(api, url_prefix='/api')

cache = Cache(config=config)
cache.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
