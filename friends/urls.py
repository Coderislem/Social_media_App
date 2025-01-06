from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import( profiles_view,add_friend,
FreindRequestSuggestions,
Friends,
remove_friend,
people_list,
user_profile,
accept_friend_request,
reject_friend_request,
my_profile
)
urlpatterns = [
    path('profiles/',FreindRequestSuggestions,name="profiles"),
    path('add-friend/<int:reciver_id>/',add_friend,name="send_friend_request"),
    path('friends',Friends,name="friends"),
    path('remove/<int:id>/',remove_friend,name="remove"),
    path('people/',people_list, name='people_list'),
    path('profile/<str:username>/', user_profile, name='user_profile'),
    path('friend-request/<int:request_id>/accept/', accept_friend_request, name='accept_friend_request'),
    path('friend-request/<int:request_id>/reject/', reject_friend_request, name='reject_friend_request'),
    path('my_profile/',my_profile,name="my_profile")
]+static(settings.MEDIA_URL,document_root = settings.MEDIA_URL)
