from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = patterns('',
    url(r'^/$', views.VoteDetail.as_view(), name='vote-detail'),
)

#urlpatterns = format_suffix_patterns(urlpatterns)

