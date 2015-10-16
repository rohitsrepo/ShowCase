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
from .permissions import IsOwnerOrReadOnlyIfPublic
from .serializers import BucketSerializer, BucketBackgroundSerializer, BucketMembershipCreateSerializer, BucketMembershipSerializer

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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnlyIfPublic)

    def get(self, request, bucket_slug, format=None):
        bucket = get_object_or_404(Bucket, slug=bucket_slug)
        self.check_object_permissions(self.request, bucket)
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

        ser = BucketSerializer(bucket, data=request.DATA, context={'request': request}, many=False)

        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

class BucketCompositionList(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnlyIfPublic)

    def get(self, request, bucket_id, format=None):
        bucket = get_object_or_404(Bucket, id=bucket_id)
        self.check_object_permissions(self.request, bucket)
        bucket.views = bucket.views + 1
        bucket.save();

        memberships = BucketMembership.objects.filter(bucket=bucket).order_by('-added')
        serializer = BucketMembershipSerializer(memberships, context={'request': request})
        return Response(serializer.data)

    def put(self, request, bucket_id, format=None):
        serializer = BucketMembershipCreateSerializer(data=request.DATA, context={'request': request})
        if serializer.is_valid():
            bucket = get_object_or_404(Bucket, id=bucket_id)
            self.check_object_permissions(request, bucket)
            composition = get_object_or_404(Composition, id=serializer.data['composition_id'])

            bucket, created = BucketMembership.objects.get_or_create(bucket=bucket, composition=composition)

            bucket.description = description=serializer.data['description']
            bucket.save()

            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BucketCompositionDetail(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnlyIfPublic)

    def get(self, request, bucket_id, composition_id, format=None):
        membership = get_object_or_404(BucketMembership, bucket=bucket_id, composition=composition_id)
        serializer = BucketMembershipSerializer(membership, context={'request': request})
        return Response(serializer.data)

    def put(self, request, bucket_id, composition_id, format=None):
        membership = get_object_or_404(BucketMembership, bucket=bucket_id, composition=composition_id)
        serializer = BucketMembershipSerializer(membership, data=request.DATA, context={'request': request})
        if serializer.is_valid():
            bucket = get_object_or_404(Bucket, id=bucket_id)
            self.check_object_permissions(request, bucket)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnlyIfPublic)

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

        return Response(data=back_ser.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_composition_buckets(request, composition_id, format=None):
    composition = get_object_or_404(Composition, pk=composition_id)
    buckets = composition.holders.filter(public=True).order_by('-created')
    serializer = BucketSerializer(buckets, context={'request': request})
    return Response(data=serializer.data)


def serialize_user_buckets(request, buckets):
    composition_id = request.GET.get('composition', '');

    if composition_id:
        try:
            composition_id = int(composition_id)
            serializer = BucketSerializer(buckets, context={'request': request,
                'composition_id': composition_id})
            return Response(data=serializer.data)
        except ValueError:
            pass

    serializer = BucketSerializer(buckets, context={'request': request})
    return Response(data=serializer.data)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_user_buckets(request, user_id, format=None):
    user = get_object_or_404(User, pk=user_id)
    buckets = user.buckets.filter(public=True).order_by('-created')
    return serialize_user_buckets(request, buckets)

@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def get_my_buckets(request, format=None):
    buckets = request.user.buckets.all().order_by('-created')
    return serialize_user_buckets(request, buckets)

@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def get_my_drafts(request, format=None):
    buckets = request.user.buckets.filter(public=False).order_by('-created')
    return serialize_user_buckets(request, buckets)


@api_view(['PUT'])
@permission_classes((permissions.IsAuthenticated,))
def make_bucket_public(request, bucket_id, format=None):
    bucket = get_object_or_404(Bucket, id=bucket_id)
    if not (bucket.owner.id == request.user.id):
        return Response(status=status.HTTP_403_FORBIDDEN)

    bucket.public = True;
    bucket.save()
    bucket.add_to_fresh_feed()

    return Response(status=status.HTTP_201_CREATED)
