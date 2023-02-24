import re
from django.forms import ModelForm, Textarea, ValidationError
from .models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body',]

    def clean_body(self):
        body = self.cleaned_data['body']
        if re.match(r'\d', body):
            raise ValidationError('не с цифры!')
        return body
