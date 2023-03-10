from enum import unique
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

'''
Models fields list
Category:
    title, slug

Tag:
    title, slug

Post:
    title, slug, author, content, created_at, photo, views, category, tags
'''

class Category(models.Model):
    '''
    Category of post. 
    One post can be belong to only one category
    title - title of category
    slug - url of category
    photo - background image of cetegory
    tagline - short tagline for category: quote, though - anything
    short_description - short text with description of category
    '''
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)
    photo = models.ImageField(upload_to='backgrounds/%Y/%m/%d/', blank=True,
                              verbose_name='Фон')
    tagline = models.CharField(max_length=100, blank=True, verbose_name='Слоган')
    short_description = models.TextField(blank=True, verbose_name='Описание')
    

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('category', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class Tag(models.Model):
    '''
    Tag of post.
    Every post can have one or more tags
    title - title of category
    slug - url of category
    '''
    title = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(max_length=50, verbose_name='Url', unique=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('tag', kwargs={'slug':self.slug})

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['title']


class Post(models.Model):
    '''
    Post in the blog.
    title - title of the post
    slug - url
    author - post author
    content - text of the post
    created_at - date and time of creation
    photo - cover(image) of post
    views - views counter
    category - category of post from Category
    tags - tags of post from Tag
    '''
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                               related_name='posts', verbose_name='Автор')
    content = models.TextField(blank=True, verbose_name='Содержание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Файл обложки')
    views = models.IntegerField(default=0, verbose_name='Кол-во просмотров')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, 
                                 related_name='posts', verbose_name='Категория')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts', verbose_name='Теги')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано?')
    pinned_post = models.BooleanField(default=False, verbose_name='Закрепить пост')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post', kwargs={'slug':self.slug})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']

class Profile(models.Model):
    '''
    user - link to standard User model
    photo - profile photo of user
    subscribed - if user subscribed to news
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users_photo/%Y/%m/%d/', blank=True, verbose_name='Фото')
    is_subscribed = models.BooleanField(default=True, verbose_name='В рассылке')
    
    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk':self.user.pk})

    

class Comment(models.Model):
    '''
    post - link to Post model. Post for this comment
    user - comment author
    body - text of comment
    created_at - time and date of creation
    active - allow to show the comment
    '''
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment {self.body} Author {self.user}'
