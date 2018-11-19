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


class Category(models.Model):
    NONE = 0
    MARKET = 1
    HUMANITY = 2
    SOCIETY = 3
    MILITARY = 4
    SCIENCE = 5
    ART = 6
    LANGUAGE = 7
    CAREER = 8
    HOBBY = 9

    CATEGORIES = {
        '없음': NONE,
        '상경계': MARKET,
        '인문학': HUMANITY,
        '사회과학': SOCIETY,
        '국방/군사/경찰': MILITARY,
        '과학/공학': SCIENCE,
        '예술': ART,
        '언어': LANGUAGE,
        '진로': CAREER,
        '취미/생활': HOBBY,
    }

    CHOICE_SET = []
    for category_choice in CATEGORIES.items():
        CHOICE_SET.append((category_choice[1], category_choice[0]))

    category = models.IntegerField(choices=CHOICE_SET, default=NONE)

    def __str__(self):
        return self.category


class Subcategory(models.Model):
    NONE = 0
    # MARKET
    ECONOMY = 1
    MANAGEMENT = 2
    MARKETING = 3
    # HUMANITY
    PHILOSOPHY = 4
    LITERATURE = 5
    HISTORY = 6
    # SOCIETY
    ADMINISTRATION = 7
    PSYCHOLOGY = 8
    EDUCATION = 9
    LAW = 10
    SOCIETY = 11
    NEWS = 12
    # MILITARY
    # SCIENCE
    MACHINARY = 13
    CONSTRUCT = 14
    PHYSICS = 15
    BIOLOGY = 16
    MATHEMATICS = 17
    ASTRONOMY = 18
    CHEMISTRY = 19
    COMPUTRE = 20
    # ART
    DANCE = 21
    ART = 22
    MUSIC = 23
    MOVIE = 24
    CULTURE = 25
    # LANGUAGE
    KOREAN = 26
    ENGLISH = 27
    JAPANESE = 28
    CHINESE = 29
    # CAREER
    BUSINESS = 30
    CAREER = 31
    ESSAY = 32
    LICENSE = 33
    EXAM = 34
    ENLIGHTMENT = 35
    # HOBBY
    LIVING = 36
    SPORTS = 37
    FASHION = 38

    SUBCATEGORIES = {
        '없음': NONE,
        '경제': ECONOMY,
        '경영': MANAGEMENT,
        '마케팅': MARKETING,
        '철학': PHILOSOPHY,
        '문학': LITERATURE,
        '역사/문화': HISTORY,
        '행정': ADMINISTRATION,
        '심리': PSYCHOLOGY,
        '교육학': EDUCATION,
        '법': LAW,
        '사회학': SOCIETY,
        '언론/신문/방송': NEWS,
        '기계/전기/전자': MACHINARY,
        '도시/토목/건설': CONSTRUCT,
        '물리학': PHYSICS,
        '생물학': BIOLOGY,
        '수학': MATHEMATICS,
        '천문/지구과학': ASTRONOMY,
        '화학': CHEMISTRY,
        '컴퓨터': COMPUTRE,
        '무용': DANCE,
        '미술': ART,
        '음악': MUSIC,
        '연극/영화': MOVIE,
        '대중문화': CULTURE,
        '국어': KOREAN,
        '영어': ENGLISH,
        '일본어': JAPANESE,
        '중국어': CHINESE,
        '창업/취업': BUSINESS,
        '진로': CAREER,
        '논술/면접대비': ESSAY,
        '공무원/자격증': LICENSE,
        '고시': EXAM,
        '자기능력계발': ENLIGHTMENT,
        '리빙': LIVING,
        '레저/스포츠': SPORTS,
        '여성/패션': FASHION
    }

    CHOICE_SET = []
    for subcategory_choice in SUBCATEGORIES.items():
        CHOICE_SET.append((subcategory_choice[1], subcategory_choice[0]))

    subcategory = models.IntegerField(choices=CHOICE_SET, default=NONE)

    def __str__(self):
        return self.subcategory


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
    grade = models.IntegerField(_('grade'), default=1, null=True, blank=True)
    point = models.FloatField(_('point'), default=1.0, null=True, blank=True)
    language = models.IntegerField(_('language'),
                                   null=True, blank=True, choices=LANGUAGE_CHOICE_SET, default=LANGUAGE_KOR)

    category = models.ForeignKey(
        Category, verbose_name=_('category'), on_delete=models.CASCADE, related_name='lectures')
    subcategory = models.ForeignKey(
        Subcategory, verbose_name=_('subcategory'), on_delete=models.CASCADE, related_name='lectures')

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
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4

    DAYS = {
        '월': MONDAY,
        '화': TUESDAY,
        '수': WEDNESDAY,
        '목': THURSDAY,
        '금': FRIDAY,
    }

    CHOICE_SET = []
    for time_choice in DAYS.items():
        CHOICE_SET.append((time_choice[1], time_choice[0]))

    day = models.IntegerField(choices=CHOICE_SET, default=MONDAY)
    start = models.TimeField()
    end = models.TimeField()
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='timetable')
