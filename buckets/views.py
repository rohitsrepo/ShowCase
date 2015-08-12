from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Bucket, BucketMembership
from .permissions import IsOwnerOrReadOnly
from .serializers import BucketSerializer, PaginatedBucketCompositionSerializer

from compositions.models import Composition
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


class BucketComposition(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get(self, request, bucket_id, format=None):
        bucket = get_object_or_404(Bucket, id=bucket_id)
        compositions = bucket.compositions.all()

        page_num = request.GET.get('page', 1)
        paginator = Paginator(compositions, 9)

        try:
            this_page_compositions = paginator.page(page_num)
        except PageNotAnInteger:
            this_page_compositions = paginator.page(1)
        except EmptyPage:
            raise Http404

        serializer = PaginatedBucketCompositionSerializer(this_page_compositions, context={'request': request})
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

    def delete(self, request, bucket_id, format=None):
        composition_id = request.DATA.get('composition_id')
        if not composition_id:
            return Response({"composition_id": "This field is required"}, status=status.HTTP_400_BAD_REQUEST)

        bucket = get_object_or_404(Bucket, id=bucket_id)
        self.check_object_permissions(request, bucket)

        try:
            membership = BucketMembership.objects.get(composition=composition_id, bucket=bucket)
            membership.delete()
        except BucketMembership.DoesNotExist:
            pass

        return Response(status=status.HTTP_201_CREATED)


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