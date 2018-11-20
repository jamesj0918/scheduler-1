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
    category = serializers.StringRelatedField(many=True)
    subcategory = serializers.StringRelatedField(many=True)
    department = serializers.StringRelatedField()

    class Meta:
        model = Lecture
        fields = (
            'id',
            'code',
            'division',
            'title',
            'point',
            'category',
            'subcategory',
            'department',
            'classroom',
            'professor',
            'timetable',
        )
