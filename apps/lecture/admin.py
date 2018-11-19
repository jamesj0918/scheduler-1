from django.contrib import admin

from .models import Lecture, LectureTime, Department


class LectureTimeInline(admin.TabularInline):
    model = LectureTime
    extra = 1


class LectureAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'code',
        'division',
        'type',
        'category',
        'subcategory',
        'grade',
        'point',
        'professor',
        'classroom',
    )
    list_filter = (
        'type',
        'language',
        'category',
        'subcategory',
        'department',
    )
    search_fields = ('title', 'code', 'professor')
    inlines = [LectureTimeInline]
    ordering = ('id',)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'get_number_of_lectures_in_department',
    )
    search_fields = ('title',)


admin.site.register(Lecture, LectureAdmin)
admin.site.register(Department, DepartmentAdmin)
