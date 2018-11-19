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

    CATEGORY_NONE = 0
    CATEGORY_ECONOMICS = 1
    CATEGORY_MANAGEMENT = 2
    CATEGORY_LANGUAGE = 3
    CATEGORY_BROADCASTING = 4
    CATEGORY_HUMANITY = 5
    CATEGORY_PSYCHOLOGY = 6
    CATEGORY_HISTORY = 7
    CATEGORY_SPORTS = 8
    CATEGORY_CAREER = 9
    CATEGORY_CULTURE = 10
    CATEGORY_SOCIETY = 11
    CATEGORY_SCIENCE = 12
    CATEGORY_MATHEMATICS = 13
    CATEGORY_ART = 14
    CATEGORY_RELIGION = 15
    CATEGORY_LIFESTYLE = 16
    CATEGORY_HOBBY = 17
    CATEGORY_COMPUTER = 18
    CATEGORY_TECHNOLOGY = 19
    CATEGORY_CONVERGENCE = 20
    CATEGORY_COMICS = 21

    CATEGORY_TYPE = {
        '없음': CATEGORY_NONE,
        '경제': CATEGORY_ECONOMICS,
        '경영': CATEGORY_MANAGEMENT,
        '언어': CATEGORY_LANGUAGE,
        '방송': CATEGORY_BROADCASTING,
        '인문': CATEGORY_HUMANITY,
        '심리': CATEGORY_PSYCHOLOGY,
        '역사': CATEGORY_HISTORY,
        '스포츠': CATEGORY_SPORTS,
        '진로': CATEGORY_CAREER,
        '문화': CATEGORY_CULTURE,
        '사회': CATEGORY_SOCIETY,
        '과학': CATEGORY_SCIENCE,
        '수학': CATEGORY_MATHEMATICS,
        '예술': CATEGORY_ART,
        '종교': CATEGORY_RELIGION,
        '생활': CATEGORY_LIFESTYLE,
        '취미': CATEGORY_HOBBY,
        '컴퓨터': CATEGORY_COMPUTER,
        '기술': CATEGORY_TECHNOLOGY,
        '융합': CATEGORY_CONVERGENCE,
        '만화': CATEGORY_COMICS,
    }

    CATEGORY_CHOICE_SET = []
    for category_choice in CATEGORY_TYPE.items():
        CATEGORY_CHOICE_SET.append((category_choice[1], category_choice[0]))

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

    code = models.CharField(_('lecture id'), max_length=16)
    division = models.CharField(_('division'), max_length=8, default=1)
    title = models.CharField(_('title'), max_length=64)
    type = models.IntegerField(_('lecture type'),
                               null=True, blank=True, choices=LECTURE_CHOICE_SET, default=LECTURE_REQUIRED)
    category = models.IntegerField(_('lecture category'),
                                   null=True, blank=True, choices=CATEGORY_CHOICE_SET, default=CATEGORY_NONE)
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
    start = models.TimeField()
    end = models.TimeField()
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='timetable')
