from .models import Comment
from .serializers import CommentSerializer
from .permissions import IsCommenterOrReadOnly
from interpretations.models import Interpretation
from rest_framework import status, permissions
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


class CommentList(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_comments(self, interpretation_id):
        return Comment.objects.filter(interpretation=interpretation_id)

    def get(self, request, composition_id, interpretation_id, format=None):
        comments = self.get_comments(interpretation_id)
        serializer = CommentSerializer(
            comments, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, composition_id, interpretation_id, format=None):
        serializer = CommentSerializer(
            data=request.DATA, context={'request': request})
        if serializer.is_valid():
            serializer.object.commenter = request.user
            serializer.object.interpretation = get_object_or_404(
                Interpretation, id=interpretation_id)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsCommenterOrReadOnly)

    def put(self, request, composition_id, interpretation_id, comment_id, format=None):
        comment = get_object_or_404(Comment, id=comment_id)
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(comment, data=request.DATA)
        if serializer.is_valid():
            serializer.object.edited = True
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, composition_id, interpretation_id, comment_id, format=None):
        comment = get_object_or_404(Comment, id=comment_id)
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
