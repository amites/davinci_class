from django.conf.urls import url

from recordings.views import course_list, recording_list

urlpatterns = (
    url(r'^course/(?P<course_arg>[\w-]+)$', course_list, name='course'),
    url(r'^course/?$', course_list, name='course-current'),

    url(r'^list/(?P<course_arg>[\w-]+)', recording_list, name='list'),
    url(r'^list/?', recording_list, name='list-current'),
)
