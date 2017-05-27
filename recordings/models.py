from __future__ import unicode_literals

import re
from datetime import datetime

from django.conf import settings
from django.db import models


COURSE_CHOICES = (
    (1, 'Fall 2016'),
    (2, 'Spring 2017'),
)


class CourseResource(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Course(CourseResource):
    date_start = models.DateField()
    date_end = models.DateField(null=True, blank=True)
    slug = models.SlugField()

    class Meta:
        db_table = 'course'


class CourseSession(CourseResource):
    course = models.ForeignKey(Course)
    num = models.PositiveIntegerField(verbose_name='Course Number')
    date = models.DateField(default=datetime.today())
    slides_url = models.URLField(max_length=250, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)

    class Meta:
        db_table = 'course_session'


class ClassRecording(CourseResource):
    course = models.IntegerField(choices=COURSE_CHOICES)
    url = models.CharField(max_length=250)

    # TODO: migrate session to FK vs int
    session = models.IntegerField()
    session_fk = models.ForeignKey(CourseSession, null=True, blank=True)
    class_date = models.DateField()
    class_part = models.IntegerField()

    class Meta:
        ordering = ['session', 'class_date', '-class_part', ]

    def __unicode__(self):
        return '{} - {} - {} - {}'.format(self.name, self.session,
                                          self.class_date, self.class_part)

    def save(self, *args, **kwargs):
        if not self.course:
            self.course = settings.CURRENT_COURSE
        if self.url:
            if not self.class_part:
                result_part = re.search(r'pt(\d+)', self.url)
                self.class_part = \
                    int(result_part.group(1)) if result_part else 1

            result = re.search(r'class-(\d+)--([\d-]+)(.*)',
                               self.url.strip('.m4a'))
            if result:
                if not self.class_date:
                    date_str = '%Y-%m-%d' \
                        if result.group(2).strip('-').count('-') \
                        else '%Y%m%d'
                    self.class_date = \
                        datetime.strptime(result.group(2).strip('-'), date_str)
                if not self.name:
                    if result.group(3):
                        name = re.sub(r'pt\d+', '', result.group(3)).strip('-')
                        self.name = name.replace('-', ' ').title()
                    else:
                        self.name = ''
                if not self.session:
                    self.session = int(result.group(1))

        super(ClassRecording, self).save(*args, **kwargs)


class CodewarsProblem(CourseResource):
    session = models.ForeignKey(CourseSession)
    url = models.CharField(max_length=250)
    url_solution = models.URLField(max_length=250, null=True, blank=True)
    recording = models.ForeignKey(ClassRecording, null=True, blank=True)

    class Meta:
        db_table = 'course_session_codewars'


class SessionReference(CourseResource):
    session = models.ForeignKey(CourseSession)
    recording = models.ForeignKey(ClassRecording, null=True, blank=True)

    class Meta:
        db_table = 'course_session_reference'

# class Student(CourseResource):
#     course = models.ForeignKey(Course)
#     full_name = models.CharField(max_length=100)
#     email = models.CharField(max_length=200)
