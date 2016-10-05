from __future__ import unicode_literals

from django.db import models


class ClassRecording(models.Model):
    name = models.CharField(max_length=250)
    url = models.CharField(max_length=250)
    course = models.IntegerField()
    session = models.IntegerField()
    class_date = models.DateField()
    class_part = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '{} - {} - {} - {}'.format(self.name, self.session,
                                          self.class_date, self.class_part)
