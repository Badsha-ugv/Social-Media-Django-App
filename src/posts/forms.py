from django import forms 
from . models import Post,Comment

class PostForm(forms.ModelForm):
    class Meta: 
        model = Post 
        fields = ('content', 'image')


class CommentForm(forms.ModelForm):
    body = forms.CharField( label='', widget=forms.Textarea(attrs={'rows': '1'}))
    class Meta: 
        model = Comment 
        fields = ('body',) 