from .models import Post,PostImage
from django import forms


class PostForm(forms.ModelForm):
    title = forms.CharField(label="Enter post title :")
    content = forms.Textarea()

    class Meta:
        model = Post
        fields = ["title","content"]
        

class PostimgsForm(forms.ModelForm):
    image = forms.ImageField()
    class Meta:
        model = PostImage
        fields = ["image"]