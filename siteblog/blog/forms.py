import re
from django.forms import ModelForm, Textarea, ValidationError, TextInput, CharField
from .models import Comment


class CommentForm(ModelForm):
    body = CharField(
            label="",
            widget=TextInput(attrs={"class":"comment", "placeholder": "Comment"})
            )
    class Meta:
        model = Comment
        fields = ['body',]

