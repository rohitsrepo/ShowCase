from .models import PostVote
from posts.models import Post
from .serializers import VoteSerializer, VotingSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status


class VoteList(APIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,)

    def get_object(self, post_id):
        try:
            return PostVote.objects.get(post=post_id)
        except PostVote.DoesNotExist:
            raise Http404

    def post(self, request, post_id, format=None):
        vote = self.get_object(post_id)
        if vote.has_voted(request.user):
            return Response({"Error": "User has already voted."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = VotingSerializer(vote, data=request.DATA)
        if serializer.is_valid():
            if serializer.data['vote']:
                vote.vote_positive(request.user)
            else:
                vote.vote_negative(request.user)

            updated_serializer = VoteSerializer(vote, context={'request': request})
            return Response(updated_serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
