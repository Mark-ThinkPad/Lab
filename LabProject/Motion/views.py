from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from Motion.EmotionAnalysis.API import API


# Home Page
@require_GET
def index(request):
    return render(request, 'index.html')
