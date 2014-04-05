from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from myapp import views

urlpatterns = patterns('',
    url(r'^myapp/$', views.CompositionList.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^myapp/(?P<pk>[0-9]+)/$', views.CompositionDetail.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)