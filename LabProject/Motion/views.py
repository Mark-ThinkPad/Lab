from django.shortcuts import render
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.views.decorators.http import require_GET, require_POST
from django.http.response import JsonResponse, HttpResponseForbidden, HttpResponseServerError
from Motion.EmotionAnalysis.API import API
import hashlib


# Functions
def set_client_id(request) -> str:
    client_addr = request.META.get('REMOTE_ADDR', 'anonymous')
    client_host = request.META.get('REMOTE_HOST', 'unknown hostname')
    client_port = request.META.get('REMOTE_PORT', 'random')
    id_source = client_addr + ', ' + client_host + ', ' + client_port
    # 进行md5加密
    m = hashlib.md5()
    m.update(id_source.encode(encoding='utf-8'))
    return m.hexdigest()


# Home Page
@require_GET
def index(request):
    client_id = request.COOKIES.get('client_id', False)
    response = render(request, 'index.html')
    if not client_id:
        client_id = set_client_id(request)
        response.set_cookie('client_id', client_id)

    cache_api = cache.get(client_id, False)
    if not cache_api:
        client_api = API()
        cache.set(client_id, client_api, timeout=60 * 60 * 24 * 1)
    else:
        cache.touch(client_id, timeout=60 * 60 * 24 * 1)

    return response


# APIs
# API getContent
@require_POST
@csrf_exempt
def api_getContent(request):
    if request.is_ajax():
        if request.method == 'POST':
            words = request.POST.get('words', False)
            client_id = request.POST.get('client_id', False)
            if not words:
                return JsonResponse({'status': 0, 'message': '请输入一句话!'})
            if not client_id:
                return JsonResponse({'status': 0, 'message': '系统缓存丢失, 将会自动刷新页面, 点击继续'})

            cache_api: API = cache.get(client_id, False)
            if not cache_api:
                return JsonResponse({'status': 0, 'message': '系统缓存丢失, 将会自动刷新页面, 点击继续'})

            res = cache_api.getContent(words)
            return JsonResponse({'status': 1, 'message': res})
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseServerError()


# API getFile
@require_POST
@csrf_exempt
def api_getFile(request):
    if request.is_ajax():
        if request.method == 'POST':
            client_id = request.POST.get('client_id', False)
            csvFile = request.FILES.get('csvFile', False)
            if not client_id:
                return JsonResponse({'status': 0, 'message': '系统缓存丢失, 将会自动刷新页面, 点击继续'})
            if not csvFile:
                return JsonResponse({'status': 0, 'message': '请选择列名为"content"的csv文件!'})

            cache_api: API = cache.get(client_id, False)
            if not cache_api:
                return JsonResponse({'status': 0, 'message': '系统缓存丢失, 将会自动刷新页面, 点击继续'})

            path = default_storage.save('../media/csv/' + csvFile.name, csvFile)
            f = default_storage.open(path)
            res = cache_api.getFile(f)
            default_storage.delete(path)

            return JsonResponse({'status': 1, 'message': res})
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseServerError()


# API getCRFModel, getDictModel, getAtrain 3 in 1
@require_POST
@csrf_exempt
def api_getTriple(request, slug):
    if request.is_ajax():
        if request.method == 'POST':
            client_id = request.POST.get('client_id', False)
            if not client_id:
                return JsonResponse({'status': 0, 'message': '系统缓存丢失, 将会自动刷新页面, 点击继续'})

            cache_api: API = cache.get(client_id, False)
            if not cache_api:
                return JsonResponse({'status': 0, 'message': '系统缓存丢失, 将会自动刷新页面, 点击继续'})

            res = 'Bad Ajax Request'
            if slug == 'CRFModel':
                res = cache_api.getCRFModel()
            if slug == 'DictModel':
                res = cache_api.getDictModel()
            if slug == 'Atrain':
                res = cache_api.getAtrain()

            return JsonResponse({'status': 1, 'message': res})
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseServerError()
