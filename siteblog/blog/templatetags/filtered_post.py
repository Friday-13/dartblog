from django import template
from django.contrib.admin import register
from blog.models import Post

register = template.Library()

@register.inclusion_tag('blog/filter_tpl.html')
def actual_posts_tpl(current_category, num:int=3):
    recent_posts = Post.objects.all().order_by('-created_at', '-views')[:num]
    popular_posts = Post.objects.all().order_by('-views', '-created_at')[:num]
    category_posts = Post.objects.filter(category=current_category).order_by('-created_at', 'views')[:3]
    recent_posts.identifier = 'recent'
    popular_posts.identifier = 'popular'
    category_posts.identifier = 'category'
    return {'post_list': [recent_posts, popular_posts, category_posts]}

