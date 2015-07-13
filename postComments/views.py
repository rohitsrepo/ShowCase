from .serializers import CommentSerializer
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CommentSerializer
from .models import PostComment
from django.shortcuts import get_object_or_404
from posts.models import Post

class CommentList(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_comments(self, post_id):
        return PostComment.objects.filter(post=post_id)

    def get(self, request, post_id, format=None):
        comments = self.get_comments(post_id)
        serializer = CommentSerializer(
            comments, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, post_id, format=None):
        serializer = CommentSerializer(data=request.DATA, context={'request': request})
        if serializer.is_valid():
            serializer.object.commenter = request.user
            serializer.object.post = get_object_or_404(Post, id=post_id)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

