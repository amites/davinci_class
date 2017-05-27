from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from recordings.models import ClassRecording, COURSE_CHOICES


def recording_list(request, course=None):
    if not course:
        course = settings.CURRENT_COURSE
    context = {
        'recordings':
            ClassRecording.objects.filter(
                course=course
            ).order_by('class_date', 'class_part'),
        'course': dict(COURSE_CHOICES).get(course, ''),
    }
    return render(request, 'recordings/list.html', context)


@staff_member_required
def recording_upload(request):
    context = {

    }
    return render(request, 'recordings/upload.html', context)