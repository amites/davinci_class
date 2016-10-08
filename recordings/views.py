from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from recordings.models import ClassRecording


def recording_list(request):
    context = {
        'recordings': ClassRecording.objects.order_by('class_date',
                                                      'class_part'),
    }
    return render(request, 'recordings/list.html', context)


@staff_member_required
def recording_upload(request):
    import ipdb
    ipdb.set_trace()
    context = {

    }
    return render(request, 'recordings/upload.html', context)