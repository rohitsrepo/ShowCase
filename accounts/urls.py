from django.conf.urls import patterns, url, include

from rest_framework.urlpatterns import format_suffix_patterns

from . import views
from . import userfollows
from .auth_views import EmailPermissionRedirect, CustomUserCallback

from posts.views import UserPostList, UserPostDetail
from streams.views import UserActivities, UserNews

urlpatterns = patterns('',
                      url(r'^$', views.UserList.as_view()),
                      url(r'^/login/(?P<provider>(\w|-)+)/$', EmailPermissionRedirect.as_view(query_string=True), name='auth-login'),
                      url(r'^/callback/(?P<provider>(\w|-)+)/$', CustomUserCallback.as_view(), name='auth-callback'),
                      url(r'^/success/(?P<provider>(\w|-)+)/$', 'accounts.auth_views.auth_success', name='auth-success'),
                      url(r'^/failure/(?P<provider>(\w|-)+)/$', 'accounts.auth_views.auth_failure', name='auth-failure'),
                      url(r'^/login$', 'accounts.views.login_user'),
                      url(r'^/logout$', 'accounts.views.logout_user'),
                      url(r'^/currentUser$', 'accounts.views.get_current_user'),
                      url(r'^/search$', 'accounts.views.search_artist'),
                      url(r'^/reset-name$', 'accounts.settingsViews.reset_name'),
                      url(r'^/reset-about$', 'accounts.settingsViews.reset_about'),
                      url(r'^/reset-nsfw$', 'accounts.settingsViews.reset_nsfw'),
                      url(r'^/reset-picture$', 'accounts.settingsViews.reset_picture'),
                      url(r'^/(?P<pk>[0-9]+)$', views.UserDetail.as_view(), name='user-detail'),
                      url(r'^/(?P<pk>[0-9]+)/set_password$', 'accounts.views.reset_password'),
                      url(r'^/follows$', userfollows.UserFollowsAdd.as_view()),
                      url(r'^/follows/(?P<pk>[0-9]+)$', userfollows.UserFollowsDelete.as_view()),
                      url(r'^/(?P<pk>[0-9]+)/follows$', userfollows.UserFollowsRead.as_view()),
                      url(r'^/(?P<pk>[0-9]+)/followers$', userfollows.UserFollowersRead.as_view()),
                      url(r'^/(?P<pk>[0-9]+)/compositions$', 'accounts.views.get_compositions'),
                      url(r'^/(?P<pk>[0-9]+)/interpretations$', 'accounts.views.get_interpretations'),
                      url(r'^/(?P<pk>[0-9]+)/uploads$', 'accounts.views.get_uploads'),
                      url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                      url(r'^/(?P<user_id>[0-9]+)/posts$', UserPostList.as_view()),
                      url(r'^/(?P<user_id>[0-9]+)/posts/(?P<post_id>[0-9]+)$', UserPostDetail.as_view()),
                      url(r'^/(?P<user_id>[0-9]+)/buckets$', 'buckets.views.get_user_buckets'),
                      url(r'^/(?P<user_id>[0-9]+)/activities$', UserActivities.as_view()),
                      url(r'^/(?P<user_id>[0-9]+)/news$', UserNews.as_view()),
                    )

urlpatterns = format_suffix_patterns(urlpatterns)
