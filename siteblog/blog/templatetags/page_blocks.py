from django import template
from django.contrib.admin import register


register = template.Library()

@register.inclusion_tag('blog/page_cover_tpl.html')
def page_cover(header:str='', description:str='', photo_url:str='/static/img/bg-iamges.jpg'):
    return {'header': header, 'description': description, 'photo': photo_url}

