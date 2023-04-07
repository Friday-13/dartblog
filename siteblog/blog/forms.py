from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    body = forms.CharField(
            label="",
            widget=forms.TextInput(attrs={"class":"comment", "placeholder": "Comment"})
            )
    class Meta:
        model = Comment
        fields = ['body',]


