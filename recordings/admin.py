from django.contrib import admin

from recordings.models import (ClassRecording,
                               CodeWarsProblem, Course, CourseSession, SessionReference)


@admin.register(ClassRecording)
class ClassRecordingAdmin(admin.ModelAdmin):
    list_display = ('session', 'name', )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_start', 'slug')


class ClassRecordingsInline(admin.TabularInline):
    model = ClassRecording


class SessionReferenceInline(admin.TabularInline):
    model = SessionReference

class CodeWarsProblemInline(admin.TabularInline):
    model = CodeWarsProblem


@admin.register(CourseSession)
class CourseSession(admin.ModelAdmin):
    list_display = ('course', 'num')
    inlines = [
        ClassRecordingsInline,
        SessionReferenceInline,
        CodeWarsProblemInline,
    ]


admin.site.register(CodeWarsProblem)
