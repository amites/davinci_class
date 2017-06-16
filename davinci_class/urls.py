from __future__ import unicode_literals

from django.conf.urls import include, url
# from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
# from django.views.i18n import set_language
from django.views.generic import RedirectView

import recordings.urls


admin.autodiscover()


urlpatterns = [
    url(r'^blog/', include('zinnia.urls')),
    url(r'^comments/', include('django_comments.urls')),

    url(r'^admin/tools/', include('admin_tools.urls')),
    url(r'^admin/', include(admin.site.urls)),
    # Change the admin prefix here to use an alternate URL for the
    # admin interface, which would be marginally more secure.
    url("^admin/", include(admin.site.urls)),

    url(r'^recordings/', include(recordings.urls, namespace='recordings')),

    url(r'^$', RedirectView.as_view(url='/blog/',
                                    permanent=False), name='home'),
]
