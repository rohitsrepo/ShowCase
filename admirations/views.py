from django.http import Http404
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.contenttypes.models import ContentType

from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView

from ShowCase.utils import check_object_permissions

from .models import Admiration
from .serializers import PaginatedAdmirationSerializer, AdmirationContentCreateSerializer

from accounts.models import User
from compositions.models import Composition
from buckets.models import Bucket

class AdmirationsList(APIView):

    permission_classes = ((permissions.IsAuthenticated,))

    def post(self, request, format=None):
        serializer = AdmirationContentCreateSerializer(data=request.DATA, context={'request': request})
        if serializer.is_valid():
            if (serializer.data['content_type'] == Admiration.ART):
                content_object = get_object_or_404(Composition, id=serializer.data['object_id'])
                ctype = ContentType.objects.get(app_label='compositions', model='composition')
                content_type = Admiration.ART
            elif (serializer.data['content_type'] == Admiration.BUCKET):
                content_object = get_object_or_404(Bucket, id=serializer.data['object_id'])
                ctype = ContentType.objects.get(app_label='buckets', model='bucket')
                content_type = Admiration.BUCKET
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            Admiration.objects.get_or_create(owner=request.user,
                object_id=content_object.id,
                content_type=ctype,
                admire_type=content_type)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        serializer = AdmirationContentCreateSerializer(data=request.DATA, context={'request': request})
        if serializer.is_valid():
            content_type = serializer.data['content_type']

            if (content_type == Admiration.ART):
                ctype = ContentType.objects.get(app_label='compositions', model='composition')
            elif (content_type == Admiration.BUCKET):
                ctype = ContentType.objects.get(app_label='buckets', model='bucket')
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            try:
                Admiration.objects.get(owner=request.user,
                    object_id=serializer.data['object_id'],
                    content_type=ctype,
                    admire_type=content_type).delete()
            except:
                pass

            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdmirationsListRead(APIView):

    permission_classes = ((permissions.AllowAny,))

    def get(self, request, user_id, format=None):
        user = get_object_or_404(User, id=user_id)
        user_admirations = user.admirations.all().order_by('-created')

        page_num = request.GET.get('page', 1)
        paginator = Paginator(user_admirations, 9)

        try:
            this_page_admirations = paginator.page(page_num)
        except PageNotAnInteger:
            this_page_admirations = paginator.page(1)
        except EmptyPage:
            raise Http404

        serializer = PaginatedAdmirationSerializer(this_page_admirations, context={'request': request})
        return Response(data=serializer.data)