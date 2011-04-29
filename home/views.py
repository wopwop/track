# Create your views here.
from django.shortcuts import render_to_response, HttpResponse

def home(request):
    return render_to_response("index.html")