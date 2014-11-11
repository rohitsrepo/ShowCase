from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
                       url(r'^$', views.InterpretationList.as_view(), name='interpretation-list'),
                       url(r'^/(?P<interpretation_id>[0-9]+)$',
                           views.InterpretationDetail.as_view(), name='interpretation-detail'),
                       )
