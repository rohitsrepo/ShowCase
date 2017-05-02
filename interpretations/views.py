from django.shortcuts import get_object_or_404

from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Interpretation
from .serializers import InterpretationSerializer
from .permissions import IsInterpreterOrReadOnly
from compositions.models import Composition


class InterpretationList(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def post(self, request, composition_id, format=None):
        serializer = InterpretationSerializer(
            data=request.DATA, context={'request': request})
        if serializer.is_valid():
            serializer.object.user = request.user
            serializer.object.composition = get_object_or_404(
                Composition, id=composition_id)
            serializer.object.public = True
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InterpretationDetail(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsInterpreterOrReadOnly)

    def put(self, request, interpretation_id, format=None):
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

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_composition_interprets(request, composition_id, format=None):
    composition = get_object_or_404(Composition, pk=composition_id)
    interprets = composition.interprets.filter(public=True, is_draft=False).order_by('-created')
    serializer = InterpretationSerializer(interprets, context={'request': request})
    return Response(data=serializer.data)
