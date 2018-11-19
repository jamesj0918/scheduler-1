from django.urls import path

from .views import LectureSearchAPIView

app_name = 'lecture'
urlpatterns = [
    path('lectures/', LectureSearchAPIView.as_view(), name='lecture-search'),
]
