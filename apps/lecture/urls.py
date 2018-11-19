from django.urls import path

from .views import LectureListAPIView

app_name = 'lecture'
urlpatterns = [
    path('lectures/', LectureListAPIView.as_view(), name='lecture-list'),
]
