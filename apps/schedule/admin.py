from django.contrib import admin

from .models import Schedule


class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'owner',
        'get_number_of_lectures_in_schedule',
    )


admin.site.register(Schedule, ScheduleAdmin)