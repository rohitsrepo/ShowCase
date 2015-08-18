from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns
from posts.views import CompositionPostList
from . import views

urlpatterns = patterns('',
                       url(r'^$', views.CompositionList.as_view()),
                       url(r'^/(?P<pk>[0-9]+)$', views.CompositionDetail.as_view(), name='composition-detail'),
                       url(r'^/explore$', 'compositions.exploreViews.get_explores', name='explore'),
                       url(r'^/random$', 'compositions.views.random_composition'),
                       url(r'^/matter$', 'compositions.views.composition_matter'),
                       url(r'^/follow$', 'compositions.views.follow_compositions'),
                       url(r'^/(?P<pk>[0-9]+)/votes', include('votes.urls')),
                       url(r'^/(?P<composition_id>[0-9]+)/interpretations', include('interpretations.urls')),
                       url(r'^/(?P<composition_id>[0-9]+)/interpretation-images$', views.InterpretationImageList.as_view()),
                       url(r'^/(?P<composition_id>[0-9]+)/interpretation-images/(?P<image_id>[0-9]+)$', views.InterpretationImageDetail.as_view()),
                       url(r'^/(?P<composition_id>[0-9]+)/posts$', CompositionPostList.as_view()),
                       url(r'^/(?P<composition_id>[0-9]+)/bookmarkers$', 'compositions.views.get_bookmarkers'),
                       url(r'^/(?P<composition_id>[0-9]+)/buckets$', 'buckets.views.get_composition_buckets'),
               )

urlpatterns = format_suffix_patterns(urlpatterns)
