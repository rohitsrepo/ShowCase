from .models import User
from .serializers import PaginatedUserSerializer
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from ShowCase.utils import check_object_permissions
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class UserFollowsAdd(APIView):

    permission_classes = ((permissions.IsAuthenticatedOrReadOnly,))

    def post(self, request, format=None):
        follows = request.DATA.get('follows')

        if not follows:
            return Response({"follows": "This field is required"}, status=status.HTTP_400_BAD_REQUEST)
        elif request.user.id in follows:
            follows.remove(request.user.id)

        request.user.followers.add(*follows)
        return Response(status=status.HTTP_201_CREATED)

class UserFollowsDelete(APIView):

    permission_classes = ((permissions.IsAuthenticatedOrReadOnly,))

    def delete(self, request, pk, format=None):
        request.user.followers.remove(pk)
        return Response(status=status.HTTP_201_CREATED)

class UserFollowsRead(APIView):

    permission_classes = ((permissions.AllowAny,))

    def get(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        user_collection = user.followers.all().order_by('-id')

        page_num = request.GET.get('page', 1)
        paginator = Paginator(user_collection, 15)

        try:
            this_page_users = paginator.page(page_num)
        except PageNotAnInteger:
            this_page_users = paginator.page(1)
        except EmptyPage:
            raise Http404

        serializer = PaginatedUserSerializer(this_page_users)
        return Response(data=serializer.data)