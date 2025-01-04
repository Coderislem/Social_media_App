from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Comment
from django.http import JsonResponse
from posts.models import Post

# Create your views here.
@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get('content')
        
        if content:
            Comment.objects.create(
                user=request.user,
                post=post,
                content=content
            )
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def post_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                user=request.user,
                post=post,
                content=content
            )
            return redirect('post_comments', post_id=post_id)
            
    comments = post.comments.select_related('user').order_by('-created_at')
    return render(request, 'comments.html', {
        'post': post,
        'comments': comments
    })

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check if user owns the comment
    if request.user == comment.user:
        comment.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)