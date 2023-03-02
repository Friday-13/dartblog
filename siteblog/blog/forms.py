import re
from ckeditor import widgets
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Comment, Profile


class CommentForm(forms.ModelForm):
    body = forms.CharField(
            label="",
            widget=forms.TextInput(attrs={"class":"comment", "placeholder": "Comment"})
            )
    class Meta:
        model = Comment
        fields = ['body',]


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
            label="Имя пользователя",
            widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(
            label="Пароль",
            widget=forms.PasswordInput(attrs={"class":"form-control"})
            )

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
            label="Email",
            widget=forms.TextInput(attrs={"class": "form-control"})
            )
    is_subscribed = forms.BooleanField(
            label="Подписать на рассылку?",
            required=False,
            initial=True,
            widget=forms.CheckboxInput(attrs={"class": "form-control"})
            )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_subscribed',]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        profile = Profile()
        profile.user = user
        profile.is_subscribed = self.cleaned_data['is_subscribed']
        if commit:
            user.save()
            profile.save()
        return user
