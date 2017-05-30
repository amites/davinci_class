from __future__ import unicode_literals

import re

from django.db import models

from recordings.models._base import CourseResource
from recordings.models.course import CourseSession


class ClassRecording(CourseResource):
    session = models.ForeignKey(CourseSession, null=True, blank=True)
    url = models.CharField(max_length=250)
    class_part = models.IntegerField()

    class Meta:
        ordering = ['session', '-class_part', ]

    def __unicode__(self):
        return '{} - {} - {} - {}'.format(self.name, self.session.num,
                                          self.session.date, self.class_part)

    def save(self, *args, **kwargs):
        if self.url:
            if not self.class_part:
                result_part = re.search(r'pt(\d+)', self.url)
                self.class_part = \
                    int(result_part.group(1)) if result_part else 1

            result = re.search(r'class-(\d+)--([\d-]+)(.*)',
                               self.url.strip('.m4a'))
            if result:
                if not self.name:
                    if result.group(3):
                        name = re.sub(r'pt\d+', '', result.group(3)).strip('-')
                        self.name = name.replace('-', ' ').title()
                    else:
                        self.name = ''
                if not self.session:
                    self.session = int(result.group(1))

        super(ClassRecording, self).save(*args, **kwargs)


class CodeWarsProblem(CourseResource):
    session = models.ForeignKey(CourseSession)
    url = models.CharField(max_length=250)
    url_solution = models.URLField(max_length=250, null=True, blank=True)
    recording = models.ForeignKey(ClassRecording, null=True, blank=True)

    class Meta:
        db_table = 'course_session_codewars'


