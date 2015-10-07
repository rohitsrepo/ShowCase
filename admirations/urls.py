from django.conf.urls import patterns, url, include

from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = patterns('',
                      url(r'^$', views.AdmirationsList.as_view()),
                      url(r'^/(?P<user_id>[0-9]+)$', views.AdmirationsListRead.as_view()),
                    )

urlpatterns = format_suffix_patterns(urlpatterns)
