from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = patterns('',
                       url(r'^$', views.CompositionList.as_view()),
                       url(r'^/(?P<pk>[0-9]+)$', views.CompositionDetail.as_view(), name='composition-detail'),
                       url(r'^/random$', 'compositions.views.random_composition'),
                       url(r'^/follow$', 'compositions.views.follow_compositions'),
                       url(r'^/(?P<pk>[0-9]+)/votes', include('votes.urls')),
                       url(r'^/(?P<composition_id>[0-9]+)/interpretations', include('interpretations.urls')),
                       url(r'^/tags/(?P<pk>[0-9]+)/add_tags$', 'compositions.views.add_tags'),
                       url(r'^/tags/(?P<pk>[0-9]+)/remove_tags$', 'compositions.views.remove_tags'),
                       url(r'^/tags/(?P<pk>[0-9]+)/remove_all_tags$', 'compositions.views.remove_all_tags'),
                       url(r'^/tags/(?P<pk>[0-9]+)/similar_compostions$', 'compositions.views.similar_compositions'),
                       url(r'^/tags/tag_based_filter$', 'compositions.views.tag_based_filter'),)

urlpatterns = format_suffix_patterns(urlpatterns)
