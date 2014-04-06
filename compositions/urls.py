from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = patterns('',
    url(r'^/$', views.CompositionList.as_view()),
    url(r'^/(?P<pk>[0-9]+)/$', views.CompositionDetail.as_view(), name='composition-detail'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
