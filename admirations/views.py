import collections

from django.db import connection
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.contenttypes.models import ContentType

from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView

from ShowCase.utils import check_object_permissions

from .models import Admiration, AdmirationOption
from .serializers import AdmirationSerializer, PaginatedAdmirationSerializer, AdmirationContentCreateSerializer, OptionSerializer

from accounts.models import User
from accounts.serializers import ExistingUserSerializer
from compositions.models import Composition
from buckets.models import Bucket

class AdmirationsList(APIView):

    permission_classes = ((permissions.IsAuthenticatedOrReadOnly,))

    def get(self, request, format=None):
        serializer = AdmirationContentCreateSerializer(data=request.GET, context={'request': request})
        if serializer.is_valid():
            if (serializer.data['content_type'] == Admiration.ART):
                content_object = get_object_or_404(Composition, id=serializer.data['object_id'])
            elif (serializer.data['content_type'] == Admiration.BUCKET):
                content_object = get_object_or_404(Bucket, id=serializer.data['object_id'])
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            admirations = Admiration.objects.filter(
                object_id=serializer.data['object_id'],
                admire_type=serializer.data['content_type'])
            admirers = [admiration.owner for admiration in admirations]
            ser = ExistingUserSerializer(admirers, context={'request': request})

            return Response(ser.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        word = request.DATA.get('word', '')

        if len(word) > 20:
            return Response(data={'error': 'word can not be greater than 20 characters'}, status=status.HTTP_400_BAD_REQUEST)

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

            try:
                admire_option = AdmirationOption.objects.get(word__iexact=word)
            except AdmirationOption.DoesNotExist:
                raise Http404;

            try:
                admire_object = Admiration.objects.get(owner=request.user,
                    object_id=content_object.id,
                    content_type=ctype,
                    admire_type=content_type)
                admire_object.admire_as = admire_option
                admire_object.save()
            except Admiration.DoesNotExist:
                admire_object = Admiration.objects.create(owner=request.user,
                    object_id=content_object.id,
                    content_type=ctype,
                    admire_type=content_type,
                    admire_as=admire_option)

            admire_serializer = AdmirationSerializer(admire_object, context={'request': request})

            return Response(admire_serializer.data, status=status.HTTP_201_CREATED)
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

class UserAdmirationsList(APIView):

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

class ObjectAdmirationsList(APIView):

    permission_classes = ((permissions.AllowAny,))

    def get(self, request, format=None):
        serializer = AdmirationContentCreateSerializer(data=request.GET, context={'request': request})
        if serializer.is_valid():
            if (serializer.data['content_type'] == Admiration.ART):
                content_object = get_object_or_404(Composition, id=serializer.data['object_id'])
            elif (serializer.data['content_type'] == Admiration.BUCKET):
                content_object = get_object_or_404(Bucket, id=serializer.data['object_id'])
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)


        admirations = content_object.admirers.all()

        serializer = AdmirationSerializer(admirations, context={'request': request})
        return Response(data=serializer.data)

class ObjectAdmirationOptionsList(APIView):

    permission_classes = ((permissions.AllowAny,))

    def dictfetchall(self, cursor):
        "Returns all rows from a cursor as a dict"
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]

    def get_grouped_options(self, object_id, admire_type):
        cursor = connection.cursor()
        query = ("SELECT admirations.count as count, options.word as word, options.id as id FROM (SELECT count(*) as count, admire_as_id"
            " FROM admirations_admiration WHERE object_id={0} AND admire_type='{1}' GROUP BY admire_as_id) as admirations"
            " INNER JOIN admirations_admirationoption as options ON admirations.admire_as_id = options.id").format(object_id, admire_type)
        cursor.execute(query)

        return self.dictfetchall(cursor)

    def get(self, request, format=None):
        serializer = AdmirationContentCreateSerializer(data=request.GET, context={'request': request})
        if serializer.is_valid():
            response =  self.get_grouped_options(serializer.data['object_id'], serializer.data['content_type'])
            serializer = OptionSerializer(response)
            return Response(serializer.data)
        else:
            return Response(data.serializer.errors, status=status.HTTP_400_BAD_REQUEST)