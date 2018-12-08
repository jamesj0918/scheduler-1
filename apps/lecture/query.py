import itertools
from datetime import time

from django.db.models import Q

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import Lecture, LectureTime
from .serializers import LectureSerializer


def convert_day(day):
    days = {
        'mon': 0,
        'tue': 1,
        'wed': 2,
        'thu': 3,
        'fri': 4
    }
    return days[day]


def convert_time(source):
    hour = int(source[:2])
    minute = int(source[2:])
    return time(hour=hour, minute=minute)


def generate_time_filter(start, end):
    return Q(timetable__start__lt=end) & Q(timetable__end__gt=start)


class LectureQueryAPIView(ListAPIView):
    serializer_class = LectureSerializer
    queryset = Lecture.objects.all()

    def get_available_lectures(self, queryset):
        # Returns every lectures that are available (i.e., not filtered with timetables, other lectures).
        # For example, if your selected lecture codes were 100 and 105, then this function would calculate
        # every lectures that has code of 100 (or 105) that are filtered, and returns the combinations of it.
        timetables = self.request.GET.get('timetable', None)
        fixed_lectures = self.request.GET.get('fixed', None)
        selected_lectures = self.request.GET.get('selected', None)
        result = []

        print('before start: ' + str(queryset.count()))

        # Step 1: Exclude queryset with the given timetables.
        if timetables is not None:
            timetables = [timetable.strip() for timetable in timetables.split(',')]
            for timetable in timetables:
                timetable = timetable.split(':')
                if len(timetable) == 1:
                    queryset = queryset.exclude(~Q(timetable__day=convert_day(timetable[0])))
                if len(timetable) == 2:
                    queryset = queryset.exclude(
                        generate_time_filter(convert_time(timetable[0]), convert_time(timetable[1])))
                if len(timetable) == 3:
                    queryset = queryset.exclude(Q(timetable__day=convert_day(timetable[0])) &
                        generate_time_filter(convert_time(timetable[1]), convert_time(timetable[2])))

        print(queryset.filter(id=1606).exists())
        print('after timetable: ' + str(queryset.count()))

        # Step 2: Exclude queryset with the given fixed lectures.
        fixed = []
        if fixed_lectures is not None:
            fixed = [int(fix) for fix in fixed_lectures.split(',')]
            for fix in fixed:
                for timetable in LectureTime.objects.filter(lecture=fix).iterator():
                    queryset = queryset.exclude(
                        Q(timetable__day=timetable.day) & generate_time_filter(timetable.start, timetable.end))

        print(queryset.filter(id=1606).exists())
        print('after fixed lectures: ' + str(queryset.count()))

        # Step 3: Filter queryset with the given selected lectures.
        combinations = []
        if selected_lectures is not None:
            selected_lectures = [code.strip() for code in selected_lectures.split(',')]
            queryset = queryset.filter(code__in=selected_lectures)
            for selected in selected_lectures:
                combinations.append(list(queryset.filter(code=selected)))

        print(queryset.filter(id=1606).exists())
        print('after selected lectures: ' + str(queryset.count()))

        # Step 4: Generate combinations with the result queryset.
        combinations = list(itertools.product(*combinations))
        for scenario in combinations:
            timetables = LectureTime.objects.filter(lecture__in=scenario)
            overlap = False
            for timetable in timetables.iterator():
                # Check if there is any overlapping lectures in the timetable query.
                checker = timetables.filter(
                    Q(day=timetable.day) & (Q(start__lt=timetable.end) & Q(end__gt=timetable.start)))
                if checker.count() >= 2:
                    overlap = True
                    break
            # Only add the non-overlapping lectures.
            if not overlap:
                result.append(list(scenario))

        # Append list with the fixed lectures.
        fixed = list(Lecture.objects.filter(pk__in=fixed))
        result = [lectures + fixed for lectures in result]

        print('final combinations: ' + str(len(result)))
        return result

    def list(self, request, *args, **kwargs):
        lectures = self.get_available_lectures(self.get_queryset())

        serializer_list = []
        for scenario in lectures:
            sublist = []
            for lecture in scenario:
                serializer = self.get_serializer(lecture)
                sublist.append(serializer.data)
            serializer_list.append(sublist)

        return Response(serializer_list, status=status.HTTP_200_OK)
