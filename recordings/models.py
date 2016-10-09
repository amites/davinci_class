from __future__ import unicode_literals

import re
from datetime import datetime

from django.conf import settings
from django.db import models


class ClassRecording(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True)
    url = models.CharField(max_length=250)
    course = models.IntegerField()
    session = models.IntegerField()
    class_date = models.DateField()
    class_part = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['session', 'class_date', 'class_part', ]

    def __unicode__(self):
        return '{} - {} - {} - {}'.format(self.name, self.session,
                                          self.class_date, self.class_part)

    def save(self, *args, **kwargs):
        if not self.course:
            self.course = settings.COURSE
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


