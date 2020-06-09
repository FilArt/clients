from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/cards/', include('apps.cards.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/calculator/', include('apps.calculator.urls')),
    path('api/bids/', include('apps.bids.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
