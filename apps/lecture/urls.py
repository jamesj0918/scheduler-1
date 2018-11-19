from django.urls import path

from .views import LectureSearchAPIView, LectureQueryAPIView

app_name = 'lecture'
urlpatterns = [
    path('lectures/search/', LectureSearchAPIView.as_view(), name='lecture-search'),
    path('lectures/query/', LectureQueryAPIView.as_view(), name='lecture-query'),
]
