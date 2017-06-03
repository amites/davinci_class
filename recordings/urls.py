from django.conf.urls import url

from recordings.views import course_list, recording_list, recording_upload

urlpatterns = (
    url(r'^course/(?P<course_arg>[\w-]+)$', course_list, name='course'),
    url(r'^course/?$', course_list, name='course-current'),

    url(r'^list/(?P<course>[\w-]+)', recording_list, name='list'),
    url(r'^list/?', recording_list, name='list-current'),

    url(r'^upload', recording_upload, name='upload'),
)
