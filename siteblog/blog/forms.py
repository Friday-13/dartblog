import re
from ckeditor import widgets
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from .models import Comment


class CommentForm(forms.ModelForm):
    body = forms.CharField(
            label="",
            widget=forms.TextInput(attrs={"class":"comment", "placeholder": "Comment"})
            )
    class Meta:
        model = Comment
        fields = ['body',]


