import re

from openpyxl import load_workbook

from .models import (
    Lecture, LectureTime, Department, Category, Subcategory
)


def create_parser(path, worksheet):
    wb = load_workbook(path, read_only=True)
    ws = wb[worksheet]
    return ws


def split_string(string):
    if string is None:
        return ['']

    elif '/' in string:
        return string.split('/')

    elif ',' in string:
        return string.split(',')

    else:
        return [string]


def parse_lecture_data(file, use_log):

    lecture_data = create_parser(file, '강의시간표(schedule)')

    first_row = False
    for row in lecture_data.rows:
        # Skip the first row
        if not first_row:
            first_row = True
            continue

        title = row[4].value  # column E
        code = row[2].value  # column C
        division = row[3].value  # column D
        grade = int(row[7].value)  # column H
        point = float(row[8].value)  # column I
        lecture_type = Lecture.LECTURE_TYPE.get(row[5].value)  # column F
        language = Lecture.LANGUAGE_TYPE.get(row[18].value)  # column S

        department, created = Department.objects.get_or_create(title=row[1].value)  # column B
        origin_dept, created = Department.objects.get_or_create(title=row[14].value)  # column O

        classroom = row[12].value  # column M
        professor = row[13].value  # column N

        lecture = Lecture.objects.create(
            title=title, code=code, division=division, grade=grade, point=point,
            type=lecture_type, language=language,
            department=department, origin_department=origin_dept,
            classroom=classroom, professor=professor,
        )

        rawtimes = row[11].value  # column L

        # if value is None, skip the current row
        if rawtimes is None:
            continue

        # split time and places
        rawtimes = split_string(rawtimes)
        places = split_string(classroom)

        # final time data stored
        # e.g. if the given data is '월 수 16:30~18:00, 수 18:00~20:00'
        # time_data = [['월', ['16:30', '18:00']], ['수', ['16:30', '18:00']], ['수', ['18:00', '20:00']]]
        time_data = []

        # regex for finding time in string
        # e.g. if the given data is '월 수 16:30~18:00'
        # regex finds 16:30, 18:00
        time_regex = re.compile('\d\d:\d\d')

        # generate time_data with given data
        for rawtime in rawtimes:
            rawtime.strip()
            times = time_regex.findall(rawtime)
            days = [day for day in rawtime[0:rawtime.find(times[0])] if day is not ' ']

            for day in days:
                time_data.append([day, times])

        # e.g. time_data is 월 수 16:30~18:00 and classroom is 광715
        # e.g. time_data is 월 수 16:30~18:00, 수 18:00~20:00 and classroom is 율301,동401
        if len(time_data) > len(places):
            while len(time_data) > len(places):
                places.insert(0, places[0])

        # e.g. time_data is 월 16:30~18:00 and classroom is 율301,동401
        # Doesn't really make sense
        elif len(time_data) < len(places):
            places = [','.join(places)]

        for (data, place) in zip(time_data, places):
            if place is not '':
                place = LectureTime.PLACE_TYPE.get(place.strip()[0][0], None)
            else:
                place = None
            day = LectureTime.DAYS[data[0].strip()]
            LectureTime.objects.create(lecture=lecture, start=data[1][0], end=data[1][1], day=day, place=place)

        time_data.clear()

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
