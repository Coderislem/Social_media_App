
from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('accounts.urls')),
    path('post/', include('posts.urls')),
    path('labery/', include('Books.urls')),
    path('friends/',include('friends.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
