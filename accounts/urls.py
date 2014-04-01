from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = patterns('',
    url(r'^/$', views.UserList.as_view()),
    url(r'^/(?P<pk>[0-9]+)$', views.UserDetail.as_view()),
    url(r'^/(?P<pk>[0-9]+)/set_password$', 'accounts.views.reset_password'),
    #url(r'^snippets/(?P<pk>[0-9]+)$', 'snippet_detail'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
