# from . import views
# from django.urls import path

# urlpatterns = [
#     path("", views.index, name="example_index")
# ]

from django.urls import path
from .views import map_markers

urlpatterns = [
    path('api/markers/', map_markers, name='map_markers'),
    # 다른 URL 패턴들을 추가할 수 있습니다.
]