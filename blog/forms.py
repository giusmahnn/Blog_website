from django import forms
from .models import Post, Comment

class PostCreateForm(forms.ModelForm):
    class Meta:
        model= Post
        fields = ['title', 'body', 'featured_image', 'categories', 'tags']


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

class LikeForm(forms.Form):
    like = forms.CharField(max_length=100)