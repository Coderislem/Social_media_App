from django.shortcuts import render
from .models import Post,PostImage
from .forms import PostForm,PostimgsForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
# Create your views here.

@login_required
def CreatePost_view(request):
    ImageformSet = modelformset_factory(PostImage, form=PostimgsForm, extra=3)

    if request.method == "POST":
        post_form = PostForm(data=request.POST)
        image_formset = ImageformSet(request.POST, request.FILES)

        if post_form.is_valid() and image_formset.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()

            for form in image_formset:
                if form.cleaned_data:
                    post_image = form.save(commit=False)
                    post_image.post = post
                    post_image.save()

            messages.success(request, "Post created successfully!")
        else:
            messages.error(request, "There was an error creating the post.")

    else:
        post_form = PostForm()
        image_formset = ImageformSet(queryset=PostImage.objects.none())

    return render(request, 'CreatePost.html', {"post_form": post_form, "image_formset": image_formset})
