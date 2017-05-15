from django.shortcuts import get_object_or_404

from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Interpretation
from .serializers import InterpretationSerializer
from .permissions import IsInterpreterOrReadOnly

from buckets.models import Bucket
from buckets.serializers import BucketSerializer
from compositions.models import Composition
from compositions.serializers import CompositionSerializer


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

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_related(request, interpretation_id, format=None):
    interpretation = get_object_or_404(Interpretation, id=interpretation_id)
    relatedBuckets = Bucket.objects.filter(public=True, owner=interpretation.user).order_by('-views')[:2]
    relatedWorks = Composition.objects.exclude(id=interpretation.composition.id, uploader=interpretation.user).order_by('-created')[:3]
    relatedInterprets = Interpretation.objects.filter(public=True, is_draft=False, user=interpretation.user).exclude(id=interpretation.id).order_by('-created')

    relatedBucketsCount = Bucket.objects.filter(public=True, owner=interpretation.user).count()
    relatedWorksCount = Composition.objects.exclude(id=interpretation.composition.id, uploader=interpretation.user).count()
    relatedInterpretsCount = Interpretation.objects.filter(public=True, is_draft=False, user=interpretation.user).exclude(id=interpretation.id).count()

    relatedBucketsSerializer = BucketSerializer(relatedBuckets, context={'request': request})
    relatedWorksSerializer = CompositionSerializer(relatedWorks, context={'request': request})
    relatedInterpretsSerializer = InterpretationSerializer(relatedInterprets, context={'request': request})

    result = {'relatedBuckets': relatedBucketsSerializer.data,
    'relatedInterprets': relatedInterpretsSerializer.data,
    'relatedWorks': relatedWorksSerializer.data,
    'counts': {'relatedBuckets': relatedBucketsCount,
        'relatedInterprets': relatedInterpretsCount,
        'relatedWorks': relatedWorksCount
    }}

    return Response(result)