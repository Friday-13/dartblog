from django.urls import path
from .views import *

urlpatterns = [
        path('', Home.as_view(), name='home'),
        path('category/<str:slug>/', PostsByCategory.as_view(), name='category'),
        path('post/<str:slug>/', SinglePost.as_view(), name='post'),
        path('tag/<str:slug>/', PostsByTag.as_view(), name='tag'),
        path('search/', SearchByTitle.as_view(), name='search'),
        path('profile/<int:pk>/', PostsByUser.as_view(), name='profile'),
        # path('edit-profile/', user_profile_edit, name='edit_profile'),
        # path('logout/', user_logout, name='logout'),
        # path('login/', user_login, name='login'),
        # path('register/', user_register, name='register'),
        # path('password-change/', ChangePassword.as_view(), name='password_change'),
        # path('activate/<uidb64>/<token>/', activate, name='activate'),
        # path('password-reset/', 
             # PasswordReset.as_view(), name='password_reset'),
        # path('password-reset-confirm/<uidb64>/<token>/', 
             # PasswordResetConfirm.as_view(), name='password_reset_confirm'),
]   


