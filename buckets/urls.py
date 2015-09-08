from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views, watchers

urlpatterns = patterns('',
                      url(r'^$', views.BucketList.as_view()),
                      url(r'^/(?P<bucket_slug>[\w-]+)$', views.BucketDetail.as_view()),
                      url(r'^/(?P<bucket_id>[0-9]+)/arts$', views.BucketComposition.as_view()),
                      url(r'^/(?P<bucket_id>[0-9]+)/background$', views.BucketBackground.as_view()),
                      url(r'^/(?P<bucket_id>[0-9]+)/watchers$', watchers.BucketWatcherDetail.as_view()),
                    )

urlpatterns = format_suffix_patterns(urlpatterns)
