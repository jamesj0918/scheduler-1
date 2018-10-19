from django.db import models
from django.utils.translation import gettext as _


class Department(models.Model):
    """
    A class which represents a department of university.
    """
    title = models.CharField(_('title'), max_length=32)

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
    LECTURE_REQUIRED = 0
    LECTURE_REQUIRED_OPTIONAL = 1
    LECTURE_OPTIONAL_EXTRA = 2
    LECTURE_MAJOR_REQUIRED = 3
    LECTURE_MAJOR_OPTIONAL = 4
    LECTURE_MAJOR_EXTRA = 5

    LECTURE_TYPE = (
        (LECTURE_REQUIRED, '중핵필수'),
        (LECTURE_REQUIRED_OPTIONAL, '중핵필수선택'),
        (LECTURE_OPTIONAL_EXTRA, '자유선택교양'),
        (LECTURE_MAJOR_REQUIRED, '전공필수'),
        (LECTURE_MAJOR_OPTIONAL, '전공선택'),
        (LECTURE_MAJOR_EXTRA, '전공기초교양'),
    )

    FIELD_BASIC = 0
    FIELD_CREATIVITY = 1
    FIELD_IDEOLOGY = 2
    FIELD_CULTURE = 3
    FIELD_CONVERGENCE = 4
    FIELD_TECHNOLOGY = 5
    FIELD_EARTH = 6
    FIELD_SCIENCE = 7
    FIELD_MORALITY = 8
    FIELD_HISTORY = 9
    FIELD_LAW = 10
    FIELD_ART = 11
    FIELD_WORLDWIDE = 12
    FIELD_ENHANCING = 13

    FIELD_TYPE = (
        (FIELD_BASIC, '학문기초'),
        (FIELD_CREATIVITY, '인성과창의력'),
        (FIELD_IDEOLOGY, '사상과역사'),
        (FIELD_CULTURE, '사회와문화'),
        (FIELD_CONVERGENCE, '융합과창업'),
        (FIELD_TECHNOLOGY, '자연과과학기술'),
        (FIELD_EARTH, '세계와지구촌'),
        (FIELD_SCIENCE, '생명과 과학'),
        (FIELD_MORALITY, '인성과도덕'),
        (FIELD_HISTORY, '역사와문화'),
        (FIELD_LAW, '사회와제도'),
        (FIELD_ART, '예술과생활'),
        (FIELD_WORLDWIDE, '지구촌의이해'),
        (FIELD_ENHANCING, '역량강화'),
    )

    LANGUAGE_KOR = 0
    LANGUAGE_ENG = 1

    LANGUAGE_TYPE = (
        (LANGUAGE_KOR, '한국어'),
        (LANGUAGE_ENG, '영어'),
    )

    uuid = models.CharField(_('lecture id'), max_length=16)
    division = models.IntegerField(_('division'), default=1)
    title = models.CharField(_('title'), max_length=64)
    type = models.IntegerField(_('lecture type'), choices=LECTURE_TYPE, default=LECTURE_REQUIRED)
    field = models.IntegerField(_('lecture field'), choices=FIELD_TYPE, default=FIELD_BASIC)
    grade = models.FloatField(_('grade point'), default=1)
    language = models.IntegerField(_('language'), choices=LANGUAGE_TYPE, default=LANGUAGE_KOR)

    department = models.ForeignKey(
        Department, verbose_name=_('department'), on_delete=models.CASCADE, related_name='lectures')
    target_department = models.ForeignKey(
        Department, verbose_name=_('target department'), on_delete=models.CASCADE, related_name='target_lectures')
    origin_department = models.ForeignKey(
        Department, verbose_name=_('origin department'), on_delete=models.CASCADE, related_name='origin_lectures')

    classroom = models.CharField(_('classroom'), max_length=16)
    professor = models.CharField(_('professor'), max_length=32)

    def __str__(self):
        return self.title


class LectureTime(models.Model):
    """
    A class which represents a time of the lecture.
    """
    TIME_MONDAY = 0
    TIME_TUESDAY = 1
    TIME_WEDNESDAY = 2
    TIME_THURSDAY = 3
    TIME_FRIDAY = 4

    TIME_DAYS = (
        (TIME_MONDAY, '월요일'),
        (TIME_TUESDAY, '화요일'),
        (TIME_WEDNESDAY, '수요일'),
        (TIME_THURSDAY, '목요일'),
        (TIME_FRIDAY, '금요일'),
    )

    day = models.IntegerField(choices=TIME_DAYS, default=TIME_MONDAY)
    start_time = models.TimeField()
    end_time = models.TimeField()
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
