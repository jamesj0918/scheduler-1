from rest_framework import serializers

from .models import Lecture, LectureTime


class LectureTimeSerializer(serializers.ModelSerializer):
    day = serializers.CharField(source='get_day_display')

    class Meta:
        model = LectureTime
        fields = (
            'day',
            'start',
            'end',
        )


class LectureSerializer(serializers.ModelSerializer):
    timetable = LectureTimeSerializer(many=True)
    category = serializers.CharField(source='get_category_display')
    department = serializers.StringRelatedField()

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
            'timetable',
        )
