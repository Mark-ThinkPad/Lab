from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
# from Motion.EmotionAnalysis.API import API
import hashlib


# Functions
def set_client_id(request) -> str:
    client_addr = request.META.get('REMOTE_ADDR', 'anonymous')
    client_host = request.META.get('REMOTE_HOST', 'unknown hostname')
    id_source = client_addr + ', ' + client_host
    # 进行md5加密
    m = hashlib.md5()
    m.update(id_source.encode(encoding='utf-8'))
    return m.hexdigest()

# Home Page
@require_GET
def index(request):
    client_id = request.COOKIES.get('client_id', False)
    response = render(request, 'index.html', {'id': client_id})
    if not client_id:
        response.set_cookie('client_id', set_client_id(request))
    return response
