from django.urls import path
from .views import *

urlpatterns = [
        path('edit-profile/', user_profile_edit, name='edit_profile'),
        path('logout/', user_logout, name='logout'),
        path('login/', user_login, name='login'),
        path('register/', user_register, name='register'),
        path('password-change/', ChangePassword.as_view(), name='password_change'),
        path('activate/<uidb64>/<token>/', activate, name='activate'),
        path('password-reset/', 
             PasswordReset.as_view(), name='password_reset'),
        path('password-reset-confirm/<uidb64>/<token>/', 
             PasswordResetConfirm.as_view(), name='password_reset_confirm'),
]   



