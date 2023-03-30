from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import  HttpResponseForbidden
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin
from django.contrib import messages

from django.conf import settings
from .models import Comment, Post, Tag, Category
from .forms import CommentForm, EditProfileForm, EditUserForm, UserLoginForm, UserRegisterForm
from django.db.models import F, Q
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from .tokens import account_activation_token
from django.core.mail import EmailMessage

class Home(ListView):
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
        print(form.cleaned_data)
        new_comment = form.save(commit=False)
        new_comment.post = self.get_object()
        new_comment.user = self.request.user
        new_comment.save()
         
        return super().form_valid(form)

class PostsByTag(ListView):
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


def user_logout(request: HttpRequest):
    logout(request)
    return HttpResponseRedirect(request.POST.get('next', '/'))


def user_login(request: HttpRequest):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You have successfully logged in!')
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'blog/login.html', {'form': form, 'title': 'Login'})


def user_register(request: HttpRequest):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activate_email(request, user, form.cleaned_data.get('email'))
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form, 'title': 'Register', 'formtitle': 'Register form'})


def user_profile_edit(request: HttpRequest):
    if request.method == 'POST':
        user_form = EditUserForm(data=request.POST, instance=request.user)
        profile_form = EditProfileForm(data=request.POST, files=request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('home')
    else:
        user_form = EditUserForm(instance=request.user)
        profile_form = EditProfileForm(instance=request.user.profile)
    return render(request, 'blog/edit_profile.html', 
                  {'user_form': user_form, 'profile_form': profile_form,
                   'title': 'Edit'})

def activate_email(request, user, to_email):
    mail_subject = 'Activate your account'
    message = render_to_string('blog/activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, from_email=settings.EMAIL_HOST_USER, to=[to_email])
    print(email.from_email)
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')

class ChangePassword(PasswordChangeView):
    template_name = 'blog/change_password.html'
    success_url = reverse_lazy('home')

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
    return redirect('home')

