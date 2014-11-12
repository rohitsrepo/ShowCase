from .models import Interpretation
from .serializers import InterpretationSerializer
from .permissions import IsInterpreterOrReadOnly
from compositions.models import Composition
from rest_framework import status, permissions
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from interpretationVotes  import signals
from notifications import notify


class InterpretationList(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_interpretations(self, composition_id):
        return Interpretation.objects.filter(composition=composition_id)

    def get(self, request, composition_id, format=None):
        interpretaions = self.get_interpretations(composition_id)
        serializer = InterpretationSerializer(
            interpretaions, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, composition_id, format=None):
        serializer = InterpretationSerializer(
            data=request.DATA, context={'request': request})
        if serializer.is_valid():
            serializer.object.user = request.user
            serializer.object.composition = get_object_or_404(
                Composition, id=composition_id)
            serializer.save()
            # Add notification.
            intrepretation = serializer.object
            if request.user != intrepretation.composition.artist:
                notify.send(request.user, recipient=intrepretation.composition.artist,
                            verb='added interpretaion', action_object=intrepretation, target=intrepretation.composition)
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
