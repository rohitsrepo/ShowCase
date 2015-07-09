from .serializers import CommentSerializer
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CommentSerializer
from .models import PostComment


class CommentList(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_comments(self, post_id):
        return PostComment.objects.filter(post=post_id)

    def get(self, request, post_id, format=None):
        comments = self.get_comments(post_id)
        serializer = CommentSerializer(
            comments, many=True, context={'request': request})
        return Response(serializer.data)

