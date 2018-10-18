from django.contrib import admin

from .models import Lecture, LectureTime, Department


class LectureTimeInline(admin.TabularInline):
    model = LectureTime
    extra = 1


class LectureAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'lecture_id',
        'type',
        'department',
        'professor',
    )
    list_filter = ['type', 'department']
    search_fields = ['title', 'lecture_id', 'professor']
    inlines = [LectureTimeInline]


class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'get_number_of_lectures_in_department',
    )


admin.site.register(Lecture, LectureAdmin)
admin.site.register(Department, DepartmentAdmin)
