from django.conf.urls import patterns, url, include

from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = patterns('',
                      url(r'^$', 'search.views.search'),
                      url(r'^/users$', 'search.views.search_users'),
                      url(r'^/buckets$', 'search.views.search_buckets'),
                      url(r'^/compositions$', 'search.views.search_compositions'),
                    )

urlpatterns = format_suffix_patterns(urlpatterns)
