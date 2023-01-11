from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def index(request: HttpRequest):
    return HttpResponse('<h1> Привет, мир! </h1>')
