from django.http import Http404
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.contenttypes.models import ContentType

from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView

from ShowCase.utils import check_object_permissions

from .models import BookMark
from .serializers import PaginatedBookmarkSerializer, BookmarkContentCreateSerializer

from compositions.models import Composition
from buckets.models import Bucket

class BookmarksList(APIView):

    permission_classes = ((permissions.IsAuthenticated,))

    def get(self, request, format=None):
        user_bookmarks = request.user.bookmarks.all().order_by('-id')

        page_num = request.GET.get('page', 1)
        paginator = Paginator(user_bookmarks, 9)

        try:
            this_page_bookmarks = paginator.page(page_num)
        except PageNotAnInteger:
            this_page_bookmarks = paginator.page(1)
        except EmptyPage:
            raise Http404

        serializer = PaginatedBookmarkSerializer(this_page_bookmarks, context={'request': request})
        return Response(data=serializer.data)

    def post(self, request, format=None):
        serializer = BookmarkContentCreateSerializer(data=request.DATA, context={'request': request})
        if serializer.is_valid():
            if (serializer.data['bookmark_type'] == BookMark.ART):
                content_object = get_object_or_404(Composition, id=serializer.data['object_id'])
                ctype = ContentType.objects.get(app_label='compositions', model='composition')
            elif (serializer.data['bookmark_type'] == BookMark.BUCKET):
                content_object = get_object_or_404(Bucket, id=serializer.data['object_id'])
                ctype = ContentType.objects.get(app_label='buckets', model='bucket')
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            BookMark.objects.get_or_create(owner=request.user,
                object_id=content_object.id,
                content_type=ctype)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        serializer = BookmarkContentCreateSerializer(data=request.DATA, context={'request': request})
        if serializer.is_valid():
            if (serializer.data['bookmark_type'] == BookMark.ART):
                ctype = ContentType.objects.get(app_label='compositions', model='composition')
            elif (serializer.data['bookmark_type'] == BookMark.BUCKET):
                ctype = ContentType.objects.get(app_label='buckets', model='bucket')
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            try:
                BookMark.objects.get(owner=request.user,
                    object_id=serializer.data['object_id'],
                    content_type=ctype).delete()
            except:
                pass

            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
