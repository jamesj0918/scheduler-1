from django.urls import path

from .views import (
    LectureSearchAPIView, LectureQueryAPIView,
    CategoryListAPIView, SubcategoryListAPIView,
    UniqueLectureListAPIView, DepartmentListAPIView,
)

app_name = 'lecture'
urlpatterns = [
    path('lectures/search/', LectureSearchAPIView.as_view(), name='lecture-search'),
    path('lectures/query/', LectureQueryAPIView.as_view(), name='lecture-query'),
    path('lectures/unique/', UniqueLectureListAPIView.as_view(), name='lecture-unique'),
    path('category/', CategoryListAPIView.as_view(), name='category-list'),
    path('subcategory/', SubcategoryListAPIView.as_view(), name='subcategory-list'),
    path('department/', DepartmentListAPIView.as_view(), name='department-list'),
]
