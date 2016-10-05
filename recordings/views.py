from django.shortcuts import render

from recordings.models import ClassRecording


def recording_list(request):
    context = {
        'recordings': ClassRecording.objects.order_by('class_date',
                                                      'class_part'),
    }
    return render(request, 'recordings/list.html', context)
