from django.conf.urls import patterns, url, include
from . import views

urlpatterns = patterns('',
                       url(r'^/(?P<post_id>[0-9]+)/comments', include('postComments.urls')),
                       url(r'^/(?P<post_id>[0-9]+)/votes', include('postVotes.urls')),
                       )
