from flask import (Blueprint, render_template,
                   request, make_response)
from EmotionAnalysis.API import API
import app
import time
import hashlib

views = Blueprint('views', __name__)


# Functions
def set_client_id() -> str:
    client_addr = request.remote_addr
    req_date = time.asctime()
    id_source = client_addr + ', ' + req_date
    # 进行md5加密
    m = hashlib.md5()
    m.update(id_source.encode(encoding='utf-8'))
    return m.hexdigest()


@views.route('/')
def index():
    client_id = request.cookies.get('client_id', False)
    res = make_response(render_template('index.html'))
    if not client_id:
        client_id = set_client_id()
        res.set_cookie('client_id', client_id)
    cache_api = app.cache.get(client_id)
    if cache_api is None:
        client_api = API()
        app.cache.set(client_id, client_api)
    else:
        app.cache.set(client_id, cache_api, timeout=60 * 60 * 24 * 1)
    return res
