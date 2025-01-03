from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Like
from .forms import PostForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.db.models import Count

@login_required
def create_post(request):
    if request.method == 'POST':
        try:
            post = Post.objects.create(
                user=request.user,
                content=request.POST.get('content'),
                image=request.FILES.get('image')
            )
            return JsonResponse({'success': True})
        except Exception as e:
            print(str(e))  # Debug
            return JsonResponse({
                'success': False, 
                'error': str(e)
            })
    return JsonResponse({'success': False})

@login_required
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk, user=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/update_post.html', {'form': form})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, user=request.user)
    if request.method == 'POST':
        if post.image:
            post.image.delete()  # Delete image file
        post.delete()
        return redirect('home')
    return render(request, 'posts/delete_post.html', {'post': post})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/post_detail.html', {'post': post})

@login_required
def Profile_posts(request):
    try:
        user = User.objects.get(id=request.user.id)
    except User.DoesNotExist:
        messages.error(request, "User not found")

    posts_with_likes = Post.objects.filter(author=user).prefetch_related("likes", "images").annotate(like_count=Count("likes"))

    return render(request, "profile.html", {"posts_with_likes": posts_with_likes})

@login_required
def add_like(request, post_id):
    if request.method == 'POST':
        Like.objects.create(
            post=post_id,
            user=request.user,
        )
        messages.success(request, "add like successfully !")
    else:
        messages.error(request, "there is something wrong !")
    return {}

@login_required
def remove_post(request, post_id):
    try:
        post = get_object_or_404(Post, pk=post_id)
        post.delete()
        messages.success(request, "post remove successfully !")
    except Post.DoesNotExist:
        messages.error(request, "Post Not found ")
    except Exception as e:
        messages.error(request, f"an error :{str(e)}")
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def all_posts(request):
    Posts = Post.objects.all()
    return render(request, "posts.html", {"posts": Posts})

@login_required
def post_list(request):
    posts = Post.objects.select_related('user').prefetch_related('likes').order_by('-created_at')
    return render(request, 'post_list.html', {'posts': posts})
