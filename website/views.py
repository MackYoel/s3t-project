from django.http import HttpResponse
from django.shortcuts import render
import datetime


def home(request):
    return render(request, 'website/index.html')
