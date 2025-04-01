from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("bakary_village.urls")),
    path("bakary/", include("bakary_village.urls")),
]
