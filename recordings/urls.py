from django.conf.urls import url

from recordings.views import recording_list, recording_upload

urlpatterns = (
    url(r'^list/(?P<course>[\w-]+)', recording_list, name='list'),
    url(r'^list/?', recording_list, name='list-current'),
    url(r'^upload', recording_upload, name='upload'),
)
