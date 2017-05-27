from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from recordings.models import ClassRecording, COURSE_CHOICES


def recording_list(request, course=None):
    kwargs = {}
    if str(course).isdigit():
        kwargs['session__course_id'] = int(course)
    else:
        kwargs['session__course__slug'] = course

    recordings = ClassRecording.objects.filter(**kwargs).order_by('session__date', 'class_part')
    context = {
        'recordings': recordings,
        'session': recordings[0].session,
    }
    return render(request, 'recordings/list.html', context)


@staff_member_required
def recording_upload(request):
    context = {

    }
    return render(request, 'recordings/upload.html', context)