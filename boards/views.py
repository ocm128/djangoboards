from django.shortcuts import render
from django.http import HttpResponse

from boards import views


def home(request):
    return HttpResponse('Hello, World!')

# Create your views here.
