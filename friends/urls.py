from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import profiles_view,add_friend,FreindRequestSuggestions
urlpatterns = [
    path('profiles/',FreindRequestSuggestions,name="profiles"),
    path('add-friend/<int:reciver_id>/',add_friend,name="add-friend")
]+static(settings.MEDIA_URL,document_root = settings.MEDIA_URL)
