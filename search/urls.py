from django.conf.urls import patterns, url, include

from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = patterns('',
                      url(r'^$', 'search.views.search'),
                    )

urlpatterns = format_suffix_patterns(urlpatterns)
