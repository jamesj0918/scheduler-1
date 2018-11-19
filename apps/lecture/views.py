from django_filters import rest_framework as filters

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import Lecture
from .serializers import LectureSerializer


class LectureFilter(filters.FilterSet):
    timetable = filters.CharFilter(field_name='timetable', method='filter_timetable')

    class Meta:
        model = Lecture
        fields = (
            'uuid',
            'title',
            'point',
            'category',
            'department',
            'classroom',
            'professor',
            'timetable',
        )

    def filter_timetable(self, queryset, name, value):
        pass


class LectureListAPIView(ListAPIView):
    serializer_class = LectureSerializer
    queryset = Lecture.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = LectureFilter

    def list(self, request, *args, **kwargs):
        lectures = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(lectures)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(lectures, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
