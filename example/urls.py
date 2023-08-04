from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="example_index"),
    # path('admin/', admin.site.urls),
    path("accident/", views.accidentApi, name="example_accident"),
    path("equipment/", views.equipmentApi, name="example_equipment"),
    path("safety/", views.safetyApi, name="example_safety"),
]