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


def recording_list(request, course_arg=None):
    kwargs = {}
    if str(course_arg).isdigit():
        kwargs['id'] = int(course_arg)
    else:
        kwargs['slug'] = course_arg

    try:
        course = Course.objects.get(**kwargs)
    except Course.DoesNotExist:
        course = None

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


# TODO: add API end point to post a new CourseSession
    # POST or JSON -- Django Rest Framework @api_view(['POST'])
    # Load fields
        # - course_id [int] - (think through better identifier?
        # - session_num [int]
        # - session_date [str] - convert to datetime.date
        # - slides_url [str] *optional*
        # - slug [str] *optional*
        # - class_recordings [list] - dict's or empty
            # class_part [int]
            # url [str]
