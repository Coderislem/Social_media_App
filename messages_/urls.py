from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('conv_list/', views.conversations_list, name='conversations_list'),
    path('new/', views.new_conversation, name='new_conversation'),
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('<int:conversation_id>/send/', views.send_message, name='send_message'),
    path('friends/', views.friends_messages, name='friends_messages'),
    path('start/<int:friend_id>/', views.start_conversation, name='start_conversation'),
]+static(settings.MEDIA_URL,document_root = settings.MEDIA_URL)
