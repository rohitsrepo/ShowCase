from .models import Vote
from compositions.models import Composition
from .permissions import HasNotVotedBeforeOrReadOnly
from .serializers import VoteSerializer, VotingSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

class VoteDetail(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, HasNotVotedBeforeOrReadOnly)

    def get_object(self, pk):
	try:
	    return Vote.objects.get(composition=Composition.objects.get(pk=pk))
	except Composition.DoesNotExist:
	    raise Http404

    def get(self, request, pk, format=None):
	vote = self.get_object(pk)
	serializer = VoteSerializer(vote, context={'request':request})
	return Response(serializer.data)

    def put(self, request, pk, format=None):
	vote = self.get_object(pk)
	self.check_object_permissions(request,vote)
	serializer = VotingSerializer(vote, data=request.DATA)
	if serializer.is_valid():
	    if serializer.data['vote']:
		vote.vote_positive(request.user)
	    else:
		vote.vote_negative(request.user)

	    updated_serializer = VoteSerializer(vote, context={'request':request})
	    return Response(updated_serializer.data)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

