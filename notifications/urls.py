from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('notifications/', views.notification_list, name='notifications'),
]+static(settings.MEDIA_URL,document_root = settings.MEDIA_URL)
