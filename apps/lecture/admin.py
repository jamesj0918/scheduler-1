from django.contrib import admin

from .models import Lecture, Department


class LectureAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'lecture_id',
        'type',
        'department',
        'professor',
        'start_time',
        'end_time',
    )


class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'get_number_of_lectures_in_department',
    )


admin.site.register(Lecture, LectureAdmin)
admin.site.register(Department, DepartmentAdmin)
