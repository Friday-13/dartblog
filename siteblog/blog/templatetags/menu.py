from django import template
from django.contrib.admin import register
from blog.models import Category

register = template.Library()

@register.inclusion_tag('blog/menu_tpl.html')
def show_menu(menu_class:str='menu'):
    categories = Category.objects.all()
    return {'categories': categories, 'menu_class': menu_class}
    
