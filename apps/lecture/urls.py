from django.urls import path

from .views import (
    LectureSearchAPIView, LectureQueryAPIView,
    CategoryListAPIView, SubcategoryListAPIView,
)

app_name = 'lecture'
urlpatterns = [
    path('lectures/search/', LectureSearchAPIView.as_view(), name='lecture-search'),
    path('lectures/query/', LectureQueryAPIView.as_view(), name='lecture-query'),
    path('lectures/category/', CategoryListAPIView.as_view(), name='category-list'),
    path('lectures/subcategory/', SubcategoryListAPIView.as_view(), name='subcategory-list'),
]
