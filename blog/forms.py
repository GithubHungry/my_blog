from django import forms
from . import models


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=225)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(required=False, widget=forms.Textarea)  # widget - type of HTML element


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('name', 'email', 'body',)
