from django.conf.urls import url

from recordings.views import recording_list

urlpatterns = (
    url(r'^list', recording_list, name='list'),
)
