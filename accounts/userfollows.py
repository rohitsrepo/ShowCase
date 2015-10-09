from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView

from ShowCase.utils import check_object_permissions

from .models import User
from .serializers import ExistingUserSerializer

from streams.manager import follow_user, unfollow_user

def follow_staff_user(user_id):
    staff_user = User.objects.get(email='info@thirddime.com')
    follow_user(user_id, staff_user.id)

class UserFollowsAdd(APIView):

    permission_classes = ((permissions.IsAuthenticatedOrReadOnly,))

    def post(self, request, format=None):
        follows = request.DATA.get('follows')

        if not follows:
            return Response({"follows": "This field is required"}, status=status.HTTP_400_BAD_REQUEST)
        elif str(request.user.id) in follows:
            follows.remove(str(request.user.id))

        request.user.follows.add(*follows)

        for follow in follows:
            follow_user(request.user.id, follow)

        return Response(status=status.HTTP_201_CREATED)

class UserFollowsDelete(APIView):

    permission_classes = ((permissions.IsAuthenticatedOrReadOnly,))

    def delete(self, request, pk, format=None):
        request.user.follows.remove(pk)
        unfollow_user(request.user.id, pk)
        return Response(status=status.HTTP_201_CREATED)

class UserFollowsRead(APIView):

    permission_classes = ((permissions.AllowAny,))

    def get(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        user_follows = user.follows.all().order_by('-id')
        serializer = ExistingUserSerializer(user_follows, context={'request': request})
        return Response(data=serializer.data)

class UserFollowersRead(APIView):

    permission_classes = ((permissions.AllowAny,))

    def get(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        user_followers = user.followers.all().order_by('-id')
        serializer = ExistingUserSerializer(user_followers, context={'request': request})
        return Response(data=serializer.data)
