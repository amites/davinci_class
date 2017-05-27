# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-27 06:57
from __future__ import unicode_literals

from datetime import datetime

from django.db import migrations


def clean_2016(apps, schema):
    ClassRecording = apps.get_model('recordings', 'ClassRecording')
    CourseSession = apps.get_model('recordings', 'CourseSession')
    Course = apps.get_model('recordings', 'Course')

    c1, created = Course.objects.get_or_create(name='Fall 2016', date_start=datetime.strptime('2016-08-09', '%Y-%m-%d'),
                                               slug='2016-fall')

    crs = ClassRecording.objects.filter(course=1)
    # cr = crs[0]
    for cr in crs:
        class_num, class_date = cr.url.split('/')[-1][:-4].split('--', 1)
        class_num = int(class_num.split('-')[1])

        if len(class_date.split('--')) > 1:
            class_date = class_date.split('--')[0]
        try:
            session_date = datetime.strptime(class_date, '%Y-%m-%d')
        except ValueError:
            session_date = datetime.strptime(class_date, '%Y%m%d')

        session, __ = CourseSession.objects.get_or_create(course=c1, num=class_num,
                                                          date=session_date)

        cr.session_fk = session
        cr.url = cr.url.replace('https://davinci-institute.s3.amazonaws.com/',
                                'https://davinci-institute.s3.amazonaws.com/2016-fall/')
        cr.save()


class Migration(migrations.Migration):

    dependencies = [
        ('recordings', '0002_auto_20170527_0613'),
    ]

    operations = [
        migrations.RunPython(clean_2016, migrations.RunPython.noop),
    ]
