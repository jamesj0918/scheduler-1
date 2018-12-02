from rest_framework import serializers

from .models import Lecture, LectureTime, Category, Subcategory, Department


class CategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='get_category_display', read_only=True)
    count = serializers.IntegerField(source='get_number_of_lectures_in_category', read_only=True)

    class Meta:
        model = Category
        fields = (
            'title',
            'count',
        )


class SubcategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='get_subcategory_display', read_only=True)
    count = serializers.IntegerField(source='get_number_of_lectures_in_subcategory', read_only=True)

    class Meta:
        model = Subcategory
        fields = (
            'title',
            'count',
        )


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


class DepartmentSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(source='get_number_of_lecture_in_department', read_only=True)

    class Meta:
        model = Department
        fields = (
            'title',
            'count',
        )
