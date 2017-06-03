from __future__ import unicode_literals

import re
from datetime import datetime

from django.conf import settings
from django.db import models
from taggit.managers import TaggableManager

from recordings.models.course import CourseSession
from recordings.models._base import CourseResource


COURSE_CHOICES = (
    (1, 'Fall 2016'),
    (2, 'Spring 2017'),
)


class ClassRecording(CourseResource):
    session = models.ForeignKey(CourseSession, null=True, blank=True)
    url = models.CharField(max_length=250)
    class_part = models.IntegerField()

    tags = TaggableManager()

    class Meta:
        ordering = ['session', 'class_part', ]

    def __str__(self):
        return '{} - {} - {} - {}'.format(self.name, self.session.num, self.session.date, self.class_part)

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

    @property
    def has_codewars(self):
        return bool(self.codewarsproblem_set.count())


class CodeWarsProblem(CourseResource):
    session = models.ForeignKey(CourseSession, null=True, blank=True)
    url = models.CharField(max_length=250)
    url_solution = models.URLField(max_length=250, null=True, blank=True)
    recording = models.ForeignKey(ClassRecording, null=True, blank=True)

    tags = TaggableManager()

    class Meta:
        db_table = 'course_session_codewars'

    def save(self, *args, **kwargs):
        if not self.session and self.recording:
            self.session = self.recording.session
        super(CodeWarsProblem, self).save(*args, **kwargs)


class SessionReference(CourseResource):
    session = models.ForeignKey(CourseSession)
    recording = models.ForeignKey(ClassRecording, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    gist_url = models.URLField(null=True, blank=True)
    snippet = models.TextField(null=True, blank=True)
    kyu = models.PositiveIntegerField(null=True, blank=True)

    tags = TaggableManager()

    class Meta:
        db_table = 'course_session_reference'

# class Student(CourseResource):
#     course = models.ForeignKey(Course)
#     full_name = models.CharField(max_length=100)
#     email = models.CharField(max_length=200)


