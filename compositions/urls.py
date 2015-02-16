from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = patterns('',
                       url(r'^$', views.CompositionList.as_view()),
                       url(r'^/(?P<pk>[0-9]+)$', views.CompositionDetail.as_view(), name='composition-detail'),
                       url(r'^/random$', 'compositions.views.random_composition'),
                       url(r'^/follow$', 'compositions.views.follow_compositions'),
                       url(r'^/(?P<pk>[0-9]+)/votes', include('votes.urls')),
                       url(r'^/(?P<composition_id>[0-9]+)/interpretations', include('interpretations.urls')),)

urlpatterns = format_suffix_patterns(urlpatterns)
