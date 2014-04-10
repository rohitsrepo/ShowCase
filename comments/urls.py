from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^/$', views.CommentList.as_view(), name='comment-list'),
    url(r'^/(?P<comment_id>[0-9]+)$', views.CommentDetail.as_view(), name='comment-detail'),
)
