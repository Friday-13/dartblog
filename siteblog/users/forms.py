from django import forms
from django.contrib.auth.admin import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import Profile

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
            label="Имя пользователя",
            widget=forms.TextInput(attrs={"class": "form-control", "id": "username", "placeholder":"Enter username"}))
    password = forms.CharField(
            label="Пароль",
            widget=forms.PasswordInput(attrs={"class": "form-control", "id": "password", "placeholder":"Enter password"})
            )

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
            label="Имя пользователя",
            widget=forms.TextInput(attrs={"class": "form-control", "id": "username", "placeholder":"Enter username"}))
    email = forms.EmailField(
            label="Email",
            widget=forms.TextInput(attrs={"class": "form-control", "id": "email", "placeholder":"Enter email"})
            )
    password1 = forms.CharField(
            label="Пароль",
            widget=forms.PasswordInput(attrs={"class": "form-control", "id": "password", "placeholder":"Enter password"})
            )
    password2 = forms.CharField(
            label="Пароль",
            widget=forms.PasswordInput(attrs={"class": "form-control", "id": "password", "placeholder":"Repeat password"})
            )
    is_subscribed = forms.BooleanField(
            label="Подписать на рассылку?",
            required=False,
            initial=True,
            widget=forms.CheckboxInput(attrs={"class": "form-control", "id": "checkbox"})
            )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_subscribed',]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class EditUserForm(forms.ModelForm):
    username = forms.CharField(
            label="User name",
            widget=forms.TextInput(attrs={"class": "form-control", "id": "username", "placeholder":"Enter username"}))
    email = forms.EmailField(
            label="Email",
            widget=forms.TextInput(attrs={"class": "form-control", "id": "email", "placeholder":"Enter email"})
            )
    class Meta:
        model = User
        fields = ['username', 'email',]

class EditProfileForm(forms.ModelForm):
    photo = forms.ImageField(
            label="User photo",
            required=False,
            widget = forms.FileInput(attrs={"class": "form-control-file", "lang": "en"})
            )
    is_subscribed = forms.BooleanField(
            label="Subscribe to news?",
            required=False,
            widget=forms.CheckboxInput(attrs={"class": "form-control", "id": "checkbox"}))

    class Meta:
        model = Profile
        fields = ['photo','is_subscribed']


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
            label="Email",
            widget=forms.TextInput(attrs={"class": "form-control", "id": "email", "placeholder":"Enter email"})
            )

class UserPasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
            label="Password",
            widget=forms.PasswordInput(attrs={"class": "form-control", "id": "password", "placeholder":"Enter password"})
            )
    new_password2 = forms.CharField(
            label="Password",
            widget=forms.PasswordInput(attrs={"class": "form-control", "id": "password", "placeholder":"Repeat password"})
            )
