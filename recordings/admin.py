from django.contrib import admin

from recordings.models import (ClassRecording,
                               CodeWarsProblem, Course, CourseSession, SessionReference)


class ClassRecordingsInline(admin.StackedInline):
    model = ClassRecording


class SessionReferenceInline(admin.StackedInline):
    model = SessionReference


class CodeWarsProblemInline(admin.StackedInline):
    model = CodeWarsProblem


@admin.register(ClassRecording)
class ClassRecordingAdmin(admin.ModelAdmin):
    list_display = ('session', 'name', 'has_codewars', )

    inlines = [
        CodeWarsProblemInline,
    ]

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_start', 'slug')


@admin.register(CourseSession)
class CourseSession(admin.ModelAdmin):
    list_display = ('course', 'num', 'date', )
    inlines = [
        ClassRecordingsInline,
        SessionReferenceInline,
        CodeWarsProblemInline,
    ]


admin.site.register(CodeWarsProblem)
