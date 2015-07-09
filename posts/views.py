from .models import Post
from .serializers import PostSerializer
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response


class CompositionPostList(APIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

	def get(self, request, composition_id, format=None):
		posts = Post.objects.filter(composition_id = composition_id)
		serializer = PostSerializer(posts, context={'request': request})
		return Response(serializer.data)



