from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render

from recordings.models import ClassRecording, Course, CourseSession


def course_list(request, course_arg=None):
    kwargs = {}
    if str(course_arg).isdigit():
        field = 'id'
        val = int(course_arg)
    else:
        field = 'slug'
        val = course_arg

    kwargs['course__{}'.format(field)] = val


    sessions = CourseSession.objects.filter(**kwargs).order_by('-date')
    context = {
        'sessions': sessions,
        'course': get_object_or_404(Course, **{field: val})
    }

    return render(request, 'course/list.html', context)


def recording_list(request, course=None):
    kwargs = {}
    if str(course).isdigit():
        kwargs['id'] = int(course)
    else:
        kwargs['slug'] = course

    try:
        session = Course.objects.get(**kwargs)
    except Course.DoesNotExist:
        session = None

    kwargs = dict([('session__course__' + var, val) for var, val in kwargs.items()])
    recordings = ClassRecording.objects.filter(**kwargs).order_by('session__date', 'class_part')
    if recordings:
        course = recordings[0].session.course
    else:
        course = None
    context = {
        'recordings': recordings,
        'course': course,
    }

    return render(request, 'recordings/list.html', context)


@staff_member_required
def recording_upload(request):
    context = {

    }
    return render(request, 'recordings/upload.html', context)
