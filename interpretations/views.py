from .models import Interpretation
from .serializers import InterpretationSerializer
from .permissions import IsInterpreterOrReadOnly
from compositions.models import Composition
from rest_framework import status, permissions
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


class InterpretationList(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_interpretations(self, composition_id):
        return Interpretation.objects.filter(composition=composition_id, public=True)

    def add_voting_status(self, interpretations, user, serializer):
        counter = 0;
        for interpretation in interpretations:
            serializer.data[counter]['voting_status'] = interpretation.vote.get_voting_status(user)
            counter += 1

    def add_comment_count(self, interpretations, serializer):
        counter = 0
        for interpretation in interpretations:
            serializer.data[counter]['comments_count'] = interpretation.comment_set.count()
            counter += 1


    def get(self, request, composition_id, format=None):
        interpretations = self.get_interpretations(composition_id)
        serializer = InterpretationSerializer(
            interpretations, many=True, context={'request': request})

        if request.user.is_authenticated():
            self.add_voting_status(interpretations, request.user, serializer)

        self.add_comment_count(interpretations, serializer)

        return Response(serializer.data)

    def post(self, request, composition_id, format=None):
        serializer = InterpretationSerializer(
            data=request.DATA, context={'request': request})
        if serializer.is_valid():
            serializer.object.user = request.user
            serializer.object.public = True
            serializer.object.composition = get_object_or_404(
                Composition, id=composition_id)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InterpretationDetail(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsInterpreterOrReadOnly)

    def put(self, request, composition_id, interpretation_id, format=None):
        interpretation = get_object_or_404(Interpretation, id=interpretation_id)
        self.check_object_permissions(request, interpretation)
        serializer = InterpretationSerializer(interpretation, data=request.DATA)
        if serializer.is_valid():
            serializer.object.edited = True
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, composition_id, interpretation_id, format=None):
        interpretation = get_object_or_404(Interpretation, id=interpretation_id)
        self.check_object_permissions(request, interpretation)
        interpretation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
