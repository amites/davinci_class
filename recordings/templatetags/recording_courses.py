from django import template

from recordings.models import ClassRecording, COURSE_CHOICES


register = template.Library()


@register.inclusion_tag('recordings/menu_dropdown.html')
def recordings_dropdown():
    return {
        'courses': COURSE_CHOICES,
    }
