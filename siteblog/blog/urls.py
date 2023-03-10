from django.urls import path
from .views import *

urlpatterns = [
        # path('', index, name='home'),
        path('', Home.as_view(), name='home'),
        path('category/<str:slug>/', PostsByCategory.as_view(), name='category'),
        path('post/<str:slug>/', SinglePost.as_view(), name='post'),
        path('tag/<str:slug>/', PostsByTag.as_view(), name='tag'),
        path('search/', SearchByTitle.as_view(), name='search'),
        path('profile/<int:pk>/', PostsByUser.as_view(), name='profile'),
        path('edit-profile/', user_profile_edit, name='edit_profile'),
        path('logout/', user_logout, name='logout'),
        path('login/', user_login, name='login'),
        path('register/', user_register, name='register'),
]

