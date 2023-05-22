from django.contrib.auth.models import User
from django.http import  HttpResponseForbidden
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin

from .models import Comment, Post, Tag, Category
from users.models import User
from .forms import CommentForm 
from django.db.models import F, Q, QuerySet


class Home(ListView):
    '''
    View for main page
    '''
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 8
    allow_empty = False
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['title'] = 'Main Page'
        '''
        Get latest post as pinned
        '''
        context['pinned_post'] = Post.objects.\
                select_related('author', 'author__profile').all().latest('created_at')
        return context

    def get_queryset(self):
        return self.model.objects.select_related('author', 'author__profile')


class PostsByCategory(ListView):
    '''
    View for news from one category
    '''
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 8
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(object_list=object_list, **kwargs)
        context['category'] = Category.objects.get(slug=self.kwargs['slug'])
        context['title'] = context['category'].title
        '''
        Get pinned_post for category. 
        If pinned doesn't exist, get latest post as pinned
        '''
        pinned_post = Post.objects.filter(Q(category__slug=self.kwargs['slug']) &
                                                  Q(pinned_post=True))
        if pinned_post.exists():
            pinned_post = pinned_post.select_related('author', 'author__profile')
            context['pinned_post'] = pinned_post[0]
        else:
            context['pinned_post'] = Post.objects.\
                    select_related('author','author__profile'). \
                    filter(category__slug=self.kwargs['slug']). \
                    latest('created_at')
        return context
    
    def get_queryset(self):
        return self.model.objects.select_related('author', 'author__profile').\
                filter(category__slug=self.kwargs['slug'])


class SinglePost(FormMixin, DetailView):
    '''
    View for single post content including comment form
    '''
    model = Post
    form_class = CommentForm
    template_name = 'blog/single.html'
    context_object_name = 'post'
    slug_field = 'slug'

    def get_context_data(self, *, form=None, object_list=None, **kwargs):
        context=super().get_context_data(object_list=object_list, **kwargs)
        context['title'] = self.object.title
        # Update views counter
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()

        # Get comments
        context['comments'] = Comment.objects.select_related('user', 'user__profile').\
                                filter(Q(post=self.object) & Q(active=True))
        return context

    def get_success_url(self):
        return reverse('post', kwargs={'slug': self.object.slug})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        new_comment = form.save(commit=False)
        new_comment.post = self.get_object()
        new_comment.user = self.request.user
        new_comment.active = True
        new_comment.save()
         
        return super().form_valid(form)

class PostsByTag(ListView):
    '''
    Views for posts conataining a common tag
    '''
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 8
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['title'] = Tag.objects.get(slug=self.kwargs['slug']).title
        return context
    
    def get_queryset(self):
        return self.model.objects.select_related('author', 'author__profile').\
                filter(tags__slug=self.kwargs['slug'])


class SearchByTitle(ListView):
    '''
    View for searching result by title
    '''
    model = Post
    template_name = 'blog/search_result.html'
    context_object_name = 'posts'
    paginate_by = 8

    def get_queryset(self):
        return self.model.objects.select_related('author', 'author__profile').\
                filter(title__icontains=self.request.GET.get('s'))
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['search_by_title'] = f"s={self.request.GET.get('s')}&" 
        context['title'] = 'Search'
        return context


class PostsByUser(ListView):
    '''
    View for "profile" - user's page with his posts
    '''
    model = Post
    template_name = 'blog/profile.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['user'] = User.objects.select_related('profile').get(pk=self.kwargs['pk'])
        context['title'] = 'Profile'
        return context
    
    def get_queryset(self):
        return self.model.objects.select_related('author').\
            filter(author__pk=self.kwargs['pk'])


