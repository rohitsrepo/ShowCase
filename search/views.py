from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .serializers import SearchSerializer

from haystack.query import SearchQuerySet
from haystack.inputs import Clean


@api_view(['GET'])
def search(request, format=None):
    q = request.GET.get('q', '')
    if q is '':
        return Response(status=status.HTTP_400_BAD_REQUEST)
    all_results = SearchQuerySet().filter(content=Clean(q))
    serializer = SearchSerializer(all_results, many=True, context={'request': request})
    return Response(data=serializer.data, status=status.HTTP_200_OK)
