from .models import Bucket
from .permissions import IsOwnerOrReadOnly
from .serializers import BucketSerializer, PaginatedBucketCompositionSerializer
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class BuckettList(APIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

	def get(self, request, user_id, format=None):
		user = get_object_or_404(User, pk=user_id)
		buckets = user.buckets.all()
		serializer = BucketSerializer(buckets, context={'request': request})
		return Response(data=serializer.data)

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

        serializer = PaginatedBucketCompositionSerializer(post, context={'request': request})
        return Response(serializer.data)

    def put(self, request, bucket_id, format=None):
        compositions = request.DATA.get('compositions')
        if not compositions:
            return Response({"compositions": "This field is required"}, status=status.HTTP_400_BAD_REQUEST)

        bucket = get_object_or_404(Bucket, id=bucket_id)
        self.check_object_permissions(request, bucket)

        bucket.add(*compositions)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, bucket_id, format=None):
        composition = request.DATA.get('composition')

        bucket = get_object_or_404(Bucket, id=bucket_id)
        self.check_object_permissions(request, bucket)

        bucket.compositions.remove(composition)
        
        return Response(status=status.HTTP_201_CREATED)
