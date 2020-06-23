from django import forms


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=225)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(required=False, widget=forms.Textarea)  # widget - type of HTML element

