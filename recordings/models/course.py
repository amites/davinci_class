from datetime import datetime

from django.db import models
from taggit.managers import TaggableManager

from recordings.models._base import CourseResource


class Course(CourseResource):
    date_start = models.DateField()
    date_end = models.DateField(null=True, blank=True)
    slug = models.SlugField()
    github_url = models.URLField(null=True)

    class Meta:
        db_table = 'course'

    def __str__(self):
        return self.name


class CourseSession(CourseResource):
    course = models.ForeignKey(Course)
    num = models.PositiveIntegerField(verbose_name='Session Number')
    date = models.DateField(default=datetime.today())
    slides_url = models.URLField(max_length=250, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)

    tags = TaggableManager()

    class Meta:
        db_table = 'course_session'

    def __str__(self):
        return '{} - {}'.format(self.date, self.num)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.slug:
            self.slug = '{}-{}'.format(self.course.slug, self.num)
        super(CourseSession, self).save(force_insert=False, force_update=False, using=None,
                                        update_fields=None)
