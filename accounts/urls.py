from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = patterns('',
                        url(r'^$', views.UserList.as_view()),
                        url(r'^/login$', 'accounts.views.login_user'),
                        url(r'^/logout$', 'accounts.views.logout_user'),
                        url(r'^/currentUser$', 'accounts.views.get_current_user'),
                        url(r'^/search$', 'accounts.views.search_artist'),
                        url(r'^/reset-name$', 'accounts.views.reset_name'),
                        url(r'^/reset-about$', 'accounts.views.reset_about'),
                        url(r'^/reset-picture$', 'accounts.views.reset_picture'),
                        url(r'^/(?P<pk>[0-9]+)$', views.UserDetail.as_view(), name='user-detail'),
                        url(r'^/(?P<pk>[0-9]+)/set_password$', 'accounts.views.reset_password'),
                        url(r'^/bookmarks$', views.UserBookmarksAdd.as_view()),
                        url(r'^/bookmarks/(?P<pk>[0-9]+)$', views.UserBookmarksDelete.as_view()),
                        url(r'^/(?P<pk>[0-9]+)/bookmarks$', views.UserBookmarksRead.as_view()),
                        url(r'^/(?P<pk>[0-9]+)/follows$', 'accounts.views.user_follows'),
                        url(r'^/(?P<pk>[0-9]+)/compositions$', 'accounts.views.get_compositions'),
                        url(r'^/(?P<pk>[0-9]+)/interpretations$', 'accounts.views.get_interpretations'),
                        url(r'^/(?P<pk>[0-9]+)/uploads$', 'accounts.views.get_uploads'),
                        url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
                    )

urlpatterns = format_suffix_patterns(urlpatterns)
