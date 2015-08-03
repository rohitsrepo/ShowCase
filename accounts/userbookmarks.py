from .models import User
from .artistSerializers import PaginatedUserCompositionSerializer
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from ShowCase.utils import check_object_permissions
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class UserBookmarksAdd(APIView):

    permission_classes = ((permissions.IsAuthenticatedOrReadOnly,))

    def post(self, request, format=None):
        bookmarks = request.DATA.get('bookmarks')
        if not bookmarks:
            return Response({"bookmarks": "This field is required"}, status=status.HTTP_400_BAD_REQUEST)
        request.user.bookmarks.add(*bookmarks)
        return Response(status=status.HTTP_201_CREATED)

class UserBookmarksDelete(APIView):

    permission_classes = ((permissions.IsAuthenticatedOrReadOnly,))

    def delete(self, request, pk, format=None):
        request.user.bookmarks.remove(pk)
        return Response(status=status.HTTP_201_CREATED)

class UserBookmarksRead(APIView):

    permission_classes = ((permissions.AllowAny,))

    def get(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        user_collection = user.bookmarks.all().order_by('-id')

        page_num = request.GET.get('page', 1)
        paginator = Paginator(user_collection, 9)

        try:
            this_page_compositions = paginator.page(page_num)
        except PageNotAnInteger:
            this_page_compositions = paginator.page(1)
        except EmptyPage:
            raise Http404

        serializer = PaginatedUserCompositionSerializer(this_page_compositions)
        return Response(data=serializer.data)