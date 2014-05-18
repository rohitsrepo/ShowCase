from django.shortcuts import render
from .models import Comment
from .serializers import CommentSerializer
from .permissions import IsCommenterOrReadOnly
from compositions.models import Composition
from rest_framework import status, permissions
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

class CommentList(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_comments(self, composition_id):
	return  Comment.objects.filter(composition=composition_id)

    def get(self, request, pk, format=None):
	comments = self.get_comments(pk)
	serializer = CommentSerializer(comments, many=True, context={'request': request})
	return Response(serializer.data)

    def post(self, request, pk, format=None):
	serializer = CommentSerializer(data=request.DATA, context={'request': request})
	if serializer.is_valid():
	    serializer.object.commenter = request.user
	    serializer.object.composition = get_object_or_404(Composition, id=pk)
	    serializer.save()
	    return Response(serializer.data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetail(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsCommenterOrReadOnly)
    
    def get(self, request, pk, comment_id, format=None):
	comment = get_object_or_404(Comment, id=comment_id)
	serializer = CommentSerializer(comment)
	return Response(serializer.data)

    def put(self, request, pk, comment_id, format=None):
	comment = get_object_or_404(Comment, id=comment_id)
	serializer = CommentSerializer(comment, data=request.DATA)
	if serializer.is_valid():
	    serializer.object.edited = True
	    serializer.save()
	    return Response(serializer.data)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, comment_id, format=None):
	comment = get_object_or_404(Comment, id=comment_id)
	comment.delete()
	return Response(status=status.HTTP_204_NO_CONTENT)
