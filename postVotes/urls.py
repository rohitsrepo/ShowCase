from django.conf.urls import patterns, url, include
from . import views

urlpatterns = patterns('',
                       url(r'^$', views.VoteList.as_view()),
                       )
