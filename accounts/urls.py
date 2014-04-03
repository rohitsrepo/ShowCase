from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = patterns('',
    url(r'^/$', views.UserList.as_view()),
    url(r'^/(?P<pk>[0-9]+)$', views.UserDetail.as_view(), name='user-detail'),
    url(r'^/(?P<pk>[0-9]+)/set_password$', 'accounts.views.reset_password'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #url(r'^snippets/(?P<pk>[0-9]+)$', 'snippet_detail'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
