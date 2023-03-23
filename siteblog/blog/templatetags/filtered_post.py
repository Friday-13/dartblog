from django import template
from django.contrib.admin import register
from blog.models import Post
from django.core.cache import cache
register = template.Library()


@register.inclusion_tag('blog/filter_tpl.html')
def actual_posts_tpl(current_category, num:int=3):
    '''
    Custom tag for isotope-like filters
    return list of posts;
    num - number of posts in each filter-category;
    filter-category: recent posts, most viewed posts, 
    recent posts in current category
    '''
    recent_posts = cache.get('recent_posts')
    popular_posts = cache.get('popular_posts')
    category_posts = cache.get(f'recent_posts_in_{current_category.title}_category')
    
    # check for cache exist
    if not recent_posts:
        recent_posts = Post.objects.all().order_by('-created_at', '-views')[:num]
        recent_posts = recent_posts.select_related('author', 'author__profile')
        cache.set('recent_posts', recent_posts)
    if not popular_posts:
        popular_posts = Post.objects.all().order_by('-views', '-created_at')[:num]
        popular_posts = popular_posts.select_related('author', 'author__profile')
        cache.set('popular_posts', popular_posts)
    if not category_posts:
        category_posts = Post.objects.filter(category=current_category).order_by('-created_at', 'views')[:num]
        category_posts = category_posts.select_related('author', 'author__profile')
        cache.set(f'recent_posts_in_{current_category.title}_category', category_posts)

    recent_posts.identifier = 'recent'
    popular_posts.identifier = 'popular'
    category_posts.identifier = 'category'
    return {'post_list': [recent_posts, popular_posts, category_posts]}

