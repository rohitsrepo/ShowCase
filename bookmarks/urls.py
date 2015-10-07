from django.conf.urls import patterns, url, include

from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = patterns('',
                      url(r'^$', views.BookmarksList.as_view()),
                    )

urlpatterns = format_suffix_patterns(urlpatterns)
