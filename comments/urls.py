from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import post_comments, delete_comment

urlpatterns = [
    path('post/<int:post_id>/comment/', post_comments, name='post_comments'),
    path('comment/<int:comment_id>/delete/', delete_comment, name='delete_comment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)
