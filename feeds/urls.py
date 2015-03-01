from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = patterns('',
                       url(r'^/editors$', 'feeds.views.editors_pick_list'),
                       url(r'^/fresh$', 'feeds.views.fresh_list'),
                       )

urlpatterns = format_suffix_patterns(urlpatterns)