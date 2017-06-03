# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-27 09:30
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recordings', '0004_auto_20170527_0659'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='github_url',
            field=models.URLField(default='https://github.com/amites/davinci_class_2016/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='coursesession',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 5, 27, 9, 30, 37, 916607)),
        ),
    ]