from django.contrib import admin

from recordings.models import (ClassRecording,
                               CodeWarsProblem, Course, CourseSession, SessionReference)


class CourseResourceInlineMixin(admin.StackedInline):
    def get_extra(self, request, obj=None, **kwargs):
        num = 6
        if obj:
            num = 1
        return num


class ClassRecordingsInline(CourseResourceInlineMixin):
    model = ClassRecording


class SessionReferenceInline(CourseResourceInlineMixin):
    model = SessionReference


class CodeWarsProblemInline(CourseResourceInlineMixin):
    model = CodeWarsProblem


@admin.register(ClassRecording)
class ClassRecordingAdmin(admin.ModelAdmin):
    list_display = ('session', 'name', 'has_codewars', )
    save_on_top = True

    inlines = [
        CodeWarsProblemInline,
    ]

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_start', 'slug')
    save_on_top = True


@admin.register(CourseSession)
class CourseSession(admin.ModelAdmin):
    list_display = ('course', 'num', 'has_slides', 'date', )
    save_on_top = True

    list_filter = ['course', ]

    inlines = [
        ClassRecordingsInline,
        SessionReferenceInline,
        CodeWarsProblemInline,
    ]


admin.site.register(CodeWarsProblem)


from recordings.admin_entry import EntryAdmin
from zinnia.models.entry import Entry
admin.site.unregister(Entry)
admin.site.register(Entry, EntryAdmin)

