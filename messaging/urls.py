from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
                       url(r'^$', views.MessageList.as_view(),
                           name='message-list'),
                       url(r'^/(?P<message_id>[0-9]+)/mark_as_read$', 'messaging.views.markAsRead',
                           name='mark-message-read')
                       )
