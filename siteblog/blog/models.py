from enum import unique
from django.db import models

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
    '''
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)

    def __str__(self):
        return self.title

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
    author = models.CharField(max_length=100, verbose_name='Автор')
    content = models.TextField(blank=True, verbose_name='Содержание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Файл обложки')
    views = models.IntegerField(default=0, verbose_name='Кол-во просмотров')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, 
                                 related_name='posts', verbose_name='Категория')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts', verbose_name='Теги')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']
