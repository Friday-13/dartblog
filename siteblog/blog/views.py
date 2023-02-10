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


class PostsByCategory(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context
    
    def get_queryset(self):
        return self.model.objects.filter(category__slug=self.kwargs['slug'])


class SinglePost(DetailView):
    model = Post
    template_name = 'blog/single.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context

class PostsByTag(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 8
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Tag.objects.get(slug=self.kwargs['slug']).title
        return context
    
    def get_queryset(self):
        return self.model.objects.filter(tags__slug=self.kwargs['slug'])

    

def index(request: HttpRequest):
    return render(request, 'blog/index.html')

def get_category(request: HttpRequest, slug: str):
    return render(request, 'blog/index.html')

def get_post(request: HttpRequest, slug: str):
    return render(request, 'blog/index.html')
