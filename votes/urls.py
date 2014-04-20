from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
                       url(r'^/$', views.VoteDetail.as_view(), name='vote-detail'),)
