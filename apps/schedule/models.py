from django.db import models
from django.conf import settings

from apps.lecture.models import Lecture, LectureTime


class Schedule(models.Model):
    """
    A schedule class which represents a collection of lectures.
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lectures = models.ManyToManyField(Lecture)

    def __str__(self):
        return self.owner.username

    def get_all_lectures_in_schedule(self):
        """
        Get every lectures in schedule.
        :return: A QuerySet of every lectures.
        """
        return self.lectures.all()

    def get_number_of_lectures_in_schedule(self):
        """
        Get a number of lectures in schedule.
        :return: A number of lectures in schedule.
        """
        return self.lectures.all().count()

    get_number_of_lectures_in_schedule.short_description = 'Number of Lectures'
