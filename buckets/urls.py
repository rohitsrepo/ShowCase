from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = patterns('',
                      url(r'^$', views.BucketList.as_view()),
                      url(r'^/(?P<bucket_slug>[\w-]+)$', views.BucketDetail.as_view()),
                      url(r'^/(?P<bucket_id>[0-9]+)/public$', 'buckets.views.make_bucket_public'),
                      url(r'^/(?P<bucket_id>[0-9]+)/arts$', views.BucketCompositionList.as_view()),
                      url(r'^/(?P<bucket_id>[0-9]+)/arts/(?P<composition_id>[0-9]+)$', views.BucketCompositionDetail.as_view()),
                      url(r'^/(?P<bucket_id>[0-9]+)/background$', views.BucketBackground.as_view()),
                    )

urlpatterns = format_suffix_patterns(urlpatterns)
