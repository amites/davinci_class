from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from recordings.models import ClassRecording, Course


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
    context = {
        'recordings': recordings,
        'session': session,
    }
    return render(request, 'recordings/list.html', context)


@staff_member_required
def recording_upload(request):
    context = {

    }
    return render(request, 'recordings/upload.html', context)