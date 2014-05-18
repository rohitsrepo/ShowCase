from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = patterns('',
                       url(r'^$', views.CompositionList.as_view()),
                       url(r'^/(?P<pk>[0-9]+)$', views.CompositionDetail.as_view(), name='composition-detail'),
                       url(r'^/(?P<pk>[0-9]+)/vote', include('votes.urls')),
                       url(r'^/(?P<pk>[0-9]+)/comments', include('comments.urls')),)

urlpatterns = format_suffix_patterns(urlpatterns)
