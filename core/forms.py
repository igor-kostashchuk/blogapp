from django import forms
from .models import BlogEntry, Comment

class BlogEntryForm(forms.ModelForm):
    class Meta:
        model = BlogEntry
        fields = ["title", "category", "content"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'stars']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a comment...'}),
            'stars': forms.HiddenInput(attrs={'min': 1, 'max': 5, 'placeholder': '1-5 Stars'}),
        }