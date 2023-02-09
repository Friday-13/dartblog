from django.urls import path
from .views import *

urlpatterns = [
        # path('', index, name='home'),
        path('', Home.as_view(), name='home'),
        path('category/<str:slug>/', PostByCategory.as_view(), name='category'),
        path('post/<str:slug>/', SinglePost.as_view(), name='post'),
        path('tag/<str:slug>', PostByTag.as_view(), name='tag'),
]

