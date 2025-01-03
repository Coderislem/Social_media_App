from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    create_post,
    update_post,
    delete_post,
    post_detail,
    add_like,
    Profile_posts,
    all_posts,
    post_list
)

urlpatterns = [
    # Post CRUD
    path('create/',create_post, name='create_post'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', update_post, name='update_post'),
    path('post/<int:pk>/delete/', delete_post, name='delete_post'),
    
    # Likes
    path('post/<int:pk>/like/', add_like, name='add_like'),
    
    # Lists
    path('profile/', Profile_posts, name='profile'),
    path('all/', all_posts, name='all_posts'),
    path('', post_list, name='post_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


