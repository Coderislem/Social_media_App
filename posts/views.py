from django.shortcuts import render,redirect
from .models import Post,PostImage,Like
from .forms import PostForm,PostimgsForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db.models import Count
from django.shortcuts import get_object_or_404
# Create your views here.

@login_required
def CreatePost_view(request):
    ImageformSet = modelformset_factory(PostImage, form=PostimgsForm, extra=3)

    if request.method == "POST":
        post_form = PostForm(data=request.POST) 
        image_formset = ImageformSet(request.POST, request.FILES)
        print(post_form)
        print(image_formset)

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
            if not image_formset.is_valid():
                print(image_formset.errors)
            if not post_form.is_valid():
                print(post_form.errors)
            messages.error(request, "There was an error creating the post.")

    else:
        post_form = PostForm()
        image_formset = ImageformSet(queryset=PostImage.objects.none())

    return render(request, 'CreatePost.html', {"post_form": post_form, "image_formset": image_formset})


@login_required
def Profile_posts(request):
    try:
        user = User.objects.get(id = request.user.id)
    except User.DoesNotExist:
        messages.error(request,"User not found")
    
    
    posts_with_likes = Post.objects.filter(author = user).prefetch_related("likes").annotate(like_count = Count("likes"))

    return render(request,"profile.html",{"posts_with_likes":posts_with_likes})
@login_required
def add_like(request,post_id):
    
    if request.method =='POST':
        Like.objects.create(
            post = post_id,
            user = request.user,
        )
        messages.success(request,"add like successfully !")
    else:
        messages.error(request,"there is something wrong !")
    return {}

@login_required
def post_details(request,post_id):
    post = Post.objects.get(id = post_id)
    return render (request,"post.html",{"post":post})
@login_required
def remove_post(request,post_id):
    try:
        post = get_object_or_404(Post,pk = post_id)
        post.delete()
        messages.success(request,"post remove successfully !")
    except Post.DoesNotExist:
        messages.error(request,"Post Not found ")
    except Exception as e:
        messages.error(request,f"an error :{str(e)}")
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def edit_post(request,post_id):
    try:
        post = get_object_or_404(Post,pk=post_id)
    except Post.DoesNotExist:
        messages.error(request,"Post not found ")
    if request.method =="POST":
        post_form = PostForm(data=request.POST or None,instance=post)
        images_form = PostImage(request.POST or None,request.FILES or None)
        if form.is_valid() and images_form.is_valid():
            post_form.save()
            if 'image' in request.FILES:
                images_post = images_form.save(commit=False)
                images_post.post = post
                images_post.save()
                

            messages.success(request,"Post updated successfully !")
            return redirect('post_details',post_id = post.id)
        else:
            messages.error(request,"invalid information ")
    else:
        form = PostForm(instance=post)
    return render(request,"edit-post.html",{"post_form":post_form,"images_form":images_form})


