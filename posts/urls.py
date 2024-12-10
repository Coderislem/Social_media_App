from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import CreatePost_view,Profile_posts
urlpatterns = [
    path('new/',CreatePost_view,name="new_post"),
    path('profile',Profile_posts,name="profile")
]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
