from .models import InterpretationVote
from interpretations.models import Interpretation
from .serializers import VoteSerializer, VotingSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from notifications import notify


class VoteDetail(APIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,)

    def get_object(self, interpretation_id):
        try:
            return InterpretationVote.objects.get(interpretation=Interpretation.objects.get(pk=interpretation_id))
        except Interpretation.DoesNotExist:
            raise Http404

    def get(self, request, composition_id, interpretation_id, format=None):
        vote = self.get_object(interpretation_id)
        serializer = VoteSerializer(vote, context={'request': request})
        return Response(serializer.data)

    def post(self, request, composition_id, interpretation_id, format=None):
        vote = self.get_object(interpretation_id)
        if not self.canVote(request, vote):
            return Response({"Error": "User has already voted."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = VotingSerializer(vote, data=request.DATA)
        if serializer.is_valid():
            if serializer.data['vote']:
                vote.vote_positive(request.user)

                # Add notification.
                if request.user != vote.interpretation.user:
                    notify.send(
                        request.user, recipient=vote.interpretation.user, verb='voted', target=vote.interpretation)
            else:
                vote.vote_negative(request.user)

            updated_serializer = VoteSerializer(
                vote, context={'request': request})
            return Response(updated_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def canVote(self, request, vote):
        self.check_object_permissions(request, vote)
        if vote.has_voted(request.user):
            return False

        return True
