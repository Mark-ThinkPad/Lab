from django.shortcuts import render
from Motion.EmotionAnalysis import API


# Home Page
def index(request):
    return render(request, 'index.html')
