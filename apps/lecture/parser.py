from openpyxl import load_workbook

from .models import Lecture, LectureTime, Department


category_data = open('categories.txt', 'r')
category_data = category_data.read().splitlines()
categories = []

for _category in category_data:
    _category = _category.split(' ')
    categories.append(_category)


def create_parser(path, worksheet):
    wb = load_workbook(path, read_only=True)
    ws = wb[worksheet]
    return ws


def parse_lecture_data():
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
        uuid = row[2].value             # column C
        division = row[3].value         # column D
        grade = int(row[7].value)       # column H
        point = float(row[8].value)     # column I

        # column F
        lecture_type = Lecture.LECTURE_TYPE.get(row[5].value)

        # column G
        # category = categorize_lecture(title)

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
            title=title, uuid=uuid, division=division, grade=grade, point=point,
            type=lecture_type, category=category, language=language,
            department=department, origin_department=origin_dept,
            classroom=classroom, professor=professor,
        )

        # column L
        rawtimes = row[11].value

        # if value is None, skip the current row
        if rawtimes is None:
            continue

        # split rawtime with comma
        rawtimes = rawtimes.split(',')
        for rawtime in rawtimes:
            rawtime = rawtime.split()
            days_cache = []
            for token in rawtime:
                # add all days before timerange into days_cache
                if token in LectureTime.TIME_DAYS:
                    days_cache.append(LectureTime.TIME_DAYS[token])
                # create time range with days
                elif len(token) > 2:
                    times = token.split('~')
                    for days in days_cache:
                        LectureTime.objects.get_or_create(
                            lecture=lecture, start=times[0], end=times[1], day=days)
                    days_cache.clear()


def categorize_lecture(title):
    """
    Categorize a lecture with the lecture title.
    """
    score = []
    found = False

    for category in category_data:
        result = 0
        for keyword in category.split():
            if keyword in title.lower():
                found = True
                result = result + 1
        if found:
            score.append(result)
        else:
            score.append(0)

    lecture_idx = score.index(max(score)) + 1
    if max(score) == 0 and lecture_idx == 1:
        return '없음'

    for lecture, idx in Lecture.CATEGORY_TYPE.items():
        if idx == lecture_idx:
            return lecture

    return '없음'
