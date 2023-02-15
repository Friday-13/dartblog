from django import template
from blog.models import Tag, Post

register = template.Library()

@register.inclusion_tag('blog/tag_cloud_tpl.html')
def tag_list(block_name='tags'):
    tags = Tag.objects.all()
    return {'tags': tags, 'block_name': block_name}

@register.inclusion_tag('blog/tag_cloud_tpl.html')
def tags_for_post(post: Post, block_name='tags'):
    tags = post.tags.all()
    return {'tags': tags, 'block_name': block_name}
