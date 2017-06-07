# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-03 08:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('recordings', '0006_auto_20170603_0353'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='classrecording',
            options={'ordering': ['session', 'class_part']},
        ),
        migrations.AddField(
            model_name='classrecording',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='codewarsproblem',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='coursesession',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='sessionreference',
            name='kyu',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sessionreference',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='coursesession',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 6, 3, 8, 26, 11, 996588)),
        ),
    ]