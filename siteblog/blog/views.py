from django.shortcuts import render
from django.http import HttpRequest

def index(request: HttpRequest):
    return render(request, 'blog/index.html')

def get_category(request: HttpRequest, slug: str):
    return render(request, 'blog/index.html')
