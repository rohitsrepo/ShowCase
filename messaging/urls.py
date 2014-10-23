from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
                       url(r'^/$', views.MessageList.as_view(),
                           name='message-list'),
                       )
