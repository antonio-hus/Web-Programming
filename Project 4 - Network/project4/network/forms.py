# Imports Section
from django import forms


# New Post Forum
class PostForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), label='')
