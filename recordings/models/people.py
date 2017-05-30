from django.db import models

from recordings.models._base import CourseResource
from recordings.models.course import Course


class Student(CourseResource):
    url = models.URLField()
    github_url = models.URLField()
    email = models.CharField(max_length=150)
    slack_name = models.CharField(max_length=50)
    slack_id = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    course = models.ForeignKey(Course)

