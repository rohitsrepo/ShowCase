import urllib2

from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File

from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Bucket, BucketMembership
from .permissions import IsOwnerOrReadOnly
from .serializers import BucketSerializer, BucketBackgroundSerializer

from compositions.models import Composition
from compositions.serializers import CompositionSerializer
from accounts.models import User

class BucketList(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def post(self, request, format=None):
        serializer = BucketSerializer(data=request.DATA, context={'request': request})
        if serializer.is_valid():
            serializer.object.owner = request.user
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BucketDetail(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get(self, request, bucket_slug, format=None):
        bucket = get_object_or_404(Bucket, slug=bucket_slug)
        serializer = BucketSerializer(bucket, context={'request': request})
        return Response(serializer.data)

    def delete(self, request, bucket_slug, format=None):
        bucket = get_object_or_404(Bucket, slug=bucket_slug)
        self.check_object_permissions(self.request, bucket)
        bucket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, bucket_slug, format=None):
        bucket = get_object_or_404(Bucket, slug=bucket_slug)
        self.check_object_permissions(self.request, bucket)

        ser = BucketSerializer(bucket, data=request.DATA, context={'request': request})
        
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

class BucketCompositionList(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get(self, request, bucket_id, format=None):
        # TODO Add serialization and accordingly pagination logic

        bucket = get_object_or_404(Bucket, id=bucket_id)
        bucket.views = bucket.views + 1
        bucket.save();

        compositions = bucket.compositions.all()
        serializer = CompositionSerializer(compositions, context={'request': request})
        return Response(serializer.data)

    def put(self, request, bucket_id, format=None):
        composition_id = request.DATA.get('composition_id')
        if not composition_id:
            return Response({"composition_id": "This field is required"}, status=status.HTTP_400_BAD_REQUEST)

        bucket = get_object_or_404(Bucket, id=bucket_id)
        self.check_object_permissions(request, bucket)
        composition = get_object_or_404(Composition, id=composition_id)

        BucketMembership.objects.get_or_create(bucket=bucket, composition=composition)

        return Response(status=status.HTTP_201_CREATED)

class BucketCompositionDetail(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def delete(self, request, bucket_id, composition_id, format=None):
        bucket = get_object_or_404(Bucket, id=bucket_id)
        self.check_object_permissions(request, bucket)

        try:
            membership = BucketMembership.objects.get(composition=composition_id, bucket=bucket)
            membership.delete()
        except BucketMembership.DoesNotExist:
            pass

        return Response(status=status.HTTP_201_CREATED)

class BucketBackground(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get_image_from_web(self, image_url):
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urllib2.urlopen(image_url).read())
        img_temp.flush()

        return img_temp

    def get_image_from_upload(self, image_file):
        dest = NamedTemporaryFile(delete=True)
        for chunk in image_file.chunks():
            dest.write(chunk)
        return dest

    def update_background(self, bucket, upload_object):
        if (upload_object['upload_type'] == 'url'):
            image_file = self.get_image_from_web(upload_object['upload_url'])
        elif (upload_object['upload_type'] == 'upl'):
            image_file = self.get_image_from_upload(upload_object['upload_image'])

        bucket.background = File(image_file)
        bucket.save();

    def post(self, request, bucket_id, format=None):
        bucket = get_object_or_404(Bucket, id=bucket_id)
        self.check_object_permissions(request, bucket)

        back_ser = BucketBackgroundSerializer(data=request.DATA, files=request.FILES, context={'request': request})
        if back_ser.is_valid():
            self.update_background(bucket, back_ser.object)

            bucket_ser = BucketSerializer(bucket, context={'request': request})
            return Response(bucket_ser.data)

        return Response(data=bucket_ser.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_composition_buckets(request, composition_id, format=None):
    composition = get_object_or_404(Composition, pk=composition_id)
    buckets = composition.holders.all()
    serializer = BucketSerializer(buckets, context={'request': request})
    return Response(data=serializer.data)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_user_buckets(request, user_id, format=None):
    user = get_object_or_404(User, pk=user_id)
    buckets = user.buckets.all()
    serializer = BucketSerializer(buckets, context={'request': request})
    return Response(data=serializer.data)
