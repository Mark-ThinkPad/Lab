from flask import Flask
from flask_caching import Cache
from api import api
from views import views
from cache import cache
from settings import BASE_DIR


app = Flask(__name__)
app.register_blueprint(views)
app.register_blueprint(api, url_prefix='/api')

cache.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
