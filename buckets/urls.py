from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = patterns('',
                      url(r'^$', views.BucketList.as_view()),
                      url(r'^/(?P<bucket_id>[0-9]+)$', views.BucketComposition.as_view()),
                    )

urlpatterns = format_suffix_patterns(urlpatterns)
