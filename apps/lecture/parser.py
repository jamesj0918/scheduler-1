from openpyxl import load_workbook

from .models import (
    Lecture, LectureTime, Department, Category, Subcategory
)


def create_parser(path, worksheet):
    wb = load_workbook(path, read_only=True)
    ws = wb[worksheet]
    return ws


def parse_lecture_data(use_log):
    """
    Parse the lecture.xlsx file and create a lecture database.
    """
    lecture_data = create_parser('lectures.xlsx', '강의시간표(schedule)')

    first_row = False
    for row in lecture_data.rows:
        # Skip the first row
        if not first_row:
            first_row = True
            continue

        title = row[4].value            # column E
        code = row[2].value             # column C
        division = row[3].value         # column D
        grade = int(row[7].value)       # column H
        point = float(row[8].value)     # column I

        # column F
        lecture_type = Lecture.LECTURE_TYPE.get(row[5].value)

        # column G
        categories, subcategories = categorize_lecture(title)

        # column S
        language = Lecture.LANGUAGE_TYPE.get(row[18].value)

        # column B
        department, created = Department.objects.get_or_create(title=row[1].value)

        # column O
        origin_dept, created = Department.objects.get_or_create(title=row[14].value)

        classroom = row[12].value       # column M
        professor = row[13].value       # column N

        # Create a corresponding object for an input.
        lecture = Lecture.objects.create(
            title=title, code=code, division=division, grade=grade, point=point,
            type=lecture_type, language=language,
            department=department, origin_department=origin_dept,
            classroom=classroom, professor=professor,
        )

        # Add categories and subcategories
        for category in categories:
            item, created = Category.objects.get_or_create(category=category)
            lecture.category.add(item)

        for subcategory in subcategories:
            item, created = Subcategory.objects.get_or_create(subcategory=subcategory)
            lecture.subcategory.add(item)

        # column L
        rawtimes = row[11].value

        # if value is None, skip the current row
        if rawtimes is None:
            continue

        # split time with comma
        rawtimes = rawtimes.split(',')
        if classroom is not None:
            places = classroom.split(',')
            for (rawtime, place) in zip(rawtimes, places):
                rawtime = rawtime.split()
                place = LectureTime.PLACE_TYPE.get(place.strip()[0], None)

                days_cache = []
                for token in rawtime:
                    # add all days before time range into days_cache
                    if token in LectureTime.DAYS:
                        days_cache.append(LectureTime.DAYS[token])
                    # create time range with days
                    elif len(token) > 2:
                        times = token.split('~')
                        for days in days_cache:
                            LectureTime.objects.create(
                                lecture=lecture, place=place, start=times[0], end=times[1], day=days)
                        days_cache.clear()
        else:
            for rawtime in rawtimes:
                rawtime = rawtime.split()
                days_cache = []
                for token in rawtime:
                    # add all days before time range into days_cache
                    if token in LectureTime.DAYS:
                        days_cache.append(LectureTime.DAYS[token])
                    # create time range with days
                    elif len(token) > 2:
                        times = token.split('~')
                        for days in days_cache:
                            LectureTime.objects.create(
                                lecture=lecture, place=None, start=times[0], end=times[1], day=days)
                        days_cache.clear()

        if use_log is True:
            print(title + '(' + str(lecture.id) + ' | ' + code + ')')


def categorize_lecture(title):
    """
    Categorize a lecture with the lecture title.
    Returns main category and subcategory.
    """
    category_prefix = '@'
    subcategory_prefix = '#'

    file = open('categories.txt', 'r')
    data = file.read().splitlines()

    categories = []
    subcategories = []

    category = Category.NONE
    subcategory = Subcategory.NONE
    found = False

    for line in data:
        if line[0] == category_prefix:
            # Current line is category.
            category = line[1:]
            found = False
        elif line[0] == subcategory_prefix:
            # Current line is subcategory.
            subcategory = line[1:]
            found = False
        else:
            # Current line is title of lectures. Search title in this line.
            # and if the lecture is found, set the found True.
            lectures = [x.strip() for x in line.split('_')]
            if title in lectures:
                found = True

        if found:
            # If we found a lecture, append category and subcategory to list.
            if category != Category.NONE:
                categories.append(Category.CATEGORIES[category])
            if subcategory != Subcategory.NONE:
                subcategories.append(Subcategory.SUBCATEGORIES[subcategory])
            found = False

    file.close()
    return categories, subcategories
