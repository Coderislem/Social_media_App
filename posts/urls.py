from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import CreatePost_view,Profile_posts,add_like,edit_post,all_posts,remove_post
urlpatterns = [
    path('new/',CreatePost_view,name="new_post"),
    path('profile/',Profile_posts,name="profile"),
    path("edit/<int:post_id>/",edit_post,name="edit_post"),
    path("delete/<int:post_id>/",remove_post,name="delete_post"),
    path("all/",all_posts,name="all_posts")
]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
