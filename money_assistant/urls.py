from django.urls import include, path
from django.contrib import admin

from money_assistant.api import router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
    path("ht/", include("health_check.urls")),
    path("django-rq/", include("django_rq.urls")),
]
