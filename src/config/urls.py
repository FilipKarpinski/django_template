from django.conf import settings
from django.contrib import admin
from django.urls import path

from apps.demo.views import index as demo_index
from config.health import health_check

urlpatterns = [
    path("health/", health_check),
    path("admin/", admin.site.urls),
    path("", demo_index),
]


if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls
    from django.conf.urls.static import static

    urlpatterns += debug_toolbar_urls()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
