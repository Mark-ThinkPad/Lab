from django.shortcuts import render
from Motion.EmotionAnalysis.API import *


# Home Page
def index(request):
    return render(request, 'index.html')
