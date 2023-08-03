from django.contrib import admin
from django.urls import path

from . import views
from .views import add_equipment, randomAPI

urlpatterns = [
    path("", views.index, name="example_index"),
    path("admin/", admin.site.urls),
    # path('save_csv_data/', views.save_csv_data_to_db, name='save_csv_data'),
    path("equipment/", add_equipment),
    path("random/", randomAPI),
]
