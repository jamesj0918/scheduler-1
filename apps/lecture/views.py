from django.db.models import Q
from django_filters import rest_framework as filters

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import Lecture, LectureTime
from .serializers import LectureSerializer


class LectureFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    professor = filters.CharFilter(field_name='professor', lookup_expr='icontains')
    lecture = filters.CharFilter(field_name='lecture', method='filter_lecture')
    timetable = filters.CharFilter(field_name='timetable', method='filter_timetable')

    class Meta:
        model = Lecture
        fields = (
            'id',
            'code',
            'title',
            'point',
            'category',
            'department',
            'classroom',
            'professor',
            'lecture',
            'timetable',
        )

    def convert_time(self, time):
        hours = time[:2]
        minutes = time[2:4]
        return hours + ':' + minutes

    def filter_lecture(self, queryset, name, value):
        """
        Filter a queryset with a timetable of given lectures.
        """
        query = [int(x) for x in value.split(',')]
        result = queryset

        for uuid in query:
            times = LectureTime.objects.filter(lecture=uuid)
            for time in times:
                day = Q(timetable__day=time.day)
                start = Q(timetable__start__gte=time.start)
                end = Q(timetable__end__lte=time.end)
                result = result.exclude(day & start & end)

        return result

    def filter_timetable(self, queryset, name, value):
        """
        Filter a queryset with a timetable.
        """
        query = [x.strip() for x in value.split(',')]
        result = queryset

        for time in query:
            time = time.split(':')
            if len(time) == 1:
                # Time query only contains one argument: filters whole day.
                day = Q(timetable__day=time[0])
                result = result.exclude(day)
            elif len(time) == 2:
                # Time query only contains two arguments: filters whole timetable.
                start = Q(timetable__start__gte=self.convert_time(time[0]))
                end = Q(timetable__end__lte=self.convert_time(time[1]))
                result = result.exclude(start & end)
            else:
                # Time query contains full condition: filters with day and timetable.
                day = Q(timetable__day=time[0])
                start = Q(timetable__start__gte=self.convert_time(time[1]))
                end = Q(timetable__end__lte=self.convert_time(time[2]))
                result = result.exclude(day & start & end)

        return result


class LectureSearchAPIView(ListAPIView):
    """
    Search a lecture with URL parameters. Returns list of lectures.
    """
    serializer_class = LectureSerializer
    queryset = Lecture.objects.prefetch_related('timetable').all()
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
