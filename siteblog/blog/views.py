from django.shortcuts import render
from django.http import HttpRequest
from django.views.generic import DetailView, ListView
from .models import Post, Tag, Category
from django.db.models import F, Q

class Home(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 8
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['title'] = 'Home'
        '''
        Get latest post as pinned
        '''
        context['pinned_post'] = Post.objects.all().latest('created_at')
        return context

class PostsByCategory(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 8
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(object_list=object_list, **kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        '''
        Get pinned_post for category. 
        If pinned doesn't exist, get latest post as pinned
        '''
        pinned_post = Post.objects.filter(Q(category__slug=self.kwargs['slug']) &
                                                  Q(pinned_post=True))
        if pinned_post.exists():
            context['pinned_post'] = pinned_post[0]
        else:
            context['pinned_post'] = Post.objects.filter(
                    category__slug=self.kwargs['slug']).latest('created_at')
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
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context


class PostsByTag(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 8
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['title'] = Tag.objects.get(slug=self.kwargs['slug']).title
        return context
    
    def get_queryset(self):
        return self.model.objects.filter(tags__slug=self.kwargs['slug'])

class SearchByTitle(ListView):
    model = Post
    template_name = 'blog/search_result.html'
    context_object_name = 'posts'
    paginate_by = 8

    def get_queryset(self):
        return self.model.objects.filter(title__icontains=self.request.GET.get('s'))
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['search_by_title'] = f"s={self.request.GET.get('s')}&" 
        context['title'] = 'Search'
        return context

