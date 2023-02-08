from django.shortcuts import render
from django.http import HttpRequest
from django.views.generic import DetailView, ListView
from .models import Post, Tag, Category

class Home(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    extra_context = {'title': 'Home'}
    paginate_by = 8

def index(request: HttpRequest):
    return render(request, 'blog/index.html')

def get_category(request: HttpRequest, slug: str):
    return render(request, 'blog/index.html')

def get_post(request: HttpRequest, slug: str):
    return render(request, 'blog/index.html')
