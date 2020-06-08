from flask import Blueprint, request
from settings import BASE_DIR
from EmotionAnalysis.API import API
from cache import cache
import os

api = Blueprint('api', __name__)


@api.route('/getContent', methods=['POST'])
def getContent():
    words = request.form.get('words', False)
    client_id = request.form.get('client_id', False)
    if not words:
        return {'status': 0, 'message': '请输入一句话!'}
    if not client_id:
        return {'status': 0, 'message': '系统缓存丢失, 将会自动刷新页面, 点击继续'}

    cache_api: API = cache.get(client_id)
    if cache_api is None:
        return {'status': 0, 'message': '系统缓存丢失, 将会自动刷新页面, 点击继续'}

    res = cache_api.getContent(words)
    return {'status': 1, 'message': res}


@api.route('/getFile', methods=['POST'])
def getFile():
    client_id = request.form.get('client_id', False)
    f = request.files.get('csvFile', False)
    if not client_id:
        return {'status': 0, 'message': '系统缓存丢失, 将会自动刷新页面, 点击继续'}
    if not f:
        return {'status': 0, 'message': '请选择列名为"content"的csv文件!'}

    cache_api: API = cache.get(client_id)
    if cache_api is None:
        return {'status': 0, 'message': '系统缓存丢失, 将会自动刷新页面, 点击继续'}

    path = BASE_DIR + '/media/csv/' + f.filename
    f.save(path)
    res = cache_api.getFile(path)
    if os.path.exists(path):
        os.remove(path)

    return {'status': 1, 'message': res}


# getCRFModel, getDictModel, getAtrain 3 in 1
@api.route('/get/<string:kw>', methods=['POST'])
def getTriple(kw):
    client_id = request.form.get('client_id', False)
    if not client_id:
        return {'status': 0, 'message': '系统缓存丢失, 将会自动刷新页面, 点击继续'}

    cache_api: API = cache.get(client_id)
    if cache_api is None:
        return {'status': 0, 'message': '系统缓存丢失, 将会自动刷新页面, 点击继续'}

    res = 'Bad Ajax Request'
    if kw == 'CRFModel':
        res = cache_api.getCRFModel()
    if kw == 'DictModel':
        res = cache_api.getDictModel()
    if kw == 'Atrain':
        res = cache_api.getAtrain()

    return {'status': 1, 'message': res}
