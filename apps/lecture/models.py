from django.db import models


class Department(models.Model):
    title = models.CharField(max_length=32)

    def __str__(self):
        return self.title

    def get_number_of_lectures_in_department(self):
        """
        Get a number of lectures in given department.
        :return: A number of every lectures in department.
        """
        return Lecture.objects.filter(department=self).count()

    get_number_of_lectures_in_department.short_description = 'Lectures in Department'


class Lecture(models.Model):
    """
    A class which represents a model of lecture.
    """
    LECTURE_REQUIRED = 1
    LECTURE_OPTIONAL = 2
    LECTURE_EXTRA = 3

    LECTURE_TYPE = (
        (LECTURE_REQUIRED, '전필'),
        (LECTURE_OPTIONAL, '전선'),
        (LECTURE_EXTRA, '교양'),
    )

    lecture_id = models.CharField(max_length=16)
    title = models.CharField(max_length=64)
    type = models.IntegerField(choices=LECTURE_TYPE, default=LECTURE_REQUIRED)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    professor = models.CharField(max_length=64)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.title

    @staticmethod
    def get_all_lectures():
        """
        Get every lectures that are instantiated.
        :return: A QuerySet of every lectures.
        """
        return Lecture.objects.all()

    @staticmethod
    def get_lectures_with_id(lecture_id):
        """
        Get every lectures with the same id.
        :param lecture_id: An id of lecture.
        :return: A QuerySet of lectures.
        """
        return Lecture.objects.filter(lecture_id=lecture_id)
