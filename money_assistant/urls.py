from django.urls import include, path
from django.contrib import admin

from money_assistant.api import router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
]
