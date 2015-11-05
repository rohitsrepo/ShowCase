from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .serializers import SearchSerializer, PaginatedSearchSerializer

from haystack.query import SearchQuerySet
from haystack.inputs import Clean
from accounts.models import User
from buckets.models import Bucket
from compositions.models import Composition

def paginate(request, all_results):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(all_results, 30)

    try:
        this_page_results = paginator.page(page_num)
    except PageNotAnInteger:
        this_page_results = paginator.page(1)
    except EmptyPage:
        return Response({'results': [], 'next': ''}, status=status.HTTP_200_OK)

    serializer = PaginatedSearchSerializer(this_page_results, context={'request': request})
    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def search(request, format=None):
    q = request.GET.get('q', '')
    if q is '' or not q:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    all_results = SearchQuerySet().filter(content=Clean(q))

    return paginate(request, all_results)

@api_view(['GET'])
def search_users(request, format=None):
    q = request.GET.get('q', '')
    if q is '' or not q:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    all_results = SearchQuerySet().models(User).filter(content=Clean(q))

    return paginate(request, all_results)


@api_view(['GET'])
def search_buckets(request, format=None):
    q = request.GET.get('q', '')
    if q is '' or not q:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    all_results = SearchQuerySet().models(Bucket).filter(content=Clean(q))

    return paginate(request, all_results)

@api_view(['GET'])
def search_compositions(request, format=None):
    q = request.GET.get('q', '')
    if q is '' or not q:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    all_results = SearchQuerySet().models(Composition).filter(content=Clean(q))

    return paginate(request, all_results)
