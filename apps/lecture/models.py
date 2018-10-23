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

    LECTURE_TYPE = {
        '중핵필수': LECTURE_REQUIRED,
        '중핵필수선택': LECTURE_MAJOR_OPTIONAL,
        '자유선택교양': LECTURE_OPTIONAL_EXTRA,
        '전공필수': LECTURE_MAJOR_REQUIRED,
        '전공선택': LECTURE_MAJOR_OPTIONAL,
        '전공기초교양': LECTURE_MAJOR_EXTRA,
    }

    LECTURE_CHOICE_SET = []
    for lecture_choice in LECTURE_TYPE.items():
        LECTURE_CHOICE_SET.append((lecture_choice[1], lecture_choice[0]))

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

    FIELD_TYPE = {
        '학문기초': FIELD_BASIC,
        '인성과창의력': FIELD_CREATIVITY,
        '사상과역사': FIELD_IDEOLOGY,
        '사회와문화': FIELD_CULTURE,
        '융합과창업': FIELD_CONVERGENCE,
        '자연과과학기술': FIELD_TECHNOLOGY,
        '세계와지구촌': FIELD_EARTH,
        '생명과 과학': FIELD_SCIENCE,
        '인성과도덕': FIELD_MORALITY,
        '역사와문화': FIELD_HISTORY,
        '사회와제도': FIELD_LAW,
        '예술과생활': FIELD_ART,
        '지구촌의이해': FIELD_WORLDWIDE,
        '역량강화': FIELD_ENHANCING,
    }

    FIELD_CHOICE_SET = []
    for field_choice in FIELD_TYPE.items():
        FIELD_CHOICE_SET.append((field_choice[1], field_choice[0]))

    LANGUAGE_KOR = 0
    LANGUAGE_ENG = 1
    LANGUAGE_ENGKOR = 2

    LANGUAGE_TYPE = {
        '한국어': LANGUAGE_KOR,
        '영어': LANGUAGE_ENG,
        '영어/한국어': LANGUAGE_ENGKOR,
    }

    LANGUAGE_CHOICE_SET = []
    for lang_choice in LANGUAGE_TYPE.items():
        LANGUAGE_CHOICE_SET.append((lang_choice[1], lang_choice[0]))

    uuid = models.CharField(_('lecture id'), max_length=16)
    division = models.CharField(_('division'), max_length=8, default=1)
    title = models.CharField(_('title'), max_length=64)
    type = models.IntegerField(_('lecture type'),
                               null=True, blank=True, choices=LECTURE_CHOICE_SET, default=LECTURE_REQUIRED)
    field = models.IntegerField(_('lecture field'),
                                null=True, blank=True, choices=FIELD_CHOICE_SET, default=FIELD_BASIC)
    grade = models.IntegerField(_('grade'), default=1, null=True, blank=True)
    point = models.FloatField(_('point'), default=1.0, null=True, blank=True)
    language = models.IntegerField(_('language'),
                                   null=True, blank=True, choices=LANGUAGE_CHOICE_SET, default=LANGUAGE_KOR)

    department = models.ForeignKey(
        Department, verbose_name=_('department'), on_delete=models.CASCADE, related_name='lectures')
    # target_department = models.ForeignKey(
    #     Department, verbose_name=_('target department'), on_delete=models.CASCADE, related_name='target_lectures')
    origin_department = models.ForeignKey(
        Department, verbose_name=_('origin department'), on_delete=models.CASCADE, related_name='origin_lectures')

    classroom = models.CharField(_('classroom'), null=True, blank=True, max_length=16)
    professor = models.CharField(_('professor'), null=True, blank=True, max_length=32)

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

    TIME_DAYS = {
        '월': TIME_MONDAY,
        '화': TIME_TUESDAY,
        '수': TIME_WEDNESDAY,
        '목': TIME_THURSDAY,
        '금': TIME_FRIDAY,
    }

    TIME_CHOICE_SET = []
    for time_choice in TIME_DAYS.items():
        TIME_CHOICE_SET.append((time_choice[1], time_choice[0]))

    day = models.IntegerField(choices=TIME_CHOICE_SET, default=TIME_MONDAY)
    start_time = models.TimeField()
    end_time = models.TimeField()
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
