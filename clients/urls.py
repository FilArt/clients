import notifications.urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/admin/", admin.site.urls),
    path("api/users/", include("apps.users.urls")),
    path("api/calculator/", include("apps.calculator.urls")),
    path("api/bids/", include("apps.bids.urls")),
    path("api/chat/", include("apps.chat.urls")),
    path("api/info/", include("apps.info.urls")),
    path("api/logs/", include("apps.logs.urls")),
    path("api/inbox/notifications/", include(notifications.urls, namespace="notifications")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path("api/auth/", include("rest_framework.urls"))]
