from django.contrib import admin
from django.urls import path

from . import views
from .views import equipmentAPI

urlpatterns = [
    path("", views.index, name="example_index"),
    path("admin/", admin.site.urls),
    path("equipment/", equipmentAPI),
]
