from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response

from .manager import get_user_feed, get_news_feeds

from posts.models import Post
from posts.serializers import PostSerializer

from accounts.models import User

def fetch_activity_posts(feed, next_token):
    if next_token:
        user_activities = feed.get(limit=11, id_lte=next_token)['results']
    else:
        user_activities = feed.get(limit=11)['results']

    if (len(user_activities) == 11):
        new_next_token = user_activities.pop()['id']
    else:
        new_next_token = ''

    user_activity_post_ids = [activity['foreign_id'] for activity in user_activities]
    user_activity_posts = Post.objects.filter(id__in=user_activity_post_ids).order_by('-created')

    return (user_activity_posts, new_next_token)

class UserActivities(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get(self, request, user_id, format=None):
        next_token = request.GET.get('next_token', '')
        user_feed = get_user_feed(user_id)

        user_activity_posts, new_next_token = fetch_activity_posts(user_feed, next_token)

        serializer = PostSerializer(user_activity_posts, context={'request': request})

        return Response(data={'results': serializer.data, 'next_token': new_next_token, 'count': len(serializer.data)})

class UserNews(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get(self, request, user_id, format=None):
        next_token = request.GET.get('next_token', '')
        user_feed = get_news_feeds(user_id)['flat']

        user_activity_posts, new_next_token = fetch_activity_posts(user_feed, next_token)

        serializer = PostSerializer(user_activity_posts, context={'request': request})

        return Response(data={'results': serializer.data, 'next_token': new_next_token, 'count': len(serializer.data)})

