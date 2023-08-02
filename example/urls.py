from . import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("", views.index, name="example_index"),
    path('admin/', admin.site.urls)
]