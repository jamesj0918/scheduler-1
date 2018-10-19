from django.contrib import admin

from .models import Lecture, LectureTime, Department


class LectureTimeInline(admin.TabularInline):
    model = LectureTime
    extra = 1


class LectureAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'uuid',
        'division',
        'type',
        'field',
        'grade',
        'professor',
    )
    list_filter = (
        'type',
        'field',
        'language',
        'department',
        'origin_department',
        'target_department',
    )
    search_fields = ('title', 'lecture_id', 'professor')
    inlines = [LectureTimeInline]


class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'get_number_of_lectures_in_department',
    )


admin.site.register(Lecture, LectureAdmin)
admin.site.register(Department, DepartmentAdmin)
