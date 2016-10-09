from django.contrib import admin

from recordings.models import ClassRecording


@admin.register(ClassRecording)
class ClassRecordingAdmin(admin.ModelAdmin):
    date_hierarchy = 'class_date'
    list_display = ('name', 'session', 'class_date', 'class_part', 'course', )
