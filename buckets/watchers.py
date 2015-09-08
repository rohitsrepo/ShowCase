from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView

from .models import Bucket
from accounts.serializers import ExistingUserSerializer

from streams.manager import follow_bucket, unfollow_bucket

class BucketWatcherDetail(APIView):

    permission_classes = ((permissions.IsAuthenticatedOrReadOnly,))

    def get(self, request, bucket_id, format=None):
        bucket = get_object_or_404(Bucket, id=bucket_id)
        bucket_watchers = bucket.watchers.all().order_by('-id')
        serializer = ExistingUserSerializer(bucket_watchers, context={'request': request})
        return Response(data=serializer.data)

    def put(self, request, bucket_id, format=None):
        bucket = get_object_or_404(Bucket, id=bucket_id)

        if bucket.owner.id==request.user.id:
            return Response(status=status.HTTP_200_OK)

        bucket.watchers.add(request.user)
        follow_bucket(request.user.id, bucket.id)

        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, bucket_id, format=None):
        bucket = get_object_or_404(Bucket, id=bucket_id)
        bucket.watchers.remove(request.user)
        unfollow_bucket(request.user.id, bucket.id)
        return Response(status=status.HTTP_201_CREATED)
