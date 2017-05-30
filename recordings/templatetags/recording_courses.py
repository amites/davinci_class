from django import template
from django.conf import settings

from recordings.models import ClassRecording


register = template.Library()


@register.inclusion_tag('recordings/menu_dropdown.html')
def recordings_dropdown():
    return {
        'courses': settings.COURSE_CHOICES,
    }
