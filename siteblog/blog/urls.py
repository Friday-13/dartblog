from django.urls import path
from .views import *

urlpatterns = [
        path('', Home.as_view(), name='home'),
        path('category/<str:slug>/', PostsByCategory.as_view(), name='category'),
        path('post/<str:slug>/', SinglePost.as_view(), name='post'),
        path('tag/<str:slug>/', PostsByTag.as_view(), name='tag'),
        path('search/', SearchByTitle.as_view(), name='search'),
        path('profile/<int:pk>/', PostsByUser.as_view(), name='profile'),
]   


