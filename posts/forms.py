from .models import Post
from django import forms


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
        

# class PostimgsForm(forms.ModelForm):
#     image = forms.ImageField()
#     class Meta:
#         model = PostImage
#         fields = ["image"]
