from django.contrib import admin
from django.urls import path

from . import views
from .views import BeachInfraAPIView, BeachWeatherAPIView, beach_scores_api

urlpatterns = [
    path("", views.index, name="example_index"),
    # path('admin/', admin.site.urls),
    path("accident/", views.accidentApi, name="example_accident"),
    path("beach-weather/<int:beach_id>/", BeachWeatherAPIView.as_view(), name="beach_weather_api"),
    path("beach-infra/<int:beach_id>/", BeachInfraAPIView.as_view(), name="beach_infra_api"),
    path("beach-scores/<int:beach_id>/", beach_scores_api, name="beach-scores-api"),
    # path("equipment/", equipmentAPI),
    path("equipment/", views.equipmentApi, name="example_equipment"),
    path("safety/", views.safetyApi, name="example_safety"),
]
