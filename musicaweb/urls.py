from django.contrib import admin
from django.urls import path, include

# 👇 añade estas dos líneas
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('music.urls')),
]

# 👇 sirve archivos de /media solo en DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
