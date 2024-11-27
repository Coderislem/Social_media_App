from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import login_view,home_view,Register_view
urlpatterns = [
    path('login/',login_view.as_view(),name='login'),
    path('home/',home_view,name='home'),
    path('register/',Register_view.as_view(),name="register")

]+static(settings.MEDIA_URL,document_root = settings.MEDIA_URL)
